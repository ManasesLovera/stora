"""
Routers package – collects all endpoint routers into a single
``api_router`` that is mounted by the main application.
"""

from fastapi import APIRouter

from app.routers.appointments import router as appointments_router
from app.routers.auth import router as auth_router
from app.routers.combo_items import router as combo_items_router
from app.routers.invitations import router as invitations_router
from app.routers.memberships import router as memberships_router
from app.routers.orders import router as orders_router
from app.routers.plans import router as plans_router
from app.routers.products import router as products_router
from app.routers.tenants import router as tenants_router
from app.routers.users import router as users_router

api_router = APIRouter()

# Register every sub-router under a common prefix.
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(plans_router, prefix="/plans", tags=["Plans"])
api_router.include_router(tenants_router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(
    memberships_router, prefix="/memberships", tags=["Memberships"]
)
api_router.include_router(
    invitations_router, prefix="/invitations", tags=["Invitations"]
)
api_router.include_router(products_router, prefix="/products", tags=["Products"])
api_router.include_router(
    combo_items_router, prefix="/combo-items", tags=["Combo Items"]
)
api_router.include_router(orders_router, prefix="/orders", tags=["Orders"])
api_router.include_router(
    appointments_router, prefix="/appointments", tags=["Appointments"]
)
