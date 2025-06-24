from __future__ import annotations

from ..fastapi_classes import DiracxRouter

router = DiracxRouter(require_auth=True)


@router.get("/auth")
def test1():
    return "hello"
