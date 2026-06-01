# KAI System

**Hệ thống Text-to-Speech Nâng cao với Phân tích Cảm xúc và Giao thức Chống Mất đồng bộ**

![Trạng thái](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Node.js](https://img.shields.io/badge/node.js-14%2B-green)

## 🎯 Tổng quan

KAI (Kai Artificial Intelligence) là một hệ thống tinh vi, đa nền tảng xử lý đầu vào từ TikTok, YouTube và các nền tảng khác, áp dụng trí thông minh cảm xúc và tạo ra các phản hồi phù hợp với ngữ cảnh cùng với đồng bộ hóa text-to-speech nâng cao.

### Khả năng chính
- 🎬 **Đầu vào Đa nền tảng** - TikTok, YouTube và các nguồn tùy chỉnh
- 🧠 **Ma trận Cảm xúc** - 8 trạng thái cảm xúc với phản hồi theo ngữ cảnh
- 🔐 **3 Lớp Bảo mật** - Kiểm tra đầu vào, lọc danh sách đen, bảo vệ chống jailbreak
- 🎙️ **TTS do AI điều khiển** - Đọc văn bản có cảm xúc tự nhiên
- ⚡ **Xử lý Thời gian thực** - <600ms từ đầu vào đến đầu ra âm thanh
- 🛡️ **Giao thức Chống Mất đồng bộ** - Đồng bộ hóa hoàn hảo giữa text và voice
- 💾 **Bộ nhớ SQLite** - Lưu trữ ngữ cảnh với dọn dẹp tự động
- 🔄 **Định tuyến LLM Lai** - Xử lý địa phương (nhanh) vs Đám mây (thông minh)

## 📊 Kiến trúc hệ thống

```
Đầu vào từ người dùng (TikTok/YouTube)
    ↓
[Lọc bảo mật - 3 lớp]
    ↓
[Gắn thẻ cảm xúc - 8 trạng thái]
    ↓
[Định tuyến LLM - Địa phương/Đám mây]
    ↓
[Tạo phản hồi]
    ↓
[Xử lý TTS - Chuẩn hóa]
    ↓
[Giao thức Chống mất đồng bộ]
    ↓
[Đầu ra âm thanh + Dữ liệu đồng bộ]
```

## ✨ Tính năng

| Tính năng | Mô tả |
|----------|-------|
| 🎭 **Ma trận Cảm xúc** | CUTE (Dễ thương), YANDERE (Yêu thương chiếm hữu), TSUNDERE (Tsundere), TROLL (Chế giễu), GENKI (Năng lượng), EXCITED (H興奮), COMFORT (An ủi), SERIOUS (Nghiêm túc) |
| 🛡️ **Lọc bảo mật** | Giới hạn 120 ký tự, tối đa 25 từ, quét danh sách đen, phát hiện jailbreak |
| 🧠 **Định tuyến thông minh** | Tự động định tuyến giữa LLM địa phương (nhanh) và đám mây (thông minh) |
| 🎵 **Tối ưu hóa TTS** | Xóa emoji, ánh xạ viết tắt, kiểm soát dấu câu |
| 📡 **API Thời gian thực** | Express + Socket.IO cho phát trực tiếp và cập nhật websocket |
| 📊 **Phân tích** | Giám sát hàng đợi, phân phối cảm xúc, theo dõi độ trễ |
| 🔄 **Quản lý Cooldown** | Giao thức chống va chạm 2.5s để ngăn chặn chồng lấp âm thanh |

## 🚀 Cài đặt

### Yêu cầu trước
- Python 3.8+
- Node.js 14+
- npm hoặc yarn

### Cài đặt Python

```bash
pip install -r requirements.txt
```

**Các thư viện cần thiết:**
```
asyncio
python-dotenv
pyyaml
requests
aiohttp
python-socketio
sqlite3
```

### Cài đặt Node.js

```bash
npm install
```

**Các thư viện cần thiết:**
```
express: ^4.18.2
socket.io: ^4.5.4
cors: ^2.8.5
body-parser: ^1.20.2
axios: ^1.3.0
nodemon: ^2.0.20 (dev)
jest: ^29.3.1 (dev)
```

## 🎮 Bắt đầu nhanh

### 1. Khởi động Server Express

```bash
npm start
```

Server sẽ chạy tại `http://localhost:3000`

### 2. Khởi động Hệ thống Python (trong terminal khác)

```bash
python python/main.py
```

### 3. Kiểm tra Hệ thống

```bash
# Kiểm tra sức khỏe
curl http://localhost:3000/health

# Thêm đầu vào
curl -X POST http://localhost:3000/api/input \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "TikTok",
    "user_raw_name": "user123",
    "payload": "Em yeu anh rat nhieu nha",
    "type": "chat"
  }'

# Kiểm tra trạng thái hàng đợi
curl http://localhost:3000/api/queue-status

# Lấy thẻ cảm xúc
curl http://localhost:3000/api/emotions

# Kiểm tra TTS
curl -X POST http://localhost:3000/api/test-tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Em yeu anh",
    "emotion": "[YANDERE]"
  }'
```

## 📚 Tài liệu API

### Các điểm cuối HTTP

#### Kiểm tra Sức khỏe
```
GET /health
Phản hồi: { status: "ok", timestamp: "2024-01-01T00:00:00.000Z" }
```

#### Thêm Đầu vào vào Hàng đợi
```
POST /api/input
Content-Type: application/json

Nội dung:
{
  "platform": "TikTok",          // Bắt buộc: TikTok, YouTube, v.v.
  "user_raw_name": "user123",    // Định danh người dùng
  "payload": "Em yeu anh",       // Văn bản đầu vào (tối đa 120 ký tự)
  "type": "chat"                 // Loại tin nhắn
}

Phản hồi: { success: true, message: "Dữ liệu được thêm vào hàng đợi" }
```

#### Trạng thái Hàng đợi
```
GET /api/queue-status
Phản hồi: {
  "input_queue_size": 5,
  "output_queue_size": 2,
  "total_processed": 152
}
```

#### Lấy Thẻ Cảm xúc
```
GET /api/emotions
Phản hồi: [
  { tag: "[CUTE]", trigger: "Lợi, khen ngợi", style: "Tính cách ngọt ngào" },
  ...
]
```

#### Kiểm tra TTS
```
POST /api/test-tts
Content-Type: application/json

Nội dung:
{
  "text": "Em yeu anh",
  "emotion": "[YANDERE]"
}

Phản hồi: { success: true, audioUrl: "https://..." }
```

### Sự kiện WebSocket (Socket.IO)

#### Kết nối & Đăng ký
```javascript
const socket = io('http://localhost:3000');

// Đăng ký cập nhật trực tiếp
socket.emit('subscribe-updates');
```

#### Thêm Đầu vào qua Socket
```javascript
socket.emit('add-input', {
  platform: 'TikTok',
  user_raw_name: 'user123',
  payload: 'Em yeu anh',
  type: 'chat'
});
```

#### Lắng nghe Đầu ra
```javascript
socket.on('output', (data) => {
  console.log('Cảm xúc:', data.emotion_tag);
  console.log('Văn bản:', data.text);
  console.log('URL âm thanh:', data.audio_url);
  console.log('Dữ liệu đồng bộ:', data.sync_data);
});

socket.on('queue-updated', (data) => {
  console.log('Kích thước hàng đợi:', data.size);
});
```

#### Xử lý Lỗi
```javascript
socket.on('error', (data) => {
  console.error('Lỗi:', data.message);
});
```

## 🧠 Chi tiết Ma trận Cảm xúc

| Cảm xúc | Từ khóa Kích hoạt | Phong cách Phản hồi | Từ Buffer | Ví dụ |
|---------|------------------|-------------------|----------|-------|
| **CUTE** | Lợi, khen ngợi | Ngọt ngào, thiên thơ | nha, ne, um | "Cảm ơn bạn tuyệt quá" |
| **YANDERE** | Tỏ tình, ghen tỵ | Chiếm hữu, mãnh liệt | ..., hm, tsk | "Anh chỉ có em là không?" |
| **TSUNDERE** | Chế giễu, khoác lác | Phòng vệ, tsun | hu, xi, che | "K... kém chỉ!" |
| **TROLL** | Trò đùa, yêu cầu vô lý | Mỉa mai, vui vẻ | haha, ak ak | "Hihi ngầu thế" |
| **GENKI** | Game, chủ đề vui | Năng lượng cao | !, yeah, yay | "Yay chơi game cùng em!" |
| **EXCITED** | Quà tặng, đóng góp | Hứng khởi, cảm ơn | !, thank you | "Cảm ơn rất nhiều!" |
| **COMFORT** | Chủ đề buồn, căng thẳng | An ủi, hỗ trợ | ..., nhe, co | "Có em đây, không buồn nha" |
| **SERIOUS** | Khoa học, logic | Chuyên nghiệp, chính thức | (không) | "Đúng, điều này quan trọng" |

## 🔐 Kiến trúc Bảo mật

### Lớp 1: Kiểm tra Ranh giới Đầu vào
- **Độ dài tối đa**: 120 ký tự
- **Từ tối đa**: 25 từ
- **Mục đích**: Ngăn chặn các cuộc tấn công DoS/spam

### Lớp 2: Quét Danh sách Đen bằng cách Khớp Chuỗi con
- **Từ khóa danh sách đen**: Chính trị, tôn giáo, nội dung dành cho người lớn, bạo lực
- **Khớp mẫu**: Tìm kiếm chuỗi con không phân biệt chữ hoa/thường
- **Mục đích**: Lọc nội dung có hại/nhạy cảm

### Lớp 3: Bảo vệ Chống Jailbreak
- **Phát hiện**: Ký tự đặc biệt `[ ] { } < > / \`
- **Phát hiện**: Từ khóa thao túng (ignore, bypass, hack)
- **Hành động**: Tự động gắn thẻ là TROLL nếu phát hiện
- **Mục đích**: Ngăn chặn các cuộc tấn công tiêm nhập lời nhắc

## ⚙️ Giao thức Chống Mất đồng bộ Text-Voice

### Quy tắc 1: Tính đơn điệu Ngữ nghĩa Tuyến tính
- Ngăn chặn thay đổi cảm xúc đột ngột trong câu
- Buộc ngắt câu bằng dấu chấm
- Tối đa 8-12 từ mỗi mệnh đề

### Quy tắc 2: Phát trực tiếp theo Mệnh đề
- Chia văn bản thành khúc 8-12 từ
- Phát âm thanh theo thời gian thực
- Giảm độ trễ từ 3s xuống <400ms

### Quy tắc 3: Cấu trúc Chống Tắc
- Cấm: Danh sách, bảng, khối mã
- Ngăn chặn: Tắc của bộ giải mã âm vị

### Quy tắc 4: Đồng bộ Lip-Sync Cấp độ Từ
- Trích xuất dấu thời gian cấp độ từ
- Đồng bộ hóa chuyển động miệng Live2D
- Ngăn chặn các lỗi hình ảnh

## 📁 Cấu trúc Dự án

```
kai-demo/
├── python/
│   ├── main.py                    # Bộ điều phối hệ thống
│   ├── security_filter.py         # Xác thực bảo mật 3 lớp
│   ├── emotion_tagger.py          # Động cơ phân loại cảm xúc
│   ├── llm_router.py              # Định tuyến LLM Địa phương vs Đám mây
│   ├── advanced_llm_router.py     # Logic định tuyến nâng cao
│   ├── tts_processor.py           # Chuẩn hóa & tối ưu hóa văn bản
│   ├── memory_manager.py          # Quản lý ngữ cảnh SQLite
│   ├── anti_desync.py             # Giao thức đồng bộ text-voice
│   ├── voice_preprocessing.py     # Xử lý trước âm thanh
│   ├── voice_cloning.py           # Chuyển đổi phong cách giọng nói
│   ├── language_processor.py      # Hỗ trợ đa ngôn ngữ
│   ├── sentiment_analyzer.py      # Phân tích cảm xúc
│   ├── context_learning.py        # Học tập theo ngữ cảnh
│   ├── analytics_engine.py        # Phân tích hiệu suất
│   ├── rate_limiting.py           # Quản lý giới hạn tỷ lệ
│   ├── redis_cache.py             # Lớp bộ nhớ đệm Redis
│   ├── realtime_streaming.py      # Phát trực tiếp dữ liệu thời gian thực
│   ├── error_handling.py          # Xử lý lỗi tập trung
│   ├── monitoring.py              # Giám sát hệ thống
│   └── test_suite.py              # Kiểm tra đơn vị & tích hợp
│
├── javascript/
│   ├── server.js                  # Server Express & định tuyến
│   ├── queue-manager.js           # Quản lý hàng đợi đầu vào/đầu ra
│   ├── emotion-handler.js         # Xử lý cảm xúc
│   ├── tts-client.js              # Tích hợp máy khách TTS
│   ├── sync-coordinator.js        # Điều phối đồng bộ
│   ├── logger.js                  # Ghi nhật ký tập trung
│   ├── realtime-dashboard.js      # Bảng điều khiển thời gian thực
│   ├── multi-llm-display.js       # Hiển thị UI LLM đa phương thức
│   ├── context-window-display.js  # Trực quan hóa ngữ cảnh
│   └── advanced-analytics.js      # Hiển thị phân tích nâng cao
│
├── package.json                   # Các thư viện Node.js
├── requirements.txt               # Các thư viện Python
├── .env.example                   # Mẫu biến môi trường
└── README.md
```

## ⚙️ Cấu hình

### Biến Môi trường

Tạo file `.env` trong thư mục gốc:

```env
# Server
PORT=3000
HOST=localhost

# Cấu hình TTS
TTS_API_KEY=your_tts_api_key
TTS_PROVIDER=google          # google, elevenlabs, azure
TTS_VOICE=female
TTS_SPEED=1.0

# Cơ sở dữ liệu
DATABASE_PATH=bekai_history.db
DATABASE_MAX_SIZE_MB=30

# Bộ nhớ đệm
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600

# Cấu hình LLM
LOCAL_LLM_MODEL=local_model
CLOUD_LLM_API_KEY=gemini_api_key
LLM_TIMEOUT=2.0

# Giới hạn Tỷ lệ
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Ghi nhật ký
LOG_LEVEL=INFO
LOG_FILE=kai-system.log

# Bảo mật
MAX_INPUT_LENGTH=120
MAX_WORDS=25
SECURITY_LEVEL=strict
```

## 📊 Chỉ số Hiệu suất

| Chỉ số | Mục tiêu | Trạng thái |
|--------|---------|-----------|
| Dung lượng Hàng đợi Đầu vào | 1000 mục | ✅ |
| Dung lượng Hàng đợi Đầu ra | 500 mục | ✅ |
| Thời gian Lọc bảo mật | <50ms | ✅ |
| Gắn thẻ Cảm xúc | <100ms | ✅ |
| Phản hồi LLM Địa phương | <200ms | ✅ |
| Phản hồi LLM Đám mây | <2000ms | ✅ |
| Tạo TTS | ~400ms | ✅ |
| Độ trễ Tổng cộng | 500-600ms | ✅ |
| Kỳ Cooldown | 2.5 giây | ✅ |
| Dọn dẹp Cơ sở dữ liệu Tự động | Ngưỡng 30MB | ✅ |

## 🐛 Khắc phục Sự cố

### Vấn đề: Lỗi Hàng đợi Đầy

**Triệu chứng:** "Input queue full, dropping data"

**Giải pháp:**
```python
# Trong main.py, tăng kích thước hàng đợi:
self.input_queue = asyncio.Queue(maxsize=2000)
self.output_queue = asyncio.Queue(maxsize=1000)
```

### Vấn đề: Tạo TTS Chậm

**Triệu chứng:** Âm thanh mất >1s để tạo

**Giải pháp:**
```javascript
// Chuyển sang nhà cung cấp TTS nhanh hơn
const ttsClient = new TTSClient(apiKey, 'elevenlabs');
// Kích hoạt bộ nhớ đệm phản hồi
const ttsClient = new TTSClient(apiKey, 'google', { cache: true });
```

### Vấn đề: Cơ sở dữ liệu Phát triển Quá nhanh

**Triệu chứng:** Tệp cơ sở dữ liệu vượt quá ngưỡng

**Giải pháp:**
```python
# Trong memory_manager.py, giảm ngưỡng dọn dẹp:
max_size_mb = 15  # Thay vì 30
cleanup_interval = 300  # Dọn dẹp mỗi 5 phút
```

### Vấn đề: Độ trễ Cao

**Triệu chứng:** Thời gian phản hồi tổng cộng > 1s

**Giải pháp:**
1. Sử dụng LLM Địa phương cho các phản hồi đơn giản
2. Kích hoạt bộ nhớ đệm cho các cụm từ phổ biến
3. Tăng tốc độ xử lý hàng đợi
4. Kiểm tra kết nối bộ nhớ đệm Redis

### Vấn đề: Kết nối WebSocket Không thành công

**Triệu chứng:** Kết nối Socket.IO bị từ chối

**Giải pháp:**
```bash
# Đảm bảo server đang chạy
npm start

# Kiểm tra khả dụng cổng
lsof -i :3000

# Kiểm tra cài đặt CORS trong server.js
const io = socketIO(server, {
  cors: {
    origin: '*',  # Hoặc miền cụ thể
    methods: ['GET', 'POST']
  }
});
```

## 📈 Giám sát & Phân tích

### Bảng điều khiển Thời gian thực

Truy cập bảng điều khiển tại: `http://localhost:3000/dashboard`

**Hiển thị:**
- Kích thước hàng đợi hoạt động
- Phân phối cảm xúc
- Độ trễ trung bình
- Tỷ lệ lỗi
- Thống kê định tuyến LLM
- Hiệu suất nhà cung cấp TTS

### Nhật ký

Kiểm tra nhật ký trong:
```bash
# Đầu ra terminal
npm start

# Tệp nhật ký
tail -f kai-system.log

# Nhật ký Python
python python/main.py 2>&1 | tee py-system.log
```

## 🧪 Kiểm tra

### Chạy Bộ kiểm tra

```bash
# Kiểm tra Python
python python/test_suite.py

# Kiểm tra Node.js
npm test
```

### Kiểm tra Thủ công

```bash
# Kiểm tra gắn thẻ cảm xúc
curl -X POST http://localhost:3000/api/input \
  -d '{"platform":"TikTok","user_raw_name":"test","payload":"Em yeu anh","type":"chat"}'

# Kiểm tra TTS với cảm xúc
curl -X POST http://localhost:3000/api/test-tts \
  -d '{"text":"Em yeu anh","emotion":"[YANDERE]"}'

# Giám sát theo thời gian thực
curl http://localhost:3000/api/queue-status | python -m json.tool
```

## 📚 Các chủ đề Nâng cao

### Thẻ Cảm xúc Tùy chỉnh

Thêm cảm xúc tùy chỉnh trong `emotion_tagger.py`:

```python
CUSTOM_EMOTIONS = {
    '[CUSTOM]': {
        'trigger': ['keywords'],
        'style': 'description',
        'buffer': ['words']
    }
}
```

### Thêm Nhà cung cấp LLM Mới

1. Triển khai trong `llm_router.py`
2. Cập nhật các biến môi trường
3. Thêm xử lý lỗi trong `error_handling.py`
4. Kiểm tra với `test_suite.py`

### Triển khai Nhà cung cấp TTS Tùy chỉnh

1. Tạo adapter trong `tts_processor.py`
2. Triển khai phương pháp tổng hợp giọng nói
3. Thêm giới hạn tỷ lệ trong `rate_limiting.py`
4. Tích hợp bộ nhớ đệm trong `redis_cache.py`

## 🤝 Đóng góp

Chúng tôi hoan nghênh các đóng góp! Vui lòng:

1. Fork repository
2. Tạo branch tính năng (`git checkout -b feature/amazing-feature`)
3. Commit các thay đổi (`git commit -m 'Thêm tính năng tuyệt vời'`)
4. Push đến branch (`git push origin feature/amazing-feature`)
5. Mở Pull Request

## 📄 Giấy phép

MIT License - Xem file LICENSE để biết chi tiết

## 🙏 Lời cảm ơn

- Cộng đồng discord.py
- OpenAI Gemini API
- Cộng đồng Nhà cung cấp TTS
- Các nhà phát triển Socket.IO

## 📞 Hỗ trợ & Phản hồi

- 🐛 [Báo cáo Lỗi](https://github.com/kidsautinh123-lang/Discord-Farm-Bot/issues)
- 💡 [Yêu cầu Tính năng](https://github.com/kidsautinh123-lang/Discord-Farm-Bot/discussions)
- 📧 Liên hệ: kidsautinh123@gmail.com

## 🚀 Lộ trình Phát triển

- [x] Nhận dạng cảm xúc cơ bản
- [x] Lọc bảo mật 3 lớp
- [x] Định tuyến LLM Địa phương/Đám mây
- [x] Giao thức Chống mất đồng bộ
- [ ] Ứng dụng di động
- [ ] Bảng điều khiển phân tích thời gian thực
- [ ] Hỗ trợ đa ngôn ngữ (v2.0)
- [ ] Sao chép giọng nói (v2.0)
- [ ] Học tập ngữ cảnh nâng cao
- [ ] Hỗ trợ gia tốc GPU

---

**Được xây dựng bằng ❤️ bởi Đội ngũ Phát triển KAI**

**Trạng thái:** 🟢 Sẵn sàng Sản xuất | **Cập nhật lần cuối:** 2026-06-01
