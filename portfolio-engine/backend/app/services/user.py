from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create(self, data: UserCreate) -> User:
        existing_user = self.repository.get_by_email(data.email)
        if existing_user is not None:
            raise UserAlreadyExistsError(
                f"User with email '{data.email}' already exists."
            )

        hashed_password = hash_password(data.password)

        user = User(
            email=data.email,
            hashed_password=hashed_password,
            full_name=data.full_name,
            is_active=data.is_active,
            is_superuser=data.is_superuser,
        )

        return self.repository.create(user)

    def get_all(self) -> list[User]:
        return self.repository.get_all()

    def get_by_id(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        return user

    def get_by_email(self, email: str) -> User | None:
        return self.repository.get_by_email(email)

    def update(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_by_id(user_id)

        update_data = data.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing = self.repository.get_by_email(update_data["email"])
            if existing is not None and existing.id != user_id:
                raise UserAlreadyExistsError(
                    f"User with email '{update_data['email']}' already exists."
                )

        if "password" in update_data:
            plain_pwd = update_data.pop("password")
            if plain_pwd:
                user.hashed_password = hash_password(plain_pwd)

        for field, value in update_data.items():
            setattr(user, field, value)

        return self.repository.update(user)

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        self.repository.delete(user)

    def authenticate(self, email: str, password: str) -> User:
        user = self.repository.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Incorrect email or password.")

        if not user.is_active:
            raise InvalidCredentialsError("User account is inactive.")

        return user
