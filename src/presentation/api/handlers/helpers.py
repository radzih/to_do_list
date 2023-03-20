from base64 import b64decode, b64encode
from typing import TypeVar
from zlib import compress, decompress

from fastapi import Request, Response, status
from fastapi.datastructures import URL
from fastapi.exceptions import HTTPException

from src.presentation.api.handlers import responses

PAGE_SIZE = 1
DEFAULT_OFFSET = 0

Model = TypeVar("Model")


def decode_cursor(encoded_cursor: str) -> tuple[int | str]:
    decoded = decompress(b64decode(encoded_cursor))
    return tuple(int(val) if val.isdigit() else val for val in decoded.split())


def encode_cursor(decoded_cursor: str | int) -> str:
    encoded = b64encode(compress(str(decoded_cursor).encode()))
    return encoded.decode()


def create_uri_with_cursor(
    decoded_cursor: str | int | None, url: URL
) -> URL | None:
    if decoded_cursor is None:
        return
    encoded_cursor = encode_cursor(decoded_cursor)
    uri = url.replace_query_params(cursor=encoded_cursor)
    return uri._url


class PaginationService:
    def __init__(
        self, request: Request, response: Response, cursor: str | None = None
    ) -> None:
        self.request = request
        self.response = response
        self.cursor = cursor
        self.offset = None
        self.limit = PAGE_SIZE

    def get_offset_limit(self) -> tuple[int, int]:
        if not self.cursor:
            self.cursor = encode_cursor(DEFAULT_OFFSET)
        try:
            self.offset = decode_cursor(self.cursor)[0]
        # I know its bad
        # TODO: fix except exception
        except Exception:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        "loc": ["query", "cursor"],
                        "msg": "invalid cursor",
                        "type": "value_error",
                    }
                ],
            )

        return self.offset, self.limit

    def paginate_response(self, data: list[Model]) -> responses.Paginated:
        next_cursor_decoded = (
            self.offset + self.limit if len(data) == self.limit else None
        )
        previous_cursor_decoded = (
            self.offset - self.limit if self.offset > 0 else None
        )

        next_uri = create_uri_with_cursor(
            next_cursor_decoded, self.request.url
        )
        previous_uri = create_uri_with_cursor(
            previous_cursor_decoded, self.request.url
        )

        return responses.Paginated[Model](
            next=next_uri,
            previous=previous_uri,
            data=data,
        )
