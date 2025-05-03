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
    version: int


class NasMethod(BaseModel):
    method: Literal[
        "login",
        "logout",
        "create",
        "rename",
        "start",
    ]


class NasSession(BaseModel):
    session: Literal["FileStation"]


class LoginNasParams(NasApi, NasVersion, NasMethod, NasSession):
    account: str
    passwd: str
    format: Literal["cookie"]


class LogoutNasParams(NasApi, NasVersion, NasMethod, NasSession):
    pass


class CreateNasParams(NasApi, NasVersion, NasMethod):
    folder_path: list[str]
    name: list[str]
    force_parent: bool = True


class MoveNasParams(NasApi, NasVersion, NasMethod):
    path: list[str]
    dest_folder_path: list[str]
    remove_src: bool = True


class DeleteNasParams(NasApi, NasVersion, NasMethod):
    path: list[str]


class RenameNasParams(NasApi, NasVersion, NasMethod):
    path: list[str]
    name: list[str]
