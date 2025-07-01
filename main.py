import asyncio
from pyrogram import Client
from services.prices import CryptoPriceFetcher
from config import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID
from services.treemap import CryptoTreeMap
from utils.logger import logger
import tgcrypto

fetcher = CryptoPriceFetcher()
tm = CryptoTreeMap()


async def send_daily_crypto_market_updates(client):
    try:
        logger.info("Preparing to send daily crypto market updates")

        treemap_buffer = tm.create_treemap_buffer()
        if treemap_buffer is None:
            logger.error("Failed to generate treemap")
            return False

        price_keyboard = fetcher.generate_price_keyboard()
        if price_keyboard is None:
            logger.warning("Failed to generate price keyboard, sending without keyboard")

        await client.send_photo(
            chat_id=CHANNEL_ID,
            photo=treemap_buffer,
            reply_markup=price_keyboard
        )

        logger.info("Daily crypto market updates sent successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to send daily crypto market updates: {str(e)}")
        return False


async def main():
    client = None
    try:
        logger.info("Starting treemap generator bot")

        if not all([API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID]):
            logger.error("Missing required configuration variables")
            return

        client = Client(
            "treemap_generator",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN
        )

        async with client:
            success = await send_daily_crypto_market_updates(client)
            if not success:
                logger.warning("Initial update failed, but continuing...")

            while True:
                try:
                    logger.info("Waiting for next update cycle (24 hours)")
                    await asyncio.sleep(86400)

                    success = await send_daily_crypto_market_updates(client)
                    if not success:
                        logger.warning("Update cycle failed, will retry in next cycle")

                except KeyboardInterrupt:
                    logger.info("Received shutdown signal")
                    break
                except Exception as e:
                    logger.error(f"Error in update cycle: {str(e)}")
                    logger.info("Waiting before retry...")
                    await asyncio.sleep(3600)

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error in main bot execution: {str(e)}")
    finally:
        if client:
            logger.info("Cleaning up client connection")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
