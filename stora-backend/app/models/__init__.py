"""
Models package – re-exports every ORM model so that
``from app.models import User, Tenant, ...`` works.

Importing all models here also guarantees they are registered on
``Base.metadata`` before any table-creation or migration step.
"""

from app.models.user import User  # noqa: F401
from app.models.tenant import Tenant  # noqa: F401
from app.models.plan import Plan  # noqa: F401
from app.models.membership import Membership  # noqa: F401
from app.models.invitation import Invitation  # noqa: F401
from app.models.product import Product  # noqa: F401
from app.models.combo_item import ComboItem  # noqa: F401
from app.models.order import Order  # noqa: F401
from app.models.appointment import Appointment  # noqa: F401
