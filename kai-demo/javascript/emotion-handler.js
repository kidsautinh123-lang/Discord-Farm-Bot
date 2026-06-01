/**
 * Emotion Handler - Quan ly cam xuc
 */

const EMOTION_MATRIX = {
  'CUTE': {
    keywords: ['khen ngoi', 'chuc', 'dep', 'xinh', 'tot'],
    buffer: ['nha', 'ne', 'um', 'em'],
    style: 'ngot ngao',
    emoji: '😊'
  },
  'YANDERE': {
    keywords: ['yeu', 'co chi', 'the', 'hen'],
    buffer: ['...', 'hm', 'tsk'],
    style: 'chiem huu',
    emoji: '😍'
  },
  'TSUNDERE': {
    keywords: ['trau', 'day', 'thua', 'that'],
    buffer: ['hu', 'xi', 'che'],
    style: 'kieu ky',
    emoji: '😤'
  },
  'TROLL': {
    keywords: ['xoay', 'bat be', 'hack', 'trolling'],
    buffer: ['aa a', 'leu leu', 'haha', 'ak ak'],
    style: 'ca khia',
    emoji: '😏'
  },
  'GENKI': {
    keywords: ['game', 'choi', 'vui', 'thao tac'],
    buffer: ['!', 'yeah', 'yay'],
    style: 'nang luong cao',
    emoji: '😄'
  },
  'EXCITED': {
    keywords: ['gift', 'tien', 'donate', 'cam on'],
    buffer: ['!', 'yeah', 'thank you'],
    style: 'reo ho',
    emoji: '🎉',
    priority: 1
  },
  'COMFORT': {
    keywords: ['buon', 'ap luc', 'tham suy', 'kho'],
    buffer: ['...', 'nhe', 'co'],
    style: 'tram am',
    emoji: '🤗'
  },
  'SERIOUS': {
    keywords: ['khoa hoc', 'hoc thuat', 'kien thuc', 'song'],
    buffer: [],
    style: 'nghiem tuc',
    emoji: '🤔'
  }
};

/**
 * Tag emotion based on payload
 */
async function tagEmotion(payload, messageType = 'chat') {
  const payloadLower = payload.toLowerCase();
  
  // EXCITED priority for gifts
  if (messageType === 'gift') {
    return '[EXCITED]';
  }
  
  // Check keywords
  for (const [emotion, config] of Object.entries(EMOTION_MATRIX)) {
    for (const keyword of config.keywords) {
      if (payloadLower.includes(keyword)) {
        return `[${emotion}]`;
      }
    }
  }
  
  // Default to TROLL
  return '[TROLL]';
}

/**
 * Get buffer words for emotion
 */
function getBufferWords(emotion) {
  const cleanEmotion = emotion.replace(/[\[\]]/g, '');
  return EMOTION_MATRIX[cleanEmotion]?.buffer || [];
}

/**
 * Get emotion matrix
 */
function getEmotionMatrix() {
  return EMOTION_MATRIX;
}

module.exports = {
  tagEmotion,
  getBufferWords,
  getEmotionMatrix,
  EMOTION_MATRIX
};
