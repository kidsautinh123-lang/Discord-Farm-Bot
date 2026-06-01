# KAI System

**Hệ thống Text-to-Speech Nâng cao với Phân tích Cảm xúc và Giao thức Chống Mất đồng bộ**

![Trạng thái](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Node.js](https://img.shields.io/badge/node.js-14%2B-green)
![Docker](https://img.shields.io/badge/docker-supported-blue)

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
- 🐳 **Docker & Kubernetes Ready** - Triển khai dễ dàng trên mọi nền tảng

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
| 🐳 **Container Ready** | Docker, Docker Compose, Kubernetes support |

## 🚀 Cài đặt

### Yêu cầu trước
- Python 3.8+
- Node.js 14+
- npm hoặc yarn
- Docker & Docker Compose (tuỳ chọn)

### Cài đặt nhanh (Local)

#### Cài đặt Python

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

#### Cài đặt Node.js

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

---

## 🐳 Docker & Docker Compose Setup

### Yêu cầu Docker
- **Docker Desktop**: [Tải xuống](https://www.docker.com/products/docker-desktop)
- **Docker Compose**: Đã bao gồm trong Docker Desktop

### Kiểm tra cài đặt

```bash
docker --version
docker-compose --version
```

### 📁 Cấu trúc Docker

```
kai-demo/
├── Dockerfile                 # Image cho ứng dụng chính
├── Dockerfile.node           # Image cho Node.js server
├── docker-compose.yml        # Orchestration file
├── docker-compose.prod.yml   # Production configuration
├── .dockerignore             # Exclude files from build
└── .env.docker              # Docker environment variables
```

---

## 🐳 Docker Compose - Cách nhanh nhất

### 1️⃣ Khởi động Toàn bộ Hệ thống

```bash
# Khởi động tất cả services
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng hệ thống
docker-compose down
```

### 2️⃣ Docker Compose File Cơ bản

Tạo file `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # 🟦 Node.js Express Server
  kai-server:
    build:
      context: .
      dockerfile: Dockerfile.node
    container_name: kai-server
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
      - TTS_API_KEY=${TTS_API_KEY}
      - TTS_PROVIDER=google
      - REDIS_URL=redis://kai-redis:6379
    depends_on:
      - kai-redis
      - kai-python
    volumes:
      - ./javascript:/app/javascript
      - ./logs:/app/logs
    networks:
      - kai-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # 🐍 Python Main System
  kai-python:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: kai-python
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=INFO
      - DATABASE_PATH=/data/bekai_history.db
      - REDIS_URL=redis://kai-redis:6379
      - LLM_API_KEY=${LLM_API_KEY}
    depends_on:
      - kai-redis
    volumes:
      - ./python:/app/python
      - ./data:/data
      - ./logs:/app/logs
    networks:
      - kai-network
    restart: unless-stopped

  # 💾 Redis Cache
  kai-redis:
    image: redis:7-alpine
    container_name: kai-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - kai-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # 📦 PostgreSQL Database (tuỳ chọn)
  kai-db:
    image: postgres:15-alpine
    container_name: kai-db
    environment:
      - POSTGRES_DB=kai_system
      - POSTGRES_USER=kai_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - kai-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U kai_user"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  redis-data:
  postgres-data:

networks:
  kai-network:
    driver: bridge
```

### 3️⃣ Dockerfile cho Python

Tạo file `Dockerfile`:

```dockerfile
# Build stage
FROM python:3.9-slim as builder

WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Set environment variables
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy application code
COPY python/ ./python/

# Create data directory
RUN mkdir -p /data /app/logs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import socket; socket.create_connection(('127.0.0.1', 8000), timeout=5)" || exit 1

# Run application
CMD ["python", "python/main.py"]
```

### 4️⃣ Dockerfile cho Node.js

Tạo file `Dockerfile.node`:

```dockerfile
# Build stage
FROM node:18-alpine as builder

WORKDIR /build

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Runtime stage
FROM node:18-alpine

WORKDIR /app

# Install production dependencies only
COPY package*.json ./
RUN npm ci --only=production

# Copy built application
COPY --from=builder /build/node_modules ./node_modules

# Copy source code
COPY javascript/ ./javascript/

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"

# Start application
CMD ["node", "javascript/server.js"]
```

### 5️⃣ .dockerignore File

```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.DS_Store
__pycache__
*.pyc
.pytest_cache
.venv
build
dist
*.egg-info
```

### 6️⃣ Environment Variables (.env.docker)

```env
# Server
NODE_ENV=production
PORT=3000

# APIs
TTS_API_KEY=your_tts_api_key
TTS_PROVIDER=google
LLM_API_KEY=your_llm_api_key

# Database
DB_PASSWORD=secure_password_here
DATABASE_PATH=/data/bekai_history.db
DATABASE_MAX_SIZE_MB=30

# Redis
REDIS_URL=redis://kai-redis:6379

# Security
MAX_INPUT_LENGTH=120
MAX_WORDS=25
SECURITY_LEVEL=strict

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/kai-system.log
```

---

## 🎮 Sử dụng Docker Compose

### Khởi động Hệ thống

```bash
# Khởi động tất cả services (chế độ nền)
docker-compose up -d

# Khởi động với output trực tiếp
docker-compose up

# Khởi động một service cụ thể
docker-compose up -d kai-server
```

### Kiểm tra Trạng thái

```bash
# Liệt kê tất cả containers
docker-compose ps

# Xem logs
docker-compose logs -f                    # Tất cả
docker-compose logs -f kai-server         # Express server
docker-compose logs -f kai-python         # Python system
docker-compose logs -f kai-redis          # Redis

# Kiểm tra health
docker-compose ps --format "table {{.Service}}\t{{.Status}}"
```

### Dừng & Xóa

```bash
# Dừng tất cả services
docker-compose stop

# Dừng service cụ thể
docker-compose stop kai-server

# Xóa containers (giữ volumes)
docker-compose down

# Xóa tất cả (bao gồm volumes)
docker-compose down -v

# Xóa images
docker-compose down --rmi all
```

### Rebuild Images

```bash
# Rebuild image
docker-compose build

# Rebuild không cache
docker-compose build --no-cache

# Rebuild service cụ thể
docker-compose build kai-server
```

---

## 🔧 Truy cập Services

### Express Server
```bash
# Truy cập từ host
curl http://localhost:3000/health

# Hoặc trong container khác
curl http://kai-server:3000/health
```

### Redis
```bash
# Kết nối từ host
redis-cli -h localhost -p 6379

# Từ trong Docker
docker-compose exec kai-redis redis-cli
```

### PostgreSQL (tuỳ chọn)
```bash
# Kết nối từ host
psql -h localhost -U kai_user -d kai_system

# Từ trong Docker
docker-compose exec kai-db psql -U kai_user -d kai_system
```

### Python Logs
```bash
# Xem logs Python
docker-compose logs -f kai-python

# Ghi lại logs
docker-compose logs kai-python > python-logs.txt
```

---

## 📊 Docker Compose Production Setup

### Tạo `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  kai-server:
    build:
      context: .
      dockerfile: Dockerfile.node
      args:
        NODE_ENV: production
    container_name: kai-server-prod
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
    depends_on:
      kai-redis:
        condition: service_healthy
      kai-python:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
    networks:
      - kai-network
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

  kai-python:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: kai-python-prod
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=WARNING
    depends_on:
      kai-redis:
        condition: service_healthy
    volumes:
      - ./data:/data
      - ./logs:/app/logs
    networks:
      - kai-network
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G

  kai-redis:
    image: redis:7-alpine
    container_name: kai-redis-prod
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - kai-network
    restart: always
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: kai-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - kai-server
    networks:
      - kai-network
    restart: always

volumes:
  redis-data:
    driver: local

networks:
  kai-network:
    driver: bridge
```

### Khởi động Production

```bash
# Khởi động production setup
docker-compose -f docker-compose.prod.yml up -d

# Theo dõi logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 🔍 Giám sát & Debugging

### Vào bên trong Container

```bash
# Python container
docker-compose exec kai-python bash

# Node.js container
docker-compose exec kai-server sh

# Redis container
docker-compose exec kai-redis sh
```

### Kiểm tra Network

```bash
# Liệt kê networks
docker network ls

# Kiểm tra network chi tiết
docker network inspect kai-network
```

### Xem Resource Usage

```bash
# Real-time stats
docker stats

# Specific container
docker stats kai-server kai-python kai-redis
```

---

## 🐛 Khắc phục Sự cố Docker

### Container không khởi động

```bash
# Xem logs lỗi
docker-compose logs kai-server

# Kiểm tra image
docker images | grep kai

# Rebuild
docker-compose build --no-cache kai-server
```

### Port đã được sử dụng

```bash
# Tìm process sử dụng port
lsof -i :3000

# Thay đổi port trong docker-compose.yml
ports:
  - "3001:3000"  # Thay đổi từ 3000 sang 3001
```

### Kết nối Database không thành công

```bash
# Kiểm tra health
docker-compose ps

# Xem logs database
docker-compose logs kai-db

# Thử kết nối lại
docker-compose restart kai-db kai-server
```

### Out of Memory

```bash
# Kiểm tra resource usage
docker stats

# Tăng memory limit trong docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G  # Tăng từ 1G
```

---

## 📈 Scaling với Docker Compose

### Chạy Multiple Instances

```bash
# Chạy 3 instances của service
docker-compose up -d --scale kai-server=3

# Kiểm tra
docker-compose ps
```

### Load Balancer

Thêm Nginx trong docker-compose.yml:

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
  depends_on:
    - kai-server
```

---

## 🚀 Deployment Options

### 1. **Docker Hub**

```bash
# Login
docker login

# Tag image
docker tag kai-server:latest your-username/kai-server:latest

# Push
docker push your-username/kai-server:latest
```

### 2. **AWS ECS**

```bash
# Tạo task definition từ docker-compose
ecs-cli compose --file docker-compose.yml create

# Khởi động service
ecs-cli service up
```

### 3. **Google Cloud Run**

```bash
# Build & push
gcloud builds submit --tag gcr.io/your-project/kai-server

# Deploy
gcloud run deploy kai-server --image gcr.io/your-project/kai-server
```

### 4. **Kubernetes**

```bash
# Generate manifests từ docker-compose
kompose convert

# Deploy
kubectl apply -f *.yaml
```

---

## 🎮 Bắt đầu nhanh (Docker)

### 1️⃣ Setup ban đầu

```bash
# Clone repository
git clone https://github.com/kidsautinh123-lang/Discord-Farm-Bot.git
cd Discord-Farm-Bot

# Tạo .env file
cp .env.docker .env

# Cập nhật API keys
nano .env
```

### 2️⃣ Khởi động

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

### 3️⃣ Kiểm tra

```bash
# Health check
curl http://localhost:3000/health

# Xem logs
docker-compose logs -f
```

### 4️⃣ Dừng

```bash
# Dừng tất cả
docker-compose down

# Dừng & xóa volumes
docker-compose down -v
```

---

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
  "platform": "TikTok",
  "user_raw_name": "user123",
  "payload": "Em yeu anh",
  "type": "chat"
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
});
```

---

## 🧠 Chi tiết Ma trận Cảm xúc

| Cảm xúc | Từ khóa Kích hoạt | Phong cách Phản hồi | Từ Buffer |
|---------|------------------|-------------------|----------|
| **CUTE** | Lợi, khen ngợi | Ngọt ngào, thiên thơ | nha, ne, um |
| **YANDERE** | Tỏ tình, ghen tỵ | Chiếm hữu, mãnh liệt | ..., hm, tsk |
| **TSUNDERE** | Chế giễu, khoác lác | Phòng vệ, tsun | hu, xi, che |
| **TROLL** | Trò đùa, yêu cầu vô lý | Mỉa mai, vui vẻ | haha, ak ak |
| **GENKI** | Game, chủ đề vui | Năng lượng cao | !, yeah, yay |
| **EXCITED** | Quà tặng, đóng góp | Hứng khởi, cảm ơn | !, thank you |
| **COMFORT** | Chủ đề buồn, căng thẳng | An ủi, hỗ trợ | ..., nhe, co |
| **SERIOUS** | Khoa học, logic | Chuyên nghiệp, chính thức | (không) |

---

## 🔐 Kiến trúc Bảo mật

### Lớp 1: Kiểm tra Ranh giới Đầu vào
- **Độ dài tối đa**: 120 ký tự
- **Từ tối đa**: 25 từ
- **Mục đích**: Ngăn chặn các cuộc tấn công DoS/spam

### Lớp 2: Quét Danh sách Đen
- **Từ khóa danh sách đen**: Chính trị, tôn giáo, nội dung dành cho người lớn, bạo lực
- **Mục đích**: Lọc nội dung có hại/nhạy cảm

### Lớp 3: Bảo vệ Chống Jailbreak
- **Phát hiện**: Ký tự đặc biệt `[ ] { } < > / \`
- **Hành động**: Tự động gắn thẻ là TROLL nếu phát hiện
- **Mục đích**: Ngăn chặn các cuộc tấn công tiêm nhập lời nhắc

---

## 📁 Cấu trúc Dự án

```
kai-demo/
├── python/
│   ├── main.py                    # Bộ điều phối hệ thống
│   ├── security_filter.py         # Xác thực bảo mật 3 lớp
│   ├── emotion_tagger.py          # Động cơ phân loại cảm xúc
│   ├── llm_router.py              # Định tuyến LLM
│   ├── tts_processor.py           # Xử lý TTS
│   ├── memory_manager.py          # Quản lý bộ nhớ
│   ├── anti_desync.py             # Giao thức đồng bộ
│   └── test_suite.py              # Kiểm tra
│
├── javascript/
│   ├── server.js                  # Server Express
│   ├── queue-manager.js           # Quản lý hàng đợi
│   ├── emotion-handler.js         # Xử lý cảm xúc
│   ├── tts-client.js              # TTS client
│   └── sync-coordinator.js        # Điều phối đồng bộ
│
├── Dockerfile                     # Python image
├── Dockerfile.node               # Node.js image
├── docker-compose.yml            # Development setup
├── docker-compose.prod.yml       # Production setup
├── package.json                  # Node.js dependencies
├── requirements.txt              # Python dependencies
├── .dockerignore                 # Docker ignore file
├── .env.docker                   # Docker environment
└── README.md
```

---

## 📊 Chỉ số Hiệu suất

| Chỉ số | Mục tiêu | Trạng thái |
|--------|---------|-----------|
| Dung lượng Hàng đợi Đầu vào | 1000 mục | ✅ |
| Phản hồi LLM Địa phương | <200ms | ✅ |
| Tạo TTS | ~400ms | ✅ |
| Độ trễ Tổng cộng | 500-600ms | ✅ |
| Uptime | >99.5% | ✅ |

---

## 🤝 Đóng góp

Chúng tôi hoan nghênh các đóng góp! Vui lòng:

1. Fork repository
2. Tạo branch tính năng (`git checkout -b feature/amazing-feature`)
3. Commit các thay đổi (`git commit -m 'Thêm tính năng tuyệt vời'`)
4. Push đến branch (`git push origin feature/amazing-feature`)
5. Mở Pull Request

---

## 📄 Giấy phép

MIT License - Xem file LICENSE để biết chi tiết

---

## 📞 Hỗ trợ & Phản hồi

- 🐛 [Báo cáo Lỗi](https://github.com/kidsautinh123-lang/Discord-Farm-Bot/issues)
- 💡 [Yêu cầu Tính năng](https://github.com/kidsautinh123-lang/Discord-Farm-Bot/discussions)
- 📧 Liên hệ: kidsautinh123@gmail.com

---

## 🚀 Lộ trình Phát triển

- [x] Nhận dạng cảm xúc cơ bản
- [x] Lọc bảo mật 3 lớp
- [x] Định tuyến LLM Địa phương/Đám mây
- [x] Giao thức Chống mất đồng bộ
- [x] Docker & Docker Compose support
- [ ] Kubernetes deployment
- [ ] Ứng dụng di động
- [ ] Hỗ trợ đa ngôn ngữ (v2.0)
- [ ] Sao chép giọng nói (v2.0)
- [ ] Gia tốc GPU

---

**Được xây dựng bằng ❤️ bởi Đội ngũ Phát triển KAI**

**Trạng thái:** 🟢 Sẵn sàng Sản xuất | **Cập nhật lần cuối:** 2026-06-01
