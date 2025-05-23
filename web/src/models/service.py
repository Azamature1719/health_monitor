from src.database import Model
from sqlalchemy.orm import Mapped, mapped_column

class ServiceOrm(Model):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 