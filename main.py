import asyncio
import logging
from core.main import start_bot

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

async def main():
    await start_bot()


if __name__ == '__main__':
    asyncio.run(main())
