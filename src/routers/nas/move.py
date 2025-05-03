from fastapi import APIRouter, status
from src.schema.response import ResponseDefault
from src.schema.request_format import MoveFolder
from utils.logger import logging
from utils.error.custom_error import NAS
from utils.nas.integration import NasIntegration
from utils.nas.folder_service import NasFolderService
from utils.nas.auth_service import NasAuthService

router = APIRouter(tags=["Directory Management"])


async def move_directory(schema: MoveFolder) -> ResponseDefault:
    logging.info("Endpoint move.")
    response = ResponseDefault()
    nas = NasIntegration(schema.ip_address)
    auth_service = NasAuthService(nas)
    file_service = NasFolderService(nas)
    try:
        await auth_service.login()
        await file_service.move_folder(
            path=schema.path, dest_folder_path=schema.dest_folder_path
        )
        response.message = "Directory successfully moved."
    except NAS:
        raise
    finally:
        await auth_service.logout()
    return response


router.add_api_route(
    methods=["POST"],
    path="/move",
    endpoint=move_directory,
    summary="Move directory on NAS.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
