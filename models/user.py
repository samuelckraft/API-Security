from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash

class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[str] = mapped_column(db.ForeignKey('employees.id'))
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255))