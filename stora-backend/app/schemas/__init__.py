"""
Schemas package – re-exports every Pydantic schema for convenient
importing: ``from app.schemas import UserCreate, TenantRead, ...``
"""

from app.schemas.user import UserCreate, UserRead, UserUpdate  # noqa: F401
from app.schemas.tenant import TenantCreate, TenantRead, TenantUpdate  # noqa: F401
from app.schemas.plan import PlanCreate, PlanRead, PlanUpdate  # noqa: F401
from app.schemas.membership import (  # noqa: F401
    MembershipCreate,
    MembershipRead,
    MembershipUpdate,
)
from app.schemas.invitation import (  # noqa: F401
    InvitationCreate,
    InvitationRead,
)
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate  # noqa: F401
from app.schemas.combo_item import (  # noqa: F401
    ComboItemCreate,
    ComboItemRead,
    ComboItemUpdate,
)
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate  # noqa: F401
from app.schemas.appointment import (  # noqa: F401
    AppointmentCreate,
    AppointmentRead,
    AppointmentUpdate,
)
from app.schemas.auth import Token, TokenData, LoginRequest  # noqa: F401
