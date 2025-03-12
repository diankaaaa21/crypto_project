# 🚀 Django WebSocket Binance Integration

A Django-based project that integrates **WebSocket API from Binance** for real-time cryptocurrency price tracking.

## 📡 Features
✔ **Connect to Binance WebSocket API** (`wss://stream.binance.com:9443/ws/btcusdt@trade`).  
✔ **Receive real-time price updates** for selected cryptocurrency pairs (e.g., BTC/USDT, ETH/USDT).  
✔ **Store price updates in PostgreSQL**.  
✔ **Django WebSocket Server** (Django Channels) to **stream live updates to clients**.  
✔ **REST API** to view historical price changes.  
✔ **Filter prices by trading pairs** (`?symbol=btcusdt`).  
✔ **Testing** with pytest and Mock WebSocket.  
✔ **WebSocket server runs with Daphne**.  
✔ **Dotenv support** for environment variables.  

---

## 📦 Tech Stack
- **Django** + **Django REST Framework** – Backend API  
- **Django Channels** + **Daphne** – WebSockets  
- **PostgreSQL** – Data storage  
- **Redis** *(optional)* – Caching  
- **Celery** *(optional)* – Background tasks  
- **pytest + Mock WebSocket** – Testing  
- **dotenv** – Environment variable management  

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
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:password@localhost:5432/db_name
```

### 4️⃣ Database setup
```bash
python manage.py migrate
python manage.py createsuperuser  # (Create an admin user)
```

### 5️⃣ Start the WebSocket server with Daphne
```bash
daphne -b 127.0.0.1 -p 8000 crypto_project.asgi:application
```
💡 **Note:** `daphne` replaces `runserver` to support WebSockets.  

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
GET /api/trades/
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
GET /api/trades/?symbol=btcusdt
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
```

---

## 🚀 What's next?
- 🔹 **Add caching with Redis**  
- 🔹 **Optimize Celery for background tasks**  
- 🔹 **Deploy on server (`gunicorn + nginx + daphne`)**  

👨‍💻 **Author:** [Diana]  
📌 **GitHub:** [[Repository Link](https://github.com/diankaaaa21/crypto_project.git)]  


