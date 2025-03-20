from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field

from diracx.db.sql import PilotAgentsDB as _PilotAgentsDB

PilotAgentsDB = Annotated[_PilotAgentsDB, Depends(_PilotAgentsDB.transaction)]
