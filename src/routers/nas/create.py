from fastapi import APIRouter, status
from src.schema.response import ResponseDefault
from src.schema.request_format import CreateFolder
from utils.logger import logging
from utils.error.custom_error import NAS
from utils.nas.integration import NasIntegration
from utils.nas.folder_service import NasFolderService
from utils.nas.auth_service import NasAuthService

router = APIRouter(tags=["Directory Management"])


async def create_directory(schema: CreateFolder) -> ResponseDefault:
    logging.info("Endpoint create.")
    response = ResponseDefault()
    nas = NasIntegration(schema.ip_address)
    auth_service = NasAuthService(nas)
    file_service = NasFolderService(nas)
    try:
        await auth_service.login()
        await file_service.create_folder(
            folder_path=schema.folder_path,
            name=schema.name,
            force_parent=True,
        )
        response.message = "Directory successfully created."
    except NAS:
        raise
    finally:
        await auth_service.logout()
    return response


router.add_api_route(
    methods=["POST"],
    path="/create",
    endpoint=create_directory,
    summary="Create new directory on NAS.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
