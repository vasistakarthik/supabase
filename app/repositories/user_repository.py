
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    # Find user by email
    def get_user_by_email(
        self,
        db: Session,
        email: str
    ):

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    # Create a new user
    def create_user(
        self,
        db: Session,
        user_data: dict
    ):

        user = User(**user_data)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user


user_repository = UserRepository()
