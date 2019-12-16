import pytest
import asyncio


@pytest.yield_fixture
def event_loop():
    return asyncio.get_event_loop()
