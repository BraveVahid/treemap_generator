from pycoingecko import CoinGeckoAPI
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from logger import logger

class CryptoPriceFetcher:
    def __init__(self):
        self.cg = CoinGeckoAPI()

    def _fetch_data(self) -> dict[str, float]:
        try:
            logger.info("Fetching price data from CoinGecko")
            coins = self.cg.get_price(
                ids=["bitcoin", "ethereum", "ripple", "binancecoin", "solana", "tron", "the-open-network", "dogecoin"],
                vs_currencies="usd"
            )
            logger.info("Successfully fetched price data")
            return {k: v["usd"] for k, v in coins.items()}
        except Exception as e:
            logger.error(f"Error fetching price data: {str(e)}")
            return {}

    def generate_price_keyboard(self) -> InlineKeyboardMarkup:
        try:
            symbol_aliases = {
                "bitcoin": "BTC",
                "ethereum": "ETH",
                "ripple": "XRP",
                "binancecoin": "BNB",
                "solana": "SOL",
                "tron": "TRX",
                "the-open-network": "TON",
                "dogecoin": "DOGE"
            }

            prices = self._fetch_data()
            buttons = list()
            row = list()

            for k, v in prices.items():
                button = InlineKeyboardButton(text=f"{symbol_aliases[k]}: {v:.2f}$", callback_data="ignore")
                row.append(button)

                if len(row) == 2:
                    buttons.append(row)
                    row = list()

            if row:
                buttons.append(row)

            buttons.append([
                InlineKeyboardButton(text="ℹ️ Source", url="https://www.coingecko.com/"),
                InlineKeyboardButton(text="💸 Buy/Sell Crypto", url="https://t.me/send?start=r-ejwc4-market")
            ])

            logger.info("Successfully generated price keyboard")
            return InlineKeyboardMarkup(buttons)
        except Exception as e:
            logger.error(f"Error generating price keyboard: {str(e)}")
