from typing import Literal
from pydantic import BaseModel


class WhitelistAddress(BaseModel):
    ip_address: Literal[
        "192.168.100.101",
        "192.168.100.102",
        "192.168.100.103",
        "192.168.100.104",
        "192.168.100.105",
    ]


class CreateFolder(WhitelistAddress):
    folder_path: list[str]
    name: list[str]


class MoveFolder(WhitelistAddress):
    path: list[str]
    dest_folder_path: list[str]


class DeleteFolder(WhitelistAddress):
    path: list[str]


class RenameFolder(WhitelistAddress):
    path: list[str]
    name: list[str]
