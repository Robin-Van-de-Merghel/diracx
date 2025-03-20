from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import insert, update

from diracx.core.exceptions import (
    DBInInvalidStateError,
    PilotNotFoundError
)

from ..utils import BaseSQLDB
from .schema import (
    PilotAgents,
    PilotAgentsDBBase,
    PilotRegistrations
)


class PilotAgentsDB(BaseSQLDB):
    """PilotAgentsDB class is a front-end to the PilotAgents Database."""

    metadata = PilotAgentsDBBase.metadata

    async def add_pilot_references(
        self,
        pilot_ref: list[str],
        vo: str,
        grid_type: str = "DIRAC",
        pilot_stamps: dict | None = None,
    ) -> None:

        if pilot_stamps is None:
            pilot_stamps = {}

        now = datetime.now(tz=timezone.utc)

        # Prepare the list of dictionaries for bulk insertion
        values = [
            {
                "PilotJobReference": ref,
                "VO": vo,
                "GridType": grid_type,
                "SubmissionTime": now,
                "LastUpdateTime": now,
                "Status": "Submitted",
                "PilotStamp": pilot_stamps.get(ref, ""),
            }
            for ref in pilot_ref
        ]

        # Insert multiple rows in a single execute call
        stmt = insert(PilotAgents).values(values)
        await self.conn.execute(stmt)
        return

    async def register_pilot_reference(
        self,
        pilot_ref: str,
        pilot_secret: str
    ) -> None:
        hashed_secret = hash(pilot_secret)

        stmt = update(PilotRegistrations).where(
            PilotRegistrations.pilot_secret == hashed_secret,
            PilotRegistrations.pilot_job_reference == pilot_ref
        )

        stmt.values(pilot_secret_use_count=PilotRegistrations.pilot_secret_use_count+1)

        result = await self.conn.execute(stmt)

        if result.rowcount == 0:
            raise PilotNotFoundError(
                pilot_ref=pilot_ref,
                detail="or the pilot_secret or the pilot_job_reference is wrong"
            )
        elif result.rowcount > 1:
            # Undo change
            await self.conn.commit()
            await self.conn.revert()

            raise DBInInvalidStateError(
                "PilotAgentsDB",
                "PilotRegistrations",
                "duplicates found"
            )
        return