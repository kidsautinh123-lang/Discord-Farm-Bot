# KAI Demo System

Advanced Text-to-Speech & Emotion-Based Response System with Anti-Desync Protocol

## Features

✅ **Multi-Platform Input Stream** - TikTok, YouTube support
✅ **3-Layer Security Filter** - Input validation, blacklist, anti-jailbreak
✅ **Hybrid LLM Routing** - Local vs Cloud intelligence
✅ **Emotion Matrix** - 8 emotion tags with customizable responses
✅ **TTS Optimization** - Text normalization, emoji removal, abbreviation mapping
✅ **Anti-Desync Protocol** - Perfect text-voice synchronization
✅ **SQLite Memory** - Persistent context window with auto-cleanup
✅ **Real-time API** - Express + Socket.IO for live updates

## Project Structure

```
kai-demo/
├── python/
│   ├── main.py              # Main orchestrator
│   ├── security_filter.py   # 3-layer security
│   ├── llm_router.py        # LLM routing engine
│   ├── emotion_tagger.py    # Emotion classification
│   ├── tts_processor.py     # TTS optimization
│   ├── memory_manager.py    # SQLite management
│   └── anti_desync.py       # Sync protocol
├── javascript/
│   ├── server.js            # Express server
│   ├── queue-manager.js     # Queue management
│   ├── emotion-handler.js   # Emotion processing
│   ├── tts-client.js        # TTS client
│   ├── sync-coordinator.js  # Sync coordination
│   └── logger.js            # Logging
├── package.json             # Node.js dependencies
├── requirements.txt         # Python dependencies
└── README.md
```

## Installation

### Python Setup

```bash
cd kai-demo
pip install -r requirements.txt
```

### Node.js Setup

```bash
cd kai-demo
npm install
```

## Running the System

### Start Express Server

```bash
npm start
```

Server will run on `http://localhost:3000`

### Start Python Main System

```bash
python python/main.py
```

## API Endpoints

### Health Check

```
GET /health
```

### Add Input

```
POST /api/input
Content-Type: application/json

{
  "platform": "TikTok",
  "user_raw_name": "user123",
  "payload": "Em yeu anh rat nhieu nha",
  "type": "chat"
}
```

### Queue Status

```
GET /api/queue-status
```

### Emotion Tags

```
GET /api/emotions
```

### Test TTS

```
POST /api/test-tts
Content-Type: application/json

{
  "text": "Em yeu anh",
  "emotion": "[YANDERE]"
}
```

## Socket.IO Events

### Add Input

```javascript
socket.emit('add-input', {
  platform: 'TikTok',
  user_raw_name: 'user123',
  payload: 'Em yeu anh',
  type: 'chat'
});
```

### Get Output

```javascript
socket.on('output', (data) => {
  console.log('Emotion:', data.emotion_tag);
  console.log('Text:', data.text);
  console.log('Audio URL:', data.audio_url);
});
```

### Subscribe to Updates

```javascript
socket.emit('subscribe-updates');
socket.on('output', (data) => {
  // Receive updates
});
```

## Emotion Matrix

| Tag | Trigger | Style | Buffer Words |
|-----|---------|-------|---------------|
| CUTE | Praise, compliments | Sweet tone | nha, ne, um |
| YANDERE | Love confessions | Possessive | ..., hm, tsk |
| TSUNDERE | Teasing, pushing | Tsundere | hu, xi, che |
| TROLL | Jokes, hacking | Sarcastic | haha, ak ak |
| GENKI | Gaming, fun | High energy | !, yeah, yay |
| EXCITED | Gifts, donations | Enthusiastic | !, thank you |
| COMFORT | Sad, stressed | Soothing | ..., nhe, co |
| SERIOUS | Science, knowledge | Professional | (none) |

## Security Layers

### Layer 1: Input Boundary Check
- Max 120 characters
- Max 25 words
- Prevent DoS/spam attacks

### Layer 2: Blacklist Substring Match
- Filter political content
- Filter religious extremism
- Filter adult content
- Filter violence/harm

### Layer 3: Anti-Jailbreak Protection
- Detect special characters: [ ] { } < > / \\ 
- Detect manipulation keywords
- Auto-tag as TROLL if detected

## Text-Voice Anti-Desync Protocol

### Rule 1: Linear Semantic Monotony
- Prevent sudden emotion changes within sentences
- Force sentence breaks with periods

### Rule 2: Clause-by-Clause Streaming
- Split text into 8-12 word chunks
- Stream audio in real-time
- Reduce latency from 3s to <400ms

### Rule 3: Anti-Stall Structural
- Prohibit: lists, tables, code blocks
- Prevent phoneme decoder stalling

### Rule 4: Word-Level Lip-Sync
- Extract word timestamps
- Sync Live2D mouth movements
- Prevent visual glitches

## Configuration

### Environment Variables

Create `.env` file:

```
PORT=3000
TTS_API_KEY=your_api_key
TTS_PROVIDER=google
DATABASE_PATH=bekai_history.db
DATABASE_MAX_SIZE_MB=30
```

## Database Schema

### stream_logs Table

```sql
CREATE TABLE stream_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    emotion_tag TEXT NOT NULL,
    content TEXT NOT NULL,
    user_name TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timestamp ON stream_logs(timestamp);
```

## Performance Metrics

- **Input Queue**: Up to 1000 items
- **Output Queue**: Up to 500 items
- **Cooldown Period**: 2.5 seconds (prevent audio collision)
- **Local LLM Latency**: < 200ms
- **TTS Generation**: ~400ms
- **Total Latency**: ~500-600ms
- **Database Cleanup**: Automatic at 30MB

## Troubleshooting

### Queue Full Error

Reduce input rate or increase queue size:

```python
self.input_queue = asyncio.Queue(maxsize=2000)
```

### TTS Generation Slow

Enable caching or switch to faster provider:

```javascript
const ttsClient = new TTSClient(apiKey, 'elevenlabs');
```

### Database Growing Too Fast

Reduce cleanup threshold:

```python
max_size_mb = 15  # Instead of 30
```

## License

MIT

## Support

For issues and questions, open a GitHub issue.
