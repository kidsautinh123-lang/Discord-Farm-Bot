/**
 * Queue Manager - Quan ly hang doi
 */

class QueueManager {
  constructor(maxSize = 1000) {
    this.queue = [];
    this.maxSize = maxSize;
    this.cooldown = 2500; // 2.5 seconds
    this.lastOutputTime = 0;
  }

  /**
   * Add item to queue
   */
  async enqueue(data) {
    if (this.queue.length >= this.maxSize) {
      throw new Error('Queue is full');
    }
    
    this.queue.push({
      ...data,
      enqueueTime: Date.now(),
      id: `${Date.now()}_${Math.random()}`
    });
    
    return { success: true, queueSize: this.queue.length };
  }

  /**
   * Remove item from queue (FIFO)
   */
  async dequeue() {
    if (this.queue.length === 0) {
      return null;
    }
    
    // Check cooldown
    const elapsed = Date.now() - this.lastOutputTime;
    if (elapsed < this.cooldown) {
      await new Promise(resolve => 
        setTimeout(resolve, this.cooldown - elapsed)
      );
    }
    
    this.lastOutputTime = Date.now();
    return this.queue.shift();
  }

  /**
   * Peek at next item without removing
   */
  peek() {
    return this.queue[0] || null;
  }

  /**
   * Get queue size
   */
  size() {
    return this.queue.length;
  }

  /**
   * Get queue status
   */
  getStatus() {
    return {
      size: this.queue.length,
      maxSize: this.maxSize,
      isFull: this.queue.length >= this.maxSize,
      isEmpty: this.queue.length === 0,
      items: this.queue.map(item => ({
        id: item.id,
        platform: item.platform,
        payloadPreview: item.payload.substring(0, 50),
        enqueueTime: item.enqueueTime
      }))
    };
  }

  /**
   * Clear entire queue
   */
  clear() {
    const count = this.queue.length;
    this.queue = [];
    return { cleared: count };
  }
}

module.exports = { QueueManager };
