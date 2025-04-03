import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Bot.core.main import start_bot


async def main():
    asyncio.run(await start_bot())


if __name__ == '__main__':
    asyncio.run(main())
