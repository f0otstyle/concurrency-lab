import asyncio
import time

from fastapi import FastAPI

app = FastAPI(title="Concurrency Lab Server")

MAX_DELAY = 30


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/delay/{seconds}")
async def delay(seconds: float) -> dict[str, float | str]:
    """Неблокирующая задержка: корутина отдаёт управление event loop."""
    seconds = min(seconds, MAX_DELAY)
    await asyncio.sleep(seconds)
    return {"slept": seconds, "mode": "async"}


@app.get("/blocking/{seconds}")
async def blocking(seconds: float) -> dict[str, float | str]:
    """Блокирующая задержка: поток встаёт, event loop не крутит другие задачи."""
    seconds = min(seconds, MAX_DELAY)
    time.sleep(seconds)
    return {"slept": seconds, "mode": "blocking"}
