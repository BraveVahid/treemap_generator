from pycoingecko import CoinGeckoAPI
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.logger import logger
from typing import Dict, Optional


class CryptoPriceFetcher:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.symbol_aliases = {
            "bitcoin": "BTC",
            "ethereum": "ETH",
            "ripple": "XRP",
            "binancecoin": "BNB",
            "solana": "SOL",
            "tron": "TRX",
            "the-open-network": "TON",
            "dogecoin": "DOGE"
        }

    def _fetch_data(self) -> Dict[str, float]:
        try:
            logger.info("Fetching price data from CoinGecko")
            coins = self.cg.get_price(
                ids=list(self.symbol_aliases.keys()),
                vs_currencies="usd"
            )

            if not coins:
                logger.warning("No price data received from CoinGecko")
                return {}

            result = {k: v["usd"] for k, v in coins.items() if "usd" in v}
            logger.info(f"Successfully fetched price data for {len(result)} coins")
            return result

        except Exception as e:
            logger.error(f"Error fetching price data: {str(e)}")
            return {}

    def generate_price_keyboard(self) -> Optional[InlineKeyboardMarkup]:
        try:
            prices = self._fetch_data()

            if not prices:
                logger.warning("No price data available for keyboard generation")
                return None

            buttons = []
            row = []

            for coin_id, price in prices.items():
                if coin_id in self.symbol_aliases:
                    symbol = self.symbol_aliases[coin_id]
                    button = InlineKeyboardButton(
                        text=f"{symbol}: ${price:.2f}",
                        callback_data="ignore"
                    )
                    row.append(button)

                    if len(row) == 2:
                        buttons.append(row)
                        row = []

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
            return None
