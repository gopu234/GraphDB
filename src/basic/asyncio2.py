import asyncio
import aiohttp

def one():
    print("one")

async def fetch():
    url ="https://python.org"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"Fetched {url} with status {response.status}")
            return await response.text()

def two():
    print("two")


async def main():
    one()
    await fetch()
    two()

asyncio.run(main())