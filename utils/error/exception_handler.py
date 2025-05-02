from fastapi import status, FastAPI
from utils.error.custom_error import (
    NAS,
    DataNotFoundError,
    ServicesConnectionError,
    DatabaseQueryError,
    NasIntegrationError,
    AccessUnauthorized,
    create_exception_handler,
)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=NAS,
        handler=create_exception_handler(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail_message="A service seems to be down, try again later.",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=DataNotFoundError,
        handler=create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail_message="File or data not found.",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=ServicesConnectionError,
        handler=create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail_message="Service currently not available.",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=DatabaseQueryError,
        handler=create_exception_handler(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail_message="Invalid database query.",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=NasIntegrationError,
        handler=create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail_message="Request into NAS not eligible.",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=AccessUnauthorized,
        handler=create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            detail_message="Blacklist certain IP address to access the service.",
        ),
    )

    return None
