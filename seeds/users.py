from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user import User, Role
from utils.auth import hash_password
from utils.logger import get_logger

logger = get_logger(__name__)

def seed_admin_user(db: Session):
    """Seed a default admin user if it doesn't exist."""
    logger.debug("Checking for existing admin user...")
    existing = db.query(User).filter(User.username == "admin").first()
    if existing:
        logger.info("Admin user already exists, skipping seed.")
        return

    logger.info("Creating default admin user...")
    admin_user = User(
        username="admin",
        name="Super Admin",
        email="admin@example.com",
        hashed_password=hash_password("admin123"),
        role=Role.admin  # Use enum value
    )

    try:
        db.add(admin_user)
        db.commit()
        logger.info("✅ Default admin user created.")
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Failed to create admin user: {e}")
        raise