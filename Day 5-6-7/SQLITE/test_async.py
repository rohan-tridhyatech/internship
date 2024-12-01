import asyncio

async def main():
    print("Hello...")
    await asyncio.sleep(6)  # Simulate an asynchronous task
    print("World!")

asyncio.run(main())
