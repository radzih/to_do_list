from fastapi import Request, status
from fastapi.responses import ORJSONResponse

from src.core.application.user import exceptions
from src.presentation.api.handlers import responses


async def user_not_exists(request: Request, err: exceptions.UserNotExists):
    return ORJSONResponse(
        responses.ErrorResult(message=err.message, data=err),
        status.HTTP_404_NOT_FOUND,
    )


async def user_already_exists(
    request: Request, err: exceptions.UserAlreadyExists
):
    return ORJSONResponse(
        responses.ErrorResult(message=err.message, data=err),
        status.HTTP_409_CONFLICT,
    )
