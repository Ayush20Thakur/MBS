import pytest
import asyncio

@pytest.mark.asyncio
async def test_concurrency_lock_isolation():
    lock = asyncio.Lock()
    counter = 0

    async def increment():
        nonlocal counter
        async with lock:
            temp = counter
            await asyncio.sleep(0.01)
            counter = temp + 1

    await asyncio.gather(increment(), increment(), increment())
    assert counter == 3
