/**
 * Real-Time Dashboard - Interactive analytics dashboard
 */

const chartLibrary = require('chart.js');

class RealTimeDashboard {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.charts = {};
    this.metrics = {};
  }

  /**
   * Initialize dashboard
   */
  initializeDashboard() {
    const html = `
      <div class="dashboard-container">
        <div class="dashboard-header">
          <h1>KAI Demo - Real-Time Analytics</h1>
          <div class="header-metrics">
            <div class="metric-box">
              <span class="metric-label">Active Users</span>
              <span class="metric-value" id="active-users">0</span>
            </div>
            <div class="metric-box">
              <span class="metric-label">Requests/min</span>
              <span class="metric-value" id="requests-per-min">0</span>
            </div>
            <div class="metric-box">
              <span class="metric-label">Avg Latency</span>
              <span class="metric-value" id="avg-latency">0ms</span>
            </div>
          </div>
        </div>
        
        <div class="dashboard-grid">
          <div class="chart-container">
            <h3>Request Trends (24h)</h3>
            <canvas id="request-chart"></canvas>
          </div>
          
          <div class="chart-container">
            <h3>Emotion Distribution</h3>
            <canvas id="emotion-chart"></canvas>
          </div>
          
          <div class="chart-container">
            <h3>Latency Distribution</h3>
            <canvas id="latency-chart"></canvas>
          </div>
          
          <div class="chart-container">
            <h3>User Activity</h3>
            <canvas id="user-activity-chart"></canvas>
          </div>
        </div>
        
        <div class="recent-events">
          <h3>Recent Events</h3>
          <div id="events-list" class="events-list"></div>
        </div>
      </div>
    `;
    
    this.container.innerHTML = html;
    this._attachStyles();
    this._initializeCharts();
  }

  /**
   * Initialize charts
   */
  _initializeCharts() {
    const ctx1 = document.getElementById('request-chart').getContext('2d');
    const ctx2 = document.getElementById('emotion-chart').getContext('2d');
    const ctx3 = document.getElementById('latency-chart').getContext('2d');
    const ctx4 = document.getElementById('user-activity-chart').getContext('2d');
    
    // Request trend chart
    this.charts.requests = new Chart(ctx1, {
      type: 'line',
      data: {
        labels: this._generateLabels(24),
        datasets: [{
          label: 'Requests',
          data: Array(24).fill(0),
          borderColor: '#667eea',
          backgroundColor: 'rgba(102, 126, 234, 0.1)',
          tension: 0.4
        }]
      },
      options: { responsive: true, maintainAspectRatio: true }
    });
    
    // Emotion distribution chart
    this.charts.emotions = new Chart(ctx2, {
      type: 'doughnut',
      data: {
        labels: ['CUTE', 'YANDERE', 'TSUNDERE', 'TROLL', 'GENKI', 'EXCITED', 'COMFORT', 'SERIOUS'],
        datasets: [{
          data: Array(8).fill(0),
          backgroundColor: [
            '#ff6b6b', '#ee5a6f', '#f06595', '#d63384',
            '#b197fc', '#748ffc', '#5c7cfa', '#339af0'
          ]
        }]
      },
      options: { responsive: true, maintainAspectRatio: true }
    });
    
    // Latency distribution chart
    this.charts.latency = new Chart(ctx3, {
      type: 'bar',
      data: {
        labels: ['<500ms', '500-1s', '1-2s', '2-3s', '>3s'],
        datasets: [{
          label: 'Requests',
          data: Array(5).fill(0),
          backgroundColor: '#667eea'
        }]
      },
      options: { responsive: true, maintainAspectRatio: true }
    });
    
    // User activity chart
    this.charts.userActivity = new Chart(ctx4, {
      type: 'bar',
      data: {
        labels: this._generateLabels(7),
        datasets: [{
          label: 'Active Users',
          data: Array(7).fill(0),
          backgroundColor: '#764ba2'
        }]
      },
      options: { responsive: true, maintainAspectRatio: true }
    });
  }

  /**
   * Update dashboard with real-time data
   */
  updateMetrics(data) {
    // Update header metrics
    document.getElementById('active-users').textContent = data.active_users || 0;
    document.getElementById('requests-per-min').textContent = data.requests_per_min || 0;
    document.getElementById('avg-latency').textContent = 
      `${(data.avg_latency || 0).toFixed(0)}ms`;
    
    // Update request trend
    this.charts.requests.data.datasets[0].data.push(data.requests || 0);
    if (this.charts.requests.data.datasets[0].data.length > 24) {
      this.charts.requests.data.datasets[0].data.shift();
    }
    this.charts.requests.update();
    
    // Update emotion distribution
    const emotionData = data.emotion_distribution || {};
    const emotions = ['CUTE', 'YANDERE', 'TSUNDERE', 'TROLL', 'GENKI', 'EXCITED', 'COMFORT', 'SERIOUS'];
    this.charts.emotions.data.datasets[0].data = emotions.map(e => emotionData[e] || 0);
    this.charts.emotions.update();
  }

  /**
   * Add event to recent events list
   */
  addEvent(event) {
    const eventsList = document.getElementById('events-list');
    
    const eventHTML = `
      <div class="event-item">
        <span class="event-time">${new Date().toLocaleTimeString()}</span>
        <span class="event-user">${event.user_name || 'Unknown'}</span>
        <span class="event-action">${event.action || 'Request'}</span>
        <span class="event-emotion">${event.emotion || 'N/A'}</span>
      </div>
    `;
    
    eventsList.insertAdjacentHTML('afterbegin', eventHTML);
    
    // Keep only last 20 events
    while (eventsList.children.length > 20) {
      eventsList.removeChild(eventsList.lastChild);
    }
  }

  /**
   * Generate time labels
   */
  _generateLabels(count) {
    const labels = [];
    for (let i = count - 1; i >= 0; i--) {
      const date = new Date();
      date.setHours(date.getHours() - i);
      labels.push(date.toLocaleTimeString());
    }
    return labels;
  }

  /**
   * Attach styles
   */
  _attachStyles() {
    if (document.getElementById('dashboard-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'dashboard-styles';
    style.textContent = `
      .dashboard-container {
        padding: 20px;
        background: #f5f5f5;
        min-height: 100vh;
      }
      
      .dashboard-header {
        margin-bottom: 30px;
      }
      
      .dashboard-header h1 {
        margin: 0 0 20px 0;
        color: #333;
      }
      
      .header-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
      }
      
      .metric-box {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      }
      
      .metric-label {
        display: block;
        font-size: 12px;
        color: #999;
        text-transform: uppercase;
        margin-bottom: 5px;
      }
      
      .metric-value {
        display: block;
        font-size: 24px;
        font-weight: bold;
        color: #667eea;
      }
      
      .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
      }
      
      .chart-container {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      }
      
      .chart-container h3 {
        margin-top: 0;
        color: #333;
      }
      
      .recent-events {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      }
      
      .events-list {
        max-height: 300px;
        overflow-y: auto;
      }
      
      .event-item {
        display: flex;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid #eee;
        font-size: 14px;
      }
      
      .event-time {
        color: #999;
        min-width: 100px;
      }
      
      .event-user {
        font-weight: bold;
        color: #333;
      }
      
      .event-action {
        color: #667eea;
      }
      
      .event-emotion {
        background: #f0f0f0;
        padding: 2px 8px;
        border-radius: 3px;
        color: #666;
      }
    `;
    
    document.head.appendChild(style);
  }
}

module.exports = { RealTimeDashboard };
