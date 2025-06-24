from __future__ import annotations

from ..fastapi_classes import DiracxRouter
from .test_with_auth import router as router_with_auth
from .test_without_auth import router as router_without_auth

router = DiracxRouter(require_auth=True)
router.include_router(router_without_auth)
router.include_router(router_with_auth)
