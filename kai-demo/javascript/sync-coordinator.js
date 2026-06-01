/**
 * Sync Coordinator - Dieu phoi dong bo van ban va giong noi
 */

class SyncCoordinator {
  constructor() {
    this.maxClauseLength = 12;
    this.minClauseLength = 4;
    this.delimiters = ['.', ',', '!', '?', '...'];
  }

  /**
   * Coordinate sync between text and voice
   */
  async coordinateSync(text, emotionTag) {
    // Step 1: Enforce linear semantics
    text = this._enforceLinearSemantics(text, emotionTag);
    
    // Step 2: Create chunks
    const chunks = this._createChunks(text);
    
    // Step 3: Remove prohibited structures
    const cleanedChunks = this._removeProhibitedStructures(chunks);
    
    // Step 4: Add lip-sync data
    const syncChunks = this._addLipSyncData(cleanedChunks);
    
    return {
      text,
      chunks: syncChunks,
      totalDuration: syncChunks[syncChunks.length - 1]?.endTime || 0,
      emotion: emotionTag
    };
  }

  /**
   * Enforce linear semantics
   */
  _enforceLinearSemantics(text, emotionTag) {
    const sentences = text.split(/(?<=[.!?])\s+/);
    const processed = [];
    
    for (const sentence of sentences) {
      const words = sentence.split(/\s+/);
      
      if (words.length > 15) {
        // Split into 2 sentences
        const mid = Math.floor(words.length / 2);
        const first = words.slice(0, mid).join(' ') + '.';
        const second = words.slice(mid).join(' ') + '.';
        processed.push(first, second);
      } else {
        processed.push(sentence);
      }
    }
    
    return processed.join(' ');
  }

  /**
   * Create chunks by clause
   */
  _createChunks(text) {
    const chunks = [];
    let currentChunk = '';
    let wordCount = 0;
    
    const words = text.split(/\s+/);
    
    for (const word of words) {
      currentChunk += word + ' ';
      wordCount++;
      
      const hasDelimiter = this.delimiters.some(delim => word.includes(delim));
      
      if (hasDelimiter || wordCount >= this.maxClauseLength) {
        if (wordCount >= this.minClauseLength) {
          chunks.push({
            text: currentChunk.trim(),
            wordCount,
            durationMs: wordCount * 100
          });
          currentChunk = '';
          wordCount = 0;
        }
      }
    }
    
    if (currentChunk.trim()) {
      chunks.push({
        text: currentChunk.trim(),
        wordCount,
        durationMs: wordCount * 100
      });
    }
    
    return chunks;
  }

  /**
   * Remove prohibited structures
   */
  _removeProhibitedStructures(chunks) {
    const prohibitedPatterns = [
      /^\s*[-*+]/,
      /^\s*\d+\./,
      /```/,
      /\[\[.*\]\]/,
      /\{\{.*\}\}/
    ];
    
    return chunks.filter(chunk => {
      return !prohibitedPatterns.some(pattern => pattern.test(chunk.text));
    });
  }

  /**
   * Add lip-sync timing data
   */
  _addLipSyncData(chunks) {
    let cumulativeTime = 0;
    
    return chunks.map(chunk => {
      chunk.startTime = cumulativeTime;
      chunk.endTime = cumulativeTime + chunk.durationMs;
      
      // Word-level timestamps
      const words = chunk.text.split(/\s+/);
      const wordDuration = chunk.durationMs / words.length;
      
      chunk.wordTimestamps = words.map((word, i) => ({
        word,
        startMs: cumulativeTime + (i * wordDuration),
        endMs: cumulativeTime + ((i + 1) * wordDuration)
      }));
      
      cumulativeTime = chunk.endTime;
      
      return chunk;
    });
  }
}

module.exports = new SyncCoordinator();
