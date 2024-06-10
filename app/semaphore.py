import asyncio

semaphore = asyncio.Semaphore(5)

async def with_semaphore():
    async with semaphore:
        yield
