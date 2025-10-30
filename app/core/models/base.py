from sqlalchemy.orm import declarative_base, Mapped, mapped_column, declared_attr
from app.utils.case_converter import camel_to_snake_case

class Base(declarative_base):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{camel_to_snake_case(cls.__name__)}s'

    id: Mapped[int] = mapped_column(primary_key=True)

