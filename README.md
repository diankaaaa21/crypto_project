# 🚀 Django WebSocket Binance Integration

A Django-based project that integrates **WebSocket API from Binance** for real-time cryptocurrency price tracking.

## 📡 Features
- ✅ Real-time updates via **Binance WebSocket API**
- ✅ Track multiple trading pairs (e.g., `BTCUSDT`, `ETHUSDT`)
- ✅ **WebSocket server** using **Django Channels** and **Daphne**
- ✅ **PostgreSQL** for persistent storage
- ✅ **Redis** (optional) for caching or background task management
- ✅ **Celery** (optional) for async processing
- ✅ **REST API** to retrieve and filter historical trade data
- ✅ **Dockerized** with **Docker Compose** + **Nginx**
- ✅ Easy testing with `pytest` and Mock WebSocket server
- ✅ **.env** support for configuration 

---

## 📦 Tech Stack
- **Backend:** Django, Django REST Framework  
- **WebSocket:** Django Channels, Daphne  
- **Database:** PostgreSQL  
- **Background Tasks:** Celery, Redis  
- **Testing:** Pytest, Websockets  
- **DevOps:** Docker, Docker Compose, Nginx  
- **Env Management:** python-dotenv 

---

## ⚙ Installation and Setup
### 1️⃣ Clone the repository
```bash
git clone https://github.com/diankaaaa21/crypto_project.git
cd crypto_project
```

### 2️⃣ Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

### 3️⃣ Configure environment variables
Create a **`.env`** file:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=db,localhost
DATABASE_URL=postgres://user:password@localhost:5432/db_name
```

### 4️⃣ Database setup
```bash
python manage.py migrate
python manage.py createsuperuser  # (Create an admin user)
``` 

---
## 🐳 Dockerized Setup
### 🔹 Start with Docker Compose
```bash
docker-compose up --build
```
### 🔹 Access services
- WebSocket: ws://localhost:8100/
- REST API (trades): http://localhost:8000/trades/
- Auth/register (если есть): http://localhost:8000/auth/register/

---
## 📡 WebSocket Client
### 📌 **Test Binance WebSocket API**
```python
import asyncio
import websockets

async def test_binance():
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    try:
        print("Connecting to Binance WebSocket...")
        async with websockets.connect(url) as ws:
            while True:
                message = await ws.recv()
                print("Binance data:", message)
    except Exception as e:
        print(f"Connection error: {e}")

asyncio.run(test_binance())
```

### 📌 **Connect to Django WebSocket**
```python
import asyncio
import websockets

async def test_django_ws():
    selected_crypto = "BTCUSDT"
    url = f"ws://127.0.0.1:8000/ws/trades/{selected_crypto}"
    try:
        print(f"Connecting to {url}...")
        async with websockets.connect(url) as ws:
            while True:
                message = await ws.recv()
                print("WebSocket data:", message)
    except Exception as e:
        print(f"Connection error: {e}")

asyncio.run(test_django_ws())
```

---

## 🔌 REST API
### 📌 **Get historical price data**
```http
GET /trades/
```
Example response:
```json
[
  {
    "symbol": "BTCUSDT",
    "price": "43250.12",
    "quantity": "0.005",
    "trade_time": "2024-03-11T12:00:00Z"
  }
]
```

### 📌 **Filter by symbol (e.g., BTCUSDT)**
```http
GET /trades/?symbol=btcusdt
```
Example response:
```json
[
  {
    "symbol": "BTCUSDT",
    "price": "43250.12",
    "quantity": "0.005",
    "trade_time": "2024-03-11T12:00:00Z"
  },
  {
    "symbol": "BTCUSDT",
    "price": "43248.50",
    "quantity": "0.002",
    "trade_time": "2024-03-11T11:59:00Z"
  }
]
```
✅ **Now you can filter price data by trading pair!**

---

## 🛠 Testing
### 📌 **Run all tests**
```bash
pytest
```
### 📌 **Mock WebSocket Server**
```python
import pytest
import asyncio
import websockets


async def mock_django_ws(websocket, path):
    await websocket.send("Hello, WebSocket!")


@pytest.fixture
async def websocket_server():
    server = await websockets.serve(mock_django_ws, "127.0.0.1", 8000)


    await asyncio.sleep(0.1)

    yield server


    server.close()
    await server.wait_closed()


@pytest.mark.asyncio
async def test_websocket_server(websocket_server):
    async with websockets.connect("ws://127.0.0.1:8000") as ws:
        message = await ws.recv()
        assert message == "Hello, WebSocket!"
```
✅ **Now you can test WebSocket functionality without connecting to Binance!**

---

## 📜 `requirements.txt`
```txt
django
djangorestframework
django-channels
daphne
websockets
psycopg2-binary
django-environ
celery
redis
pytest
pytest-django
flower
```

---

## 🚀 Deployment (Production)
- ✅ gunicorn + nginx + daphne ready 
- ✅ Configurable through .env
- ✅ Dockerized for easy deployment
- ⏳ Add HTTPS with Let's Encrypt (via Nginx)
- ⏳ Add monitoring (e.g., Flower)

👨‍💻 **Author:** [Diana]  
📌 **GitHub:** [[Repository Link](https://github.com/diankaaaa21/crypto_project.git)]  


