from typing import Literal
from pydantic import BaseModel


class NasApi(BaseModel):
    api: Literal[
        "SYNO.API.Auth",
        "SYNO.FileStation.CreateFolder",
        "SYNO.FileStation.Rename",
        "SYNO.FileStation.Delete",
        "SYNO.FileStation.Delete",
        "SYNO.FileStation.List",
        "SYNO.FileStation.CopyMove",
    ]


class NasVersion(BaseModel):
    version: int = None


class NasMethod(BaseModel):
    method: Literal[
        "login",
        "logout",
        "query",
        "list_share",
        "create",
        "rename",
        "start",
        "status",
    ]


class NasSession(BaseModel):
    session: Literal["FileStation"]


class LoginNasParams(NasApi, NasVersion, NasMethod, NasSession):
    account: str = None
    passwd: str = None
    format: Literal["cookie"]


class LogoutNasParams(NasApi, NasVersion, NasMethod, NasSession):
    pass
