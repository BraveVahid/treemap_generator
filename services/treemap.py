import squarify
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
from pycoingecko import CoinGeckoAPI
from datetime import datetime
from io import BytesIO
from utils.logger import logger

class CryptoTreeMap:
    def __init__(self):
        self.figure_size = (12, 7)
        self.dpi = 200
        self.positive_color = "#16c784"
        self.strong_positive_color = "#157e59"
        self.negative_color = "#f8baba"
        self.strong_negative_color = "#c5151f"
        self.neutral_color = "#6d7588"
        self.alpha = 1
        self.edge_color = "white"
        self.line_width = 1
        self.font_size = 10
        self.font_color = "white"
        self.font_weight = "normal"
        self.cg = CoinGeckoAPI()

    def _generate_colors_and_labels(self, data: pd.DataFrame) -> tuple[List[str], List[str]]:
        try:
            colors = list()
            for i in data["price_change_percentage_24h"]:
                if -0.02 <= i <= 0.02:
                    colors.append(self.neutral_color)
                elif 0.02 < i <= 5:
                    colors.append(self.positive_color)
                elif 5 < i:
                    colors.append(self.strong_positive_color)
                elif -5 <= i < -0.02:
                    colors.append(self.negative_color)
                elif -5 > i:
                    colors.append(self.strong_negative_color)

            labels = [f"{symbol}\n{change:.2f}%" for symbol, change in
                    zip(data["symbol"], data["price_change_percentage_24h"])]

            return colors, labels
        except Exception as e:
            logger.error(f"Error generating colors and labels: {str(e)}")

    def _get_data(self) -> pd.DataFrame:
        try:
            logger.info("Fetching top coins data from CoinGecko")
            top_coins = self.cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=10, page=1)

            data = []
            for coin in top_coins:
                data.append({
                    "symbol": coin["symbol"].upper(),
                    "market_cap": coin["market_cap"],
                    "price_change_percentage_24h": coin["price_change_percentage_24h"]
                })

            df = pd.DataFrame(data)
            df = df[df["market_cap"] > 0]
            logger.info(f"Successfully fetched data for {len(df)} coins")
            return df
        except Exception as e:
            logger.error(f"Error fetching coin data: {str(e)}")

    def create_treemap_buffer(self) -> BytesIO:
        try:
            df = self._get_data()
            colors, labels = self._generate_colors_and_labels(df)

            plt.figure(figsize=self.figure_size)
            squarify.plot(
                sizes=df["market_cap"],
                label=labels,
                color=colors,
                alpha=self.alpha,
                edgecolor=self.edge_color,
                linewidth=self.line_width,
                text_kwargs={
                    "fontsize": self.font_size,
                    "color": self.font_color,
                    "weight": self.font_weight
                }
            )
            title = f"Cryptocurrency TreeMap | {datetime.today().strftime('%Y-%m-%d')}"
            plt.title(title)
            plt.axis("off")

            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=self.dpi, bbox_inches="tight")
            buffer.seek(0)
            plt.close()
            logger.info("Successfully created treemap buffer")
            return buffer
        except Exception as e:
            logger.error(f"Error creating treemap: {str(e)}")
            plt.close()
