import squarify
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
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

    def _generate_colors_and_labels(self, data: pd.DataFrame) -> Tuple[List[str], List[str]]:
        try:
            colors = []
            labels = []

            for _, row in data.iterrows():
                change = row["price_change_percentage_24h"]
                symbol = row["symbol"]

                if -0.02 <= change <= 0.02:
                    color = self.neutral_color
                elif 0.02 < change <= 5:
                    color = self.positive_color
                elif change > 5:
                    color = self.strong_positive_color
                elif -5 <= change < -0.02:
                    color = self.negative_color
                else:
                    color = self.strong_negative_color

                colors.append(color)
                labels.append(f"{symbol}\n{change:.2f}%")

            return colors, labels

        except Exception as e:
            logger.error(f"Error generating colors and labels: {str(e)}")
            return [], []

    def _get_data(self) -> Optional[pd.DataFrame]:
        try:
            logger.info("Fetching top coins data from CoinGecko")
            top_coins = self.cg.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=10,
                page=1
            )

            if not top_coins:
                logger.warning("No coin data received from CoinGecko")
                return None

            data = []
            for coin in top_coins:
                if all(key in coin for key in ["symbol", "market_cap", "price_change_percentage_24h"]):
                    if coin["market_cap"] and coin["market_cap"] > 0:
                        data.append({
                            "symbol": coin["symbol"].upper(),
                            "market_cap": coin["market_cap"],
                            "price_change_percentage_24h": coin["price_change_percentage_24h"] or 0
                        })

            if not data:
                logger.warning("No valid coin data found")
                return None

            df = pd.DataFrame(data)
            logger.info(f"Successfully processed data for {len(df)} coins")
            return df

        except Exception as e:
            logger.error(f"Error fetching coin data: {str(e)}")
            return None

    def create_treemap_buffer(self) -> Optional[BytesIO]:
        fig = None
        try:
            df = self._get_data()
            if df is None or df.empty:
                logger.error("No data available for treemap generation")
                return None

            colors, labels = self._generate_colors_and_labels(df)

            if not colors or not labels:
                logger.error("Failed to generate colors and labels")
                return None

            fig = plt.figure(figsize=self.figure_size)

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
            plt.title(title, fontsize=14, color='black', pad=20)
            plt.axis("off")

            buffer = BytesIO()
            plt.savefig(
                buffer,
                format='png',
                dpi=self.dpi,
                bbox_inches="tight",
                facecolor='white',
                edgecolor='none'
            )
            buffer.seek(0)

            logger.info("Successfully created treemap buffer")
            return buffer

        except Exception as e:
            logger.error(f"Error creating treemap: {str(e)}")
            return None

        finally:
            if fig is not None:
                plt.close(fig)
            else:
                plt.close('all')
