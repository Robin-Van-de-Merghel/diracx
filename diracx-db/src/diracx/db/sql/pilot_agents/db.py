from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from diracx.core.exceptions import (
    AuthorizationError,
    PilotAlreadyExistsError,
    PilotNotFoundError,
)

from ..utils import BaseSQLDB
from .schema import PilotAgents, PilotAgentsDBBase, PilotRegistrations


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

        # Insert multiple rows in a single execute call and use 'returning' to get primary keys
        stmt = insert(PilotAgents).values(values)  # Assuming 'id' is the primary key

        await self.conn.execute(stmt)

    async def increment_pilot_secret_use(
        self,
        pilot_id: int,
    ) -> None:

        #  Prepare the update statement
        stmt = (
            update(PilotRegistrations)
            .values(
                pilot_secret_use_count=PilotRegistrations.pilot_secret_use_count + 1
            )
            .where(PilotRegistrations.pilot_id == pilot_id)
        )

        # Execute the update using the connection
        res = await self.conn.execute(stmt)

        if res.rowcount == 0:
            raise PilotNotFoundError(pilot_id=pilot_id)

    async def verify_pilot_secret(
        self, pilot_job_reference: str, pilot_hashed_secret: str
    ) -> None:

        try:
            pilot = await self.get_pilot_by_reference(pilot_job_reference)
        except NoResultFound as e:
            raise PilotNotFoundError(pilot_ref=pilot_job_reference) from e

        pilot_id = pilot["PilotID"]

        stmt = (
            select(PilotRegistrations)
            .with_for_update()
            .where(PilotRegistrations.pilot_hashed_secret == pilot_hashed_secret)
            .where(PilotRegistrations.pilot_id == pilot_id)
            .where(
                PilotRegistrations.pilot_secret_expiration_date
                > datetime.now(tz=timezone.utc)
            )
        )

        # Execute the request
        res = await self.conn.execute(stmt)

        result = res.fetchone()

        if result is None:
            raise AuthorizationError(
                detail="bad pilot_id / pilot_secret or secret has expired"
            )

        # Increment the count
        await self.increment_pilot_secret_use(pilot_id=pilot_id)

    async def add_pilot_credentials(
        self, pilot_id: int, pilot_hashed_secret: str
    ) -> datetime:

        stmt = insert(PilotRegistrations).values(
            pilot_id=pilot_id, pilot_hashed_secret=pilot_hashed_secret
        )

        try:
            await self.conn.execute(stmt)
        except IntegrityError as e:
            if "foreign key" in str(e.orig).lower():
                raise PilotNotFoundError(pilot_id=pilot_id) from e
            if "duplicate entry" in str(e.orig).lower():
                raise PilotAlreadyExistsError(
                    pilot_id=pilot_id, detail="this pilot has already credentials"
                ) from e

        added_creds = await self.get_pilot_creds_by_id(pilot_id)

        return added_creds["PilotSecretCreationDate"]

    async def set_pilot_credentials_expiration(
        self, pilot_id: int, pilot_secret_expiration_date: DateTime
    ):
        #  Prepare the update statement
        stmt = (
            update(PilotRegistrations)
            .values(pilot_secret_expiration_date=pilot_secret_expiration_date)
            .where(PilotRegistrations.pilot_id == pilot_id)
        )

        await self.conn.execute(stmt)

    async def fetch_all_pilots(self):
        stmt = select(PilotRegistrations).with_for_update()
        result = await self.conn.execute(stmt)

        # Convert results into a dictionary
        pilots = [dict(row._mapping) for row in result]

        return pilots

    async def get_pilot_by_reference(self, pilot_ref: str):
        stmt = (
            select(PilotAgents)
            .with_for_update()
            .where(PilotAgents.pilot_job_reference == pilot_ref)
        )

        # We assume it is unique...
        return dict((await self.conn.execute(stmt)).one()._mapping)

    async def get_pilot_creds_by_id(self, pilot_id: int):
        stmt = (
            select(PilotRegistrations)
            .with_for_update()
            .where(PilotRegistrations.pilot_id == pilot_id)
        )

        return dict((await self.conn.execute(stmt)).one()._mapping)
