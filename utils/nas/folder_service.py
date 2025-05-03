import json
from typing import Literal
from utils.nas.integration import NasIntegration
from utils.nas.decorator import require_nas_login
from utils.error.custom_error import NasIntegrationError
from src.schema.nas_params import (
    CreateNasParams,
    MoveNasParams,
    DeleteNasParams,
    RenameNasParams,
)


class NasFolderService:
    def __init__(self, nas: NasIntegration):
        self.nas = nas

    def _is_equal(
        self, method: Literal["create", "rename", "move"], payload: dict
    ) -> None:
        equal_length_pairs = {
            "create": ["folder_path", "name"],
            "rename": ["path", "name"],
            "move": ["path", "dest_folder_path"],
        }

        if method in equal_length_pairs:
            key1, key2 = equal_length_pairs[method]
            if len(payload.get(key1, [])) != len(payload.get(key2, [])):
                raise NasIntegrationError(
                    detail=f"Length of '{key1}' and '{key2}' must be equal."
                )

    def _is_started_with_slash(self, payload: dict) -> None:
        keys_to_check = ["folder_path", "path", "source", "dest", "dest_folder_path"]
        for key in keys_to_check:
            if key in payload:
                for val in payload[key]:
                    if not val.startswith("/"):
                        raise NasIntegrationError(
                            detail=f"All values in '{key}' must start with '/'. Invalid value: {val}"
                        )

    def _is_unique(self, name: list[str]) -> None:
        if len(name) != len(set(name)):
            raise NasIntegrationError(detail="All names must be unique.")
        return None

    @require_nas_login
    async def create_folder(
        self, folder_path: list[str], name: list[str], force_parent: bool = True
    ) -> None:
        params = CreateNasParams(
            api="SYNO.FileStation.CreateFolder",
            version=2,
            method="create",
            folder_path=folder_path,
            name=name,
            force_parent=force_parent,
        )

        payload = params.model_dump()
        payload["folder_path"] = json.dumps(folder_path)
        payload["name"] = json.dumps(name)
        self._is_equal("create", params.model_dump())
        self._is_started_with_slash(params.model_dump())
        self._is_unique(name)
        await self.nas.send_request(api=params.api, params=payload, sid=self.nas.sid)
        return None

    @require_nas_login
    async def move_folder(
        self, path: list[str], dest_folder_path: list[str], remove_src: bool = True
    ) -> None:
        params = MoveNasParams(
            api="SYNO.FileStation.CopyMove",
            version=3,
            method="start",
            path=path,
            dest_folder_path=dest_folder_path,
            remove_src=remove_src,
        )

        payload = params.model_dump()
        payload["path"] = json.dumps(path)
        payload["dest_folder_path"] = json.dumps(dest_folder_path)
        self._is_equal("move", params.model_dump())
        self._is_started_with_slash(params.model_dump())
        await self.nas.send_request(api=params.api, params=payload, sid=self.nas.sid)
        return None

    @require_nas_login
    async def delete_folder(self, path: list[str]) -> None:
        params = DeleteNasParams(
            api="SYNO.FileStation.Delete", version=2, method="start", path=path
        )

        payload = params.model_dump()
        payload["path"] = json.dumps(path)
        self._is_started_with_slash(params.model_dump())
        await self.nas.send_request(api=params.api, params=payload, sid=self.nas.sid)
        return None

    @require_nas_login
    async def rename_folder(self, path: list[str], name: list[str]) -> None:
        params = RenameNasParams(
            api="SYNO.FileStation.Rename",
            version=2,
            method="rename",
            path=path,
            name=name,
        )

        payload = params.model_dump()
        payload["path"] = json.dumps(path)
        payload["name"] = json.dumps(name)
        self._is_equal("rename", params.model_dump())
        self._is_started_with_slash(params.model_dump())
        self._is_unique(name)
        await self.nas.send_request(api=params.api, params=payload, sid=self.nas.sid)
        return None
