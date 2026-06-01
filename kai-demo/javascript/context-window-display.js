/**
 * Context Window Component - Hien thi context learning
 */

class ContextWindowDisplay {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
  }

  /**
   * Display user context
   */
  displayUserContext(userSummary) {
    const html = `
      <div class="context-window">
        <h3>User Profile: ${userSummary.user_name}</h3>
        
        <div class="context-stats">
          <div class="stat-item">
            <label>Total Interactions:</label>
            <value>${userSummary.total_interactions}</value>
          </div>
          
          <div class="stat-item">
            <label>Favorite Emotion:</label>
            <value class="emotion-badge">${userSummary.favorite_emotion || 'N/A'}</value>
          </div>
          
          <div class="stat-item">
            <label>Preferred Platform:</label>
            <value>${userSummary.preferred_platform || 'N/A'}</value>
          </div>
        </div>
        
        <div class="keywords-section">
          <h4>Top Keywords</h4>
          <div class="keyword-cloud">
            ${(userSummary.top_keywords || []).map(
              (keyword, index) => `
                <span class="keyword" style="font-size: ${12 + index * 2}px;">
                  ${keyword}
                </span>
              `
            ).join('')}
          </div>
        </div>
        
        ${userSummary.last_interaction ? `
          <div class="last-interaction">
            <h4>Last Interaction</h4>
            <p><strong>User:</strong> ${userSummary.last_interaction.user_name}</p>
            <p><strong>Message:</strong> ${userSummary.last_interaction.payload.substring(0, 100)}...</p>
            <p><strong>Emotion:</strong> ${userSummary.last_interaction.emotion_tag}</p>
          </div>
        ` : ''}
      </div>
    `;
    
    this.container.innerHTML = html;
    this._attachStyles();
  }

  /**
   * Attach styles
   */
  _attachStyles() {
    if (document.getElementById('context-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'context-styles';
    style.textContent = `
      .context-window {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
      }
      
      .context-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin: 20px 0;
      }
      
      .stat-item {
        display: flex;
        flex-direction: column;
        gap: 5px;
      }
      
      .stat-item label {
        font-size: 12px;
        color: #999;
        text-transform: uppercase;
      }
      
      .stat-item value {
        font-size: 18px;
        font-weight: bold;
        color: #333;
      }
      
      .emotion-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        max-width: fit-content;
      }
      
      .keywords-section {
        margin: 20px 0;
      }
      
      .keyword-cloud {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
      }
      
      .keyword {
        background: #f0f0f0;
        padding: 5px 10px;
        border-radius: 5px;
        color: #666;
        cursor: pointer;
        transition: all 0.2s ease;
      }
      
      .keyword:hover {
        background: #667eea;
        color: white;
      }
      
      .last-interaction {
        background: #f9f9f9;
        border-left: 4px solid #667eea;
        padding: 15px;
        margin-top: 20px;
      }
      
      .last-interaction p {
        margin: 8px 0;
        font-size: 14px;
      }
    `;
    
    document.head.appendChild(style);
  }
}

module.exports = { ContextWindowDisplay };
