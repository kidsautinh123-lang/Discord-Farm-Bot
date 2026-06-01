/**
 * Simple Logger
 */

const fs = require('fs');
const path = require('path');

const logDir = path.join(__dirname, '../../logs');
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

const logFile = path.join(logDir, `app_${new Date().toISOString().split('T')[0]}.log`);

function log(level, message) {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] [${level}] ${message}\n`;
  
  console.log(logMessage.trim());
  fs.appendFileSync(logFile, logMessage);
}

module.exports = {
  info: (msg) => log('INFO', msg),
  error: (msg) => log('ERROR', msg),
  warn: (msg) => log('WARN', msg),
  debug: (msg) => log('DEBUG', msg)
};
