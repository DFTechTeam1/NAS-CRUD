from fastapi import APIRouter, status
from src.schema.response import ResponseDefault
from src.schema.request_format import DeleteFolder
from utils.logger import logging
from utils.error.custom_error import NAS
from utils.nas.integration import NasIntegration
from utils.nas.folder_service import NasFolderService
from utils.nas.auth_service import NasAuthService

router = APIRouter(tags=["Directory Management"])


async def delete_directory(schema: DeleteFolder) -> ResponseDefault:
    logging.info("Endpoint delete.")
    response = ResponseDefault()
    nas = NasIntegration(schema.ip_address)
    auth_service = NasAuthService(nas)
    file_service = NasFolderService(nas)
    try:
        await auth_service.login()
        await file_service.delete_folder(path=schema.path)
        response.message = "Directory successfully deleted."
    except NAS:
        raise
    finally:
        await auth_service.logout()
    return response


router.add_api_route(
    methods=["POST"],
    path="/nas/delete",
    endpoint=delete_directory,
    summary="Delete existing directory on NAS.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDefault,
)
