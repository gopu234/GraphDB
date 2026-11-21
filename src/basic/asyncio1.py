import asyncio

async def one():
    print("one")

async def two():
    print("two")
    await asyncio.sleep(3)
    print("two finished after 3 sec")

async def three():
    print("three")
    await asyncio.sleep(2)
    print("three finished after 2 sec")

def four():
    print("four")

async def main():
    await asyncio.gather(one(), two(), three())


asyncio.run(main())