/**
 * Multi-LLM Display Component - Hien thi phan hoi tu nhieu LLM
 */

class MultiLLMDisplay {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.responses = [];
  }

  /**
   * Display all LLM responses
   */
  displayResponses(data) {
    this.responses = data.all_provider_responses || [];
    
    const html = `
      <div class="multi-llm-container">
        <div class="best-response">
          <h3>Best Response (${data.provider})</h3>
          <div class="response-content">
            <span class="emotion-tag">${data.emotion}</span>
            <p>${data.response}</p>
            <div class="metrics">
              <span class="latency">⏱️ ${data.latency_ms.toFixed(0)}ms</span>
              <span class="quality">⭐ ${(data.quality_score * 100).toFixed(0)}%</span>
              <span class="consensus">🤝 ${(data.consensus * 100).toFixed(0)}% consensus</span>
            </div>
          </div>
        </div>
        
        <div class="all-responses">
          <h3>All Provider Responses</h3>
          <div class="response-grid">
            ${this.responses.map(resp => this._createResponseCard(resp)).join('')}
          </div>
        </div>
      </div>
    `;
    
    this.container.innerHTML = html;
    this._attachStyles();
  }

  /**
   * Create response card for each provider
   */
  _createResponseCard(response) {
    const statusClass = response.error ? 'error' : 'success';
    
    return `
      <div class="response-card ${statusClass}">
        <h4>${response.provider}</h4>
        <div class="response-body">
          ${response.error 
            ? `<p class="error-text">❌ ${response.error}</p>`
            : `
              <p class="response-text">${response.content}</p>
              <div class="response-metrics">
                <span>🕐 ${response.latency_ms.toFixed(0)}ms</span>
                <span>⭐ ${(response.quality * 100).toFixed(0)}%</span>
              </div>
            `
          }
        </div>
      </div>
    `;
  }

  /**
   * Attach styles
   */
  _attachStyles() {
    if (document.getElementById('multi-llm-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'multi-llm-styles';
    style.textContent = `
      .multi-llm-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
        font-family: Arial, sans-serif;
      }
      
      .best-response {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
      }
      
      .response-content {
        margin-top: 10px;
      }
      
      .emotion-tag {
        display: inline-block;
        background: rgba(255,255,255,0.3);
        padding: 5px 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        font-weight: bold;
      }
      
      .metrics {
        display: flex;
        gap: 15px;
        margin-top: 15px;
        font-size: 14px;
        opacity: 0.9;
      }
      
      .all-responses {
        padding: 20px;
        background: #f5f5f5;
        border-radius: 10px;
      }
      
      .response-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 15px;
        margin-top: 15px;
      }
      
      .response-card {
        background: white;
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        transition: all 0.3s ease;
      }
      
      .response-card.success {
        border-color: #4CAF50;
      }
      
      .response-card.error {
        border-color: #f44336;
        opacity: 0.7;
      }
      
      .response-card:hover {
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transform: translateY(-2px);
      }
      
      .response-card h4 {
        margin: 0 0 10px 0;
        color: #333;
      }
      
      .response-text {
        font-size: 14px;
        line-height: 1.5;
        color: #666;
        margin: 10px 0;
      }
      
      .error-text {
        color: #f44336;
        font-weight: bold;
      }
      
      .response-metrics {
        display: flex;
        gap: 10px;
        font-size: 12px;
        margin-top: 10px;
        color: #999;
      }
    `;
    
    document.head.appendChild(style);
  }
}

/**
 * Performance Monitor - Theo doi hieu nang
 */
class PerformanceMonitor {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.data = [];
  }

  /**
   * Update performance metrics
   */
  updateMetrics(metrics) {
    const html = `
      <div class="performance-dashboard">
        <div class="metric-card">
          <h4>Total Requests</h4>
          <p class="metric-value">${metrics.total_requests}</p>
        </div>
        
        <div class="metric-card">
          <h4>Average Latency</h4>
          <p class="metric-value">${metrics.average_latency_ms.toFixed(0)}ms</p>
        </div>
        
        <div class="metric-card">
          <h4>Active Users</h4>
          <p class="metric-value">${metrics.total_users}</p>
        </div>
        
        <div class="metric-card">
          <h4>Emotional Distribution</h4>
          <div class="emotion-dist">
            ${Object.entries(metrics.emotional_distribution).map(
              ([emotion, count]) => `
                <div class="emotion-item">
                  <span>${emotion}</span>
                  <span class="count">${count}</span>
                </div>
              `
            ).join('')}
          </div>
        </div>
      </div>
    `;
    
    this.container.innerHTML = html;
    this._attachStyles();
  }

  /**
   * Attach styles
   */
  _attachStyles() {
    if (document.getElementById('performance-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'performance-styles';
    style.textContent = `
      .performance-dashboard {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        padding: 20px;
      }
      
      .metric-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
      }
      
      .metric-card h4 {
        margin: 0 0 10px 0;
        color: #666;
        font-size: 14px;
      }
      
      .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #667eea;
        margin: 0;
      }
      
      .emotion-dist {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 10px;
      }
      
      .emotion-item {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        color: #666;
      }
      
      .count {
        font-weight: bold;
        color: #764ba2;
      }
    `;
    
    document.head.appendChild(style);
  }
}

module.exports = { MultiLLMDisplay, PerformanceMonitor };
