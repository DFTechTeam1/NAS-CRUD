from fastapi import APIRouter, status
from src.schema.response import ResponseDefault
from src.schema.request_format import RenameFolder
from utils.logger import logging
from utils.error.custom_error import NAS
from utils.nas.integration import NasIntegration
from utils.nas.folder_service import NasFolderService
from utils.nas.auth_service import NasAuthService

router = APIRouter(tags=["Directory Management"])


async def rename_directory(schema: RenameFolder) -> ResponseDefault:
    logging.info("Endpoint rename.")
    response = ResponseDefault()
    nas = NasIntegration(schema.ip_address)
    auth_service = NasAuthService(nas)
    file_service = NasFolderService(nas)
    try:
        await auth_service.login()
        await file_service.rename_folder(path=schema.path, name=schema.name)
        response.message = "Directory successfully renamed."
    except NAS:
        raise
    finally:
        await auth_service.logout()
    return response


router.add_api_route(
    methods=["POST"],
    path="/rename",
    endpoint=rename_directory,
    summary="Rename existing directory on NAS.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
