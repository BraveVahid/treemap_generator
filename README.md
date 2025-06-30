# Treemap Generator

Treemap Generator is a Telegram bot that provides daily cryptocurrency market updates, including a visual TreeMap of top coins by market capitalization and their 24-hour price change percentages. It fetches data from the CoinGecko API and sends updates to a specified Telegram channel.

## Features
- Daily Updates: Sends a daily TreeMap visualization of the top 10 cryptocurrencies by market cap, with color-coded 24-hour price changes.
- Price Keyboard: Displays current prices of selected cryptocurrencies (Bitcoin, Ethereum, Ripple, etc.) in an inline keyboard.
- Logging: Logs bot activities and errors to both console and a file for debugging.
- Error Handling: Basic error handling for API requests and Telegram interactions.

## Technologies Used
- Python 3.8+: Core programming language.
- Kurigram: For interacting with the Telegram Bot API.
- CoinGeckoAPI: For fetching cryptocurrency market data.
- Matplotlib & Squarify: For generating TreeMap visualizations.
- Python-dotenv: For managing environment variables.

## Installation
1. Clone the Repository:
```bash
git clone https://github.com/your-username/MarketMapBot.git
cd treemapgenerator
```

2. Install Dependencies: Ensure you have Python 3.8+ installed. Then, install the required packages:
```bash
pip install -r requirements.txt
```
3. Create a .env file in the project root and add the following:
```
your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
CHANNEL_ID=your_channel_id
Obtain API_ID and API_HASH from https://my.telegram.org
Get BOT_TOKEN from https://t.me/BotFather
Use the Telegram channel ID (e.g., -100123456789) where the bot will send updates.
```

4. Run the Bot:
```bash
python main.py
```


## Usage
- The bot runs continuously, sending a TreeMap and price updates to the specified Telegram channel every 24 hours.
- The TreeMap shows the top 10 cryptocurrencies by market cap, with colors indicating price changes:
  - Green: Positive change (>0.02%)
  - Red: Negative change (<-0.02%)
  - Gray: Neutral change (-0.02% to 0.02%)
- Inline keyboard buttons show current prices.
