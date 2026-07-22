from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.exception import add_exception_handlers
from app.middleware import register_middlewares
from app.modules.users.model import User  # noqa: F401
from app.router import master_router

# ANSI color helpers
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    print(f"{YELLOW}🚀 Starting server...{RESET}")
    yield
    print(f"{RED}🛑 Shutting down server...{RESET}")


description = """
### FastAPI Template.
"""

app = FastAPI(
    lifespan=lifespan,
    title="FastAPI Template",
    description=description,
    version="0.0.1",
)


app.include_router(master_router)
add_exception_handlers(app)
register_middlewares(app)
