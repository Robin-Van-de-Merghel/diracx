from __future__ import annotations

from datetime import datetime
from http import HTTPStatus
from typing import Annotated, Any

from fastapi import HTTPException, Query, status

from diracx.core.exceptions import DBInInvalidStateError, PilotNotFoundError

from ..dependencies import PilotAgentsDB
from ..fastapi_classes import DiracxRouter

# Import the router
router = DiracxRouter()


@router.post("/register", status_code=201)
async def register_pilot_reference(
    pilot_db: PilotAgentsDB,
    pilot_stamp: Annotated[str, Query(max_length=32)],  # Arbitrary length
    pilot_secret: Annotated[str, Query(max_length=32)],  # Arbitrary length
):
    if pilot_stamp is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pilot Stamp must be defined",
        )

    if pilot_secret is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pilot Secret mus be defined",
        )
    try:
        await pilot_db.add_pilot_secret(
            pilot_secret=pilot_secret, 
            pilot_stamp=pilot_secret
        )
    except PilotNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.args[0]
        )
    except DBInInvalidStateError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.args[0]
        )
    
    # TODO: Return token