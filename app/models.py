from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship


# Таблица связи многие ко многим: User <-> Role
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('role_id', ForeignKey('roles.id'))
)


# Таблица связи многие ко многим: Role <-> Permission
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column('role_id', ForeignKey('roles.id')),
    Column('permission_id', ForeignKey('permissions.id'))
)

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный Id
    fullname = Column(String, nullable=False)  # ФИО
    email = Column(String, unique=True, nullable=False, index=True)  # email (логин)
    password_hash = Column(String, nullable=False)  # хэш пароля
    is_active = Column(Boolean, default=True)  # активен ли аккаунт

    # Связь: у пользователя может быть несколько ролей
    roles = relationship("Role", secondary=user_roles, back_populates="users")

# Модель роли
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True,)
    name = Column(String, unique=True)  # Название роли

    # Обратные связи
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")


# Модель разрешений
class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True,)
    resource = Column(String, nullable=False)  # Название ресурса
    action = Column(String, nullable=False)  # Действие

    # Обратная связь: какое разрешение к какой роли отнсотится
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")






