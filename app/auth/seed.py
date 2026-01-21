import os 

from flask import current_app

from app.auth.services import create_user_in_db
from app.models import User


DEV_USER_EMAIL = os.getenv("DEV_USER_EMAIL")
DEV_USER_PASSWORD = os.getenv("DEV_USER_PASSWORD")
DEV_USER_NAME = os.getenv("DEV_USER_NAME")
SEED_USER = os.getenv("SEED_USER", "False")


def seed_dev_user():
    logger = current_app.logger

    if not SEED_USER.lower() == "true":
        logger.info(
            "SEED_USER is not set to True. Skipping seed user creation..."
        )
        return
    
    user = User.query.filter_by(email=DEV_USER_EMAIL).first()
    if user:
        logger.info(f"Dev user already exists: {DEV_USER_EMAIL}")
        return

    success, message, _ = create_user_in_db(
        name=DEV_USER_NAME, 
        email=DEV_USER_EMAIL, 
        password=DEV_USER_PASSWORD
    )
    if not success:
        logger.error(f"seed_dev_user failed: {message}")
        return
    logger.info(f"seed_dev_user success: {message}")