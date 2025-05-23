from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from utils.logger import get_logger
from routes import movement, client, login, branch, stock, product, health, user
from db.base import Base, engine
from seeds.users import seed_admin_user
from db.base import SessionLocal


logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Create tables on startup
    logger.info("Creating tables on startup")
    Base.metadata.create_all(bind=engine)

    # 🔥 Seeding logic
    logger.info("Seeding logic")
    db = SessionLocal()
    try:
        logger.info("before seed_admin_user")
        seed_admin_user(db)
        logger.info("after seed_admin_user")
    finally:
        db.close()

    yield

app = FastAPI(
    title="Inventory & Branch Management API",
    description="""
This API powers a multi-branch inventory management system.

Features:
- 🔐 User authentication with roles (admin, user)
- 📦 CRUD for products and real-time stock
- 🧍 CRUD for clients
- 🔁 Stock transfers between branches
- 🌐 Multi-branch visibility and control
""",
    version="1.0.0",
    contact={
        "name": "J&T",
        "url": "https://ourdomain.com",
        "email": "support@ourdomain.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",      # Swagger UI (default)
    redoc_url="/redoc",    # ReDoc UI
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Frontend's domain
    allow_credentials=True,  # Allow cookies or auth headers
    allow_methods=["*"],     # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Allow all headers
)

app.include_router(health.router)
app.include_router(login.router)
app.include_router(product.router)
app.include_router(stock.router)
app.include_router(user.router)
app.include_router(client.router)
app.include_router(movement.router)
app.include_router(branch.router)
