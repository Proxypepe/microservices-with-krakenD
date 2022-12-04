import functools
import httpx


class HTTPError(Exception):

    def __init__(self, message):
        self.message = message

    @property
    def message(self):
        return self.message


class HTTPContent(HTTPError):
    ...


class HTTPStatus(HTTPError):
    ...


def HTTP_handler(logger):
    def decorator(task):
        async def wrapper(*args, **kwargs):
            try:
                await task()
                logger.debug('Service is healthy')
                print('Service is healthy')
            except httpx.RequestError as exc:
                logger.error(f"Произошла ошибка при запросе {exc.request.url!r}.")
            except httpx.HTTPStatusError as exc:
                logger.error(f"Ошибочный код запроса {exc.response.status_code} при выполнени запроса {exc.request.url!r}.")
            except HTTPContent as e:
                logger.error(e.message)
            except HTTPError as e:
                logger.error(e.message)
        return wrapper
    return decorator
