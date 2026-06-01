#!/usr/bin/env node

/**
 * KAI Demo - Express Server
 * API Gateway va Real-time Communication
 */

const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const cors = require('cors');
const bodyParser = require('body-parser');
const queueManager = require('./queue-manager');
const emotionHandler = require('./emotion-handler');
const ttsClient = require('./tts-client');
const syncCoordinator = require('./sync-coordinator');

const app = express();
const server = http.createServer(app);
const io = socketIO(server, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST']
  }
});

// Middleware
app.use(cors());
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));

// Logger
const logger = require('./logger');

// Port
const PORT = process.env.PORT || 3000;

// ========== Queue Manager Instance ==========
const queue = new queueManager.QueueManager();

// ========== HTTP Routes ==========

/**
 * Health Check
 */
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

/**
 * Add input to queue
 * POST /api/input
 * Body: { platform, user_raw_name, payload, type }
 */
app.post('/api/input', async (req, res) => {
  try {
    const { platform, user_raw_name, payload, type } = req.body;
    
    if (!platform || !payload) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    const data = {
      platform,
      user_raw_name: user_raw_name || 'Anonymous',
      payload,
      type: type || 'chat',
      timestamp: new Date().toISOString()
    };
    
    await queue.enqueue(data);
    logger.info(`Input received from ${platform}: ${payload.substring(0, 50)}...`);
    
    res.json({ success: true, message: 'Data added to queue' });
  } catch (error) {
    logger.error(`POST /api/input error: ${error.message}`);
    res.status(500).json({ error: error.message });
  }
});

/**
 * Get queue status
 * GET /api/queue-status
 */
app.get('/api/queue-status', (req, res) => {
  const status = queue.getStatus();
  res.json(status);
});

/**
 * Get emotion tags
 * GET /api/emotions
 */
app.get('/api/emotions', (req, res) => {
  const emotions = emotionHandler.getEmotionMatrix();
  res.json(emotions);
});

/**
 * Test TTS
 * POST /api/test-tts
 * Body: { text, emotion }
 */
app.post('/api/test-tts', async (req, res) => {
  try {
    const { text, emotion } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'Text required' });
    }
    
    const audioUrl = await ttsClient.generateSpeech(text, emotion || '[CUTE]');
    res.json({ success: true, audioUrl });
  } catch (error) {
    logger.error(`TTS error: ${error.message}`);
    res.status(500).json({ error: error.message });
  }
});

// ========== Socket.IO Events ==========

io.on('connection', (socket) => {
  logger.info(`Client connected: ${socket.id}`);
  
  /**
   * Add input via socket
   */
  socket.on('add-input', async (data) => {
    try {
      await queue.enqueue(data);
      io.emit('queue-updated', { size: queue.size() });
    } catch (error) {
      socket.emit('error', { message: error.message });
    }
  });
  
  /**
   * Request output
   */
  socket.on('get-output', async () => {
    try {
      const output = await queue.dequeue();
      if (output) {
        socket.emit('output', output);
      }
    } catch (error) {
      socket.emit('error', { message: error.message });
    }
  });
  
  /**
   * Subscribe to real-time updates
   */
  socket.on('subscribe-updates', () => {
    socket.join('updates');
    socket.emit('subscribed', { message: 'Listening to updates' });
  });
  
  socket.on('disconnect', () => {
    logger.info(`Client disconnected: ${socket.id}`);
  });
});

// ========== Processing Loop ==========

async function processingLoop() {
  while (true) {
    try {
      const input = await queue.dequeue();
      
      if (input) {
        logger.info(`Processing: ${input.payload.substring(0, 50)}...`);
        
        // Emotion tagging
        const emotion = await emotionHandler.tagEmotion(input.payload, input.type);
        
        // Generate response (mock)
        const response = `[${emotion.substring(1, emotion.length - 1)}] Response to: ${input.payload}`;
        
        // TTS
        const audioUrl = await ttsClient.generateSpeech(response, emotion);
        
        // Sync coordination
        const syncData = await syncCoordinator.coordinateSync(response, emotion);
        
        // Output
        const output = {
          emotion_tag: emotion,
          text: response,
          audio_url: audioUrl,
          sync_data: syncData,
          user_name: input.user_raw_name,
          timestamp: new Date().toISOString()
        };
        
        // Emit to all connected clients
        io.to('updates').emit('output', output);
        
        // Cooldown
        await new Promise(resolve => setTimeout(resolve, 2500));
      } else {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    } catch (error) {
      logger.error(`Processing loop error: ${error.message}`);
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
}

// ========== Start Server ==========

server.listen(PORT, () => {
  logger.info(`KAI Demo Server running on port ${PORT}`);
  
  // Start processing loop
  processingLoop().catch(error => {
    logger.error(`Fatal error: ${error.message}`);
    process.exit(1);
  });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down...');
  server.close(() => {
    logger.info('Server closed');
    process.exit(0);
  });
});
