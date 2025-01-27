document.addEventListener("DOMContentLoaded", function () {
    const tickerMove = document.getElementById("ticker-move");

    const stocks = [
        { "symbol": "NVDA", "name": "NVIDIA" },
        { "symbol": "AAPL", "name": "Apple" },
        { "symbol": "MSFT", "name": "Microsoft" },
        { "symbol": "AMZN", "name": "Amazon" },
        { "symbol": "GOOG", "name": "Alphabet" },
        { "symbol": "META", "name": "Meta" },
        { "symbol": "TSLA", "name": "Tesla" },
        { "symbol": "TSM", "name": "TSMC" },
        { "symbol": "AVGO", "name": "Broadcom" },
        { "symbol": "ORCL", "name": "Oracle" },
        { "symbol": "TCEHY", "name": "Tencent" },
        { "symbol": "NFLX", "name": "Netflix" },
        { "symbol": "SAP", "name": "SAP" },
        { "symbol": "CRM", "name": "Salesforce" },
        { "symbol": "ASML", "name": "ASML" },
        { "symbol": "005930.KS", "name": "Samsung" },
        { "symbol": "CSCO", "name": "Cisco" },
        { "symbol": "NOW", "name": "ServiceNow" },
        { "symbol": "BABA", "name": "Alibaba" },
        { "symbol": "IBM", "name": "IBM" },
        { "symbol": "AMD", "name": "AMD" },
        { "symbol": "QCOM", "name": "QUALCOMM" },
        { "symbol": "ADBE", "name": "Adobe" },
        { "symbol": "PLTR", "name": "Palantir" },
        { "symbol": "ARM", "name": "Arm Holdings" },
        { "symbol": "TXN", "name": "Texas Instruments" },
        { "symbol": "INTU", "name": "Intuit" },
        { "symbol": "ANET", "name": "Arista Networks" },
        { "symbol": "SU.PA", "name": "Schneider Electric" },
        { "symbol": "BKNG", "name": "Booking Holdings" },
        { "symbol": "PDD", "name": "Pinduoduo" },
        { "symbol": "AMAT", "name": "Applied Materials" },
        { "symbol": "UBER", "name": "Uber" },
        { "symbol": "SHOP", "name": "Shopify" },
        { "symbol": "SONY", "name": "Sony" },
        { "symbol": "PANW", "name": "Palo Alto Networks" },
        { "symbol": "APP", "name": "AppLovin" },
        { "symbol": "ADP", "name": "Automatic Data Processing" },
        { "symbol": "FI", "name": "Fiserv" },
        { "symbol": "XIACF", "name": "Xiaomi" },
        { "symbol": "3690.HK", "name": "Meituan" },
        { "symbol": "MU", "name": "Micron Technology" },
        { "symbol": "ADI", "name": "Analog Devices" },
        { "symbol": "MRVL", "name": "Marvell Technology Group" },
        { "symbol": "6861.T", "name": "Keyence" },
        { "symbol": "000660.KS", "name": "SK Hynix" },
        { "symbol": "SPOT", "name": "Spotify" },
        { "symbol": "LRCX", "name": "Lam Research" },
        { "symbol": "KLAC", "name": "KLA" },
        { "symbol": "MELI", "name": "MercadoLibre" }
    ];

    // Function to display all tickers
    function displayTickers() {
        // Clear previous ticker items
        tickerMove.innerHTML = '';

        // Create ticker items for all stocks
        stocks.forEach(stock => {
            const span = document.createElement("span");
            span.className = "ticker-item";
            span.textContent = `${stock.name} [ ${stock.symbol} ]`;
            tickerMove.appendChild(span);
        });
    }

    // Display the tickers immediately
    displayTickers();

    // Set interval to refresh the ticker display every 30 seconds (30000 milliseconds)
    setInterval(displayTickers, 1000);
});