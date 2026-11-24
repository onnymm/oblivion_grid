from __future__ import annotations
from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import false
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class TRANSITIVE_MODEL_NAME:
    ROLE__PERMISSIONS = "role_permissions"
    ROLE__RECORD_RULES = "role_record_rules"

class MODEL_NAME:
    USERS = "users"
    ROLES = "roles"
    PERMISSIONS = "permissions"
    RECORD_RULES = "record_rules"
    ALLIANCES = "alliances"
    PLAYERS = "players"
    PLANETS = "planets"
    COORDINATES = "coordinates"

class _Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key= True, autoincrement= True)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    creator_id: Mapped[int | None] = mapped_column(ForeignKey(f"{MODEL_NAME.USERS}.id"))

    @declared_attr
    def create_uid(cls) -> Mapped[Model.User | None]:
        return relationship("User", foreign_keys=lambda: [cls.creator_id], remote_side="User.id")

class _OperationPermissions:
    can_create: Mapped[bool] = mapped_column(Boolean, server_default= false())
    can_write: Mapped[bool] = mapped_column(Boolean, server_default= false())
    can_modify: Mapped[bool] = mapped_column(Boolean, server_default= false())
    can_delete: Mapped[bool] = mapped_column(Boolean, server_default= false())

class TransitiveModel:

    role_permissions = Table(
        TRANSITIVE_MODEL_NAME.ROLE__PERMISSIONS,
        _Base.metadata,
        Column("role_id", ForeignKey(f"{MODEL_NAME.ROLES}.id"), primary_key= True),
        Column("permission_id", ForeignKey(F"{MODEL_NAME.PERMISSIONS}.id"), primary_key= True),
    )

    role_record_rules = Table(
        TRANSITIVE_MODEL_NAME.ROLE__RECORD_RULES,
        _Base.metadata,
        Column("role_id", ForeignKey(f"{MODEL_NAME.ROLES}.id"), primary_key= True),
        Column("record_rule_id", ForeignKey("record_rules.id"), primary_key= True),
    )

# Modelos de datos
class Model:

    class User(_Base):
        __tablename__ = MODEL_NAME.USERS

        nickname: Mapped[str] = mapped_column(String(255))
        galaxy_life_id: Mapped[int] = mapped_column(Integer)
        profile_picture: Mapped[str | None] = mapped_column(Text)
        role_id: Mapped[int] = mapped_column(ForeignKey(f"{MODEL_NAME.ROLES}.id", name="fk_users_role"))
        alliance_id: Mapped[int | None] = mapped_column(ForeignKey(f"{MODEL_NAME.ALLIANCES}.id", name="fk_users_alliance"))

        role: Mapped[Model.Role] = relationship("Role", foreign_keys=[role_id], back_populates= MODEL_NAME.USERS)
        alliance: Mapped[Model.Alliance | None] = relationship("Alliance", foreign_keys=[alliance_id], back_populates= MODEL_NAME.USERS)


    class Role(_Base):
        __tablename__ = MODEL_NAME.ROLES

        name: Mapped[str] = mapped_column(String(255))
        users: Mapped[list[Model.User]] = relationship("User", foreign_keys="User.role_id", back_populates="role")
        permissions: Mapped[list[Model.Permission]] = relationship("Permission",
            secondary= TransitiveModel.role_permissions, back_populates= MODEL_NAME.ROLES
        )
        record_rules: Mapped[list[Model.RecordRule]] = relationship("RecordRule",
            secondary= TransitiveModel.role_record_rules, back_populates= MODEL_NAME.ROLES
        )

    class Permission(_OperationPermissions, _Base):
        __tablename__ = MODEL_NAME.PERMISSIONS

        name: Mapped[str] = mapped_column(String(255))
        table_name: Mapped[str] = mapped_column(String(255))
        roles: Mapped[list[Model.Role]] = relationship("Role",
            secondary= TransitiveModel.role_permissions, back_populates= MODEL_NAME.PERMISSIONS
        )


    class RecordRule(_OperationPermissions, _Base):
        __tablename__ = MODEL_NAME.RECORD_RULES

        name: Mapped[str] = mapped_column(String(255))
        criteria: Mapped[str] = mapped_column(Text)
        roles: Mapped[list[Model.Role]] = relationship("Role",
            secondary= TransitiveModel.role_record_rules, back_populates= MODEL_NAME.RECORD_RULES
        )


    class Alliance(_Base):
        __tablename__ = MODEL_NAME.ALLIANCES

        name: Mapped[str] = mapped_column(String(255))
        emblem: Mapped[str | None] = mapped_column(Text)
        members: Mapped[list[Model.Player]] = relationship("Player", back_populates="alliance")
        users: Mapped[list[Model.User]] = relationship("User", foreign_keys="User.alliance_id", back_populates="alliance")


    class Player(_Base):
        __tablename__ = MODEL_NAME.PLAYERS

        name: Mapped[str] = mapped_column(String(255))
        galaxy_life_id: Mapped[str] = mapped_column(String(255))
        profile_picture: Mapped[str | None] = mapped_column(Text)
        alliance_id: Mapped[int | None] = mapped_column(ForeignKey(f"{MODEL_NAME.ALLIANCES}.id"))

        alliance: Mapped[Model.Alliance | None] = relationship("Alliance", back_populates="members")
        planets: Mapped[list[Model.Planet]] = relationship("Planet", back_populates="owner")


    class Planet(_Base):
        __tablename__ = MODEL_NAME.PLANETS

        number: Mapped[int] = mapped_column(server_default="0")
        color: Mapped[str] = mapped_column(String(255))
        star_base_level: Mapped[int]
        owner_id: Mapped[int] = mapped_column(ForeignKey(f"{MODEL_NAME.PLAYERS}.id"))

        owner: Mapped[Model.Player] = relationship("Player", back_populates= MODEL_NAME.PLANETS)
        coordinates: Mapped[list[Model.Coordinate]] = relationship("Coordinate", back_populates="planet")


    class Coordinate(_Base):
        __tablename__ = MODEL_NAME.COORDINATES

        x: Mapped[int]
        y: Mapped[int]
        planet_id: Mapped[int] = mapped_column(ForeignKey(f"{MODEL_NAME.PLANETS}.id"))
        added_by_id: Mapped[int] = mapped_column(ForeignKey(f"{MODEL_NAME.USERS}.id"))

        added_by: Mapped[Model.User] = relationship("User", foreign_keys=[added_by_id])
        planet: Mapped[Model.Planet] = relationship("Planet", back_populates= MODEL_NAME.COORDINATES)
