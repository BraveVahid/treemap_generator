import asyncio
from pyrogram import Client
from services.prices import CryptoPriceFetcher
from config import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID
from services.treemap import CryptoTreeMap
from utils.logger import logger

fetcher = CryptoPriceFetcher()
tm = CryptoTreeMap()


async def send_daily_crypto_market_updates(client):
    try:
        logger.info("Preparing to send daily treemap_generator market updates")
        await client.send_photo(
            chat_id=CHANNEL_ID,
            photo=tm.create_treemap_buffer(),
            reply_markup=fetcher.generate_price_keyboard()
        )
        logger.info("Daily treemap_generator market updates sent successfully")
    except Exception as e:
        logger.error(f"Failed to send daily treemap_generator market updates: {str(e)}")


async def main():
    try:
        logger.info("Starting treemap_generator bot")
        client = Client("treemap_generator", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

        async with client:
            while True:
                try:
                    await send_daily_crypto_market_updates(client)
                    logger.info("Waiting for next update cycle (24 hours)")
                    await asyncio.sleep(86400)
                except Exception as e:
                    logger.error(f"Error in update cycle: {str(e)}")
                    await asyncio.sleep(86400)

    except Exception as e:
        logger.error(f"Fatal error in main bot execution: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
