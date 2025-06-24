from __future__ import annotations

from ..fastapi_classes import DiracxRouter

router = DiracxRouter(require_auth=False)


@router.get("/without-auth")
def test1():
    return "hello"
