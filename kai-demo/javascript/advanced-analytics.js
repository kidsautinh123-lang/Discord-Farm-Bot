/**
 * Advanced Analytics - Phan tich chi tiet
 */

class AdvancedAnalytics {
  constructor() {
    this.data = [];
    this.userStats = {};
  }

  /**
   * Add analytics event
   */
  trackEvent(event) {
    this.data.push({
      ...event,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * Get user analytics
   */
  getUserAnalytics(userName) {
    if (!this.userStats[userName]) {
      this.userStats[userName] = {
        total_interactions: 0,
        favorite_emotion: null,
        platforms: {},
        response_times: [],
        emotions: {}
      };
    }
    
    return this.userStats[userName];
  }

  /**
   * Update user analytics
   */
  updateUserAnalytics(userName, event) {
    const stats = this.getUserAnalytics(userName);
    
    stats.total_interactions += 1;
    
    // Update emotion
    if (!stats.emotions[event.emotion]) {
      stats.emotions[event.emotion] = 0;
    }
    stats.emotions[event.emotion] += 1;
    
    // Update favorite emotion
    const maxEmotion = Object.entries(stats.emotions)
      .sort(([, a], [, b]) => b - a)[0];
    stats.favorite_emotion = maxEmotion ? maxEmotion[0] : null;
    
    // Track platform
    if (!stats.platforms[event.platform]) {
      stats.platforms[event.platform] = 0;
    }
    stats.platforms[event.platform] += 1;
    
    // Track response time
    if (event.latency_ms) {
      stats.response_times.push(event.latency_ms);
    }
  }

  /**
   * Get statistics
   */
  getStatistics() {
    const totalEvents = this.data.length;
    const avgLatency = this.data.length > 0
      ? this.data.reduce((sum, e) => sum + (e.latency_ms || 0), 0) / totalEvents
      : 0;
    
    const emotionDistribution = {};
    this.data.forEach(e => {
      emotionDistribution[e.emotion] = (emotionDistribution[e.emotion] || 0) + 1;
    });
    
    return {
      totalEvents,
      avgLatency: avgLatency.toFixed(2),
      uniqueUsers: Object.keys(this.userStats).length,
      emotionDistribution,
      userStats: this.userStats
    };
  }

  /**
   * Generate report
   */
  generateReport() {
    const stats = this.getStatistics();
    
    const report = `
=== KAI DEMO ANALYTICS REPORT ===

Total Events: ${stats.totalEvents}
Average Latency: ${stats.avgLatency}ms
Unique Users: ${stats.uniqueUsers}

Emotion Distribution:
${Object.entries(stats.emotionDistribution)
  .map(([emotion, count]) => `  ${emotion}: ${count}`)
  .join('\n')}

Top Users:
${Object.entries(stats.userStats)
  .sort(([, a], [, b]) => b.total_interactions - a.total_interactions)
  .slice(0, 5)
  .map(([user, data]) => 
    `  ${user}: ${data.total_interactions} interactions (Favorite: ${data.favorite_emotion})`
  )
  .join('\n')}
    `;
    
    return report;
  }
}

module.exports = { AdvancedAnalytics };
