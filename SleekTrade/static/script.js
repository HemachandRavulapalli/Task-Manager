document.addEventListener('DOMContentLoaded', () => {
    let orderType = 'MARKET';
    let orderSide = 'BUY';

    // Elements
    const balanceVal = document.getElementById('balance-value');
    const availableVal = document.getElementById('available-value');
    const ordersList = document.getElementById('orders-list');
    const orderForm = document.getElementById('order-form');
    const executeBtn = document.getElementById('place-order-btn');

    // Initialize TradingView Widget
    new TradingView.widget({
        "autosize": true,
        "symbol": "BINANCE:BTCUSDT.P",
        "interval": "15",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_top_toolbar": true,
        "save_image": false,
        "container_id": "tv-chart",
        "backgroundColor": "#131722",
        "gridColor": "rgba(43, 49, 57, 0.5)"
    });

    // Tab Logic
    document.querySelectorAll('.trade-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.trade-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            orderType = tab.dataset.type;

            document.getElementById('price-fields').style.display = (orderType !== 'MARKET') ? 'block' : 'none';
            document.getElementById('stop-fields').style.display = (orderType === 'STOP_LIMIT') ? 'block' : 'none';
        });
    });

    // Side Logic
    document.querySelectorAll('.btn-side').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.btn-side').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            orderSide = btn.dataset.side;

            executeBtn.className = `btn-execute ${orderSide.toLowerCase()}`;
            executeBtn.innerText = orderSide === 'BUY' ? 'SEND BUY ORDER' : 'SEND SELL ORDER';
        });
    });

    // Data Fetching
    async function updateData() {
        try {
            const res = await fetch('/api/balance');
            if (res.ok) {
                const data = await res.json();
                balanceVal.innerText = `${parseFloat(data.balance).toLocaleString()} USDT`;
                availableVal.innerText = `${parseFloat(data.availableBalance).toLocaleString()} USDT`;
                document.getElementById('bot-status').innerHTML = '<span class="status-dot" style="background:#00ffaa; box-shadow:0 0 10px #00ffaa"></span> LIVE';
            } else {
                document.getElementById('bot-status').innerHTML = '<span class="status-dot" style="background:#ff4d4d;"></span> OFFLINE';
            }

            const sym = document.getElementById('symbol').value || 'BTCUSDT';
            const oRes = await fetch(`/api/orders/${sym}`);
            if (oRes.ok) {
                const orders = await oRes.json();
                renderOrders(orders);
            }
        } catch (e) {
            console.error(e);
        }
    }

    function renderOrders(orders) {
        if (!orders || orders.length === 0) {
            ordersList.innerHTML = '<tr><td colspan="6" style="text-align:center; color:var(--text-dim); padding:2rem;">NO ACTIVE ORDERS</td></tr>';
            return;
        }
        ordersList.innerHTML = orders.map(o => `
            <tr>
                <td style="font-family:var(--font-mono)">${o.symbol}</td>
                <td><span class="side-${o.side.toLowerCase()}">${o.side}</span></td>
                <td>${o.type}</td>
                <td style="font-family:var(--font-mono)">${parseFloat(o.price).toFixed(2)}</td>
                <td style="font-family:var(--font-mono)">${o.origQty}</td>
                <td style="color:var(--accent)">${o.status}</td>
            </tr>
        `).join('');
    }

    // Place Order
    orderForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        executeBtn.disabled = true;
        executeBtn.innerText = 'TRANSMITTING...';

        const payload = {
            symbol: document.getElementById('symbol').value.toUpperCase(),
            side: orderSide,
            quantity: parseFloat(document.getElementById('quantity').value),
            order_type: orderType,
            price: document.getElementById('price').value ? parseFloat(document.getElementById('price').value) : null,
            stop_price: document.getElementById('stop_price').value ? parseFloat(document.getElementById('stop_price').value) : null
        };

        try {
            const res = await fetch('/api/order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await res.json();
            if (res.ok) {
                toast(`Order Executed: ${result.orderId}`, 'success');
                updateData();
            } else {
                toast(result.detail, 'error');
            }
        } catch (e) {
            toast('Connection Failed', 'error');
        } finally {
            executeBtn.disabled = false;
            executeBtn.innerText = orderSide === 'BUY' ? 'SEND BUY ORDER' : 'SEND SELL ORDER';
        }
    });

    function toast(msg, type) {
        const t = document.createElement('div');
        t.className = 'toast';
        t.style.borderLeftColor = type === 'success' ? '#00ffaa' : '#ff4d4d';
        t.innerText = msg;
        document.getElementById('notifications').appendChild(t);
        setTimeout(() => t.remove(), 4000);
    }

    setInterval(updateData, 3000);
    updateData();
});
