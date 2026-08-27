let socket = null;

function connectWebSocket() {
    const cryptoSelect = document.getElementById("crypto");
    if (!cryptoSelect) return;

    const selectedCrypto = cryptoSelect.value;
    const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    const wsUrl = `${wsProtocol}${window.location.host}/ws/trades/${selectedCrypto}/`;

    console.log(`[WebSocket] Connecting to: ${wsUrl}`);

    if (socket) {
        socket.onopen = null;
        socket.onmessage = null;
        socket.onerror = null;
        socket.onclose = null;
        socket.close();
        socket = null;
    }

    const tradeList = document.getElementById("trade-list");
    if (tradeList) tradeList.innerHTML = "";

    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        console.log(`[WebSocket] Connection is opened: ${selectedCrypto}`);
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const listItem = document.createElement("li");

        if (data.symbol && data.price) {
            listItem.textContent = `${data.symbol}: ${data.price}`;
        } else if (data.message) {
            listItem.textContent = data.message;
        }

        if (tradeList) {
            tradeList.insertBefore(listItem, tradeList.firstChild);
            if (tradeList.children.length > 10) {
                tradeList.removeChild(tradeList.lastChild);
            }
        }
    };
}

