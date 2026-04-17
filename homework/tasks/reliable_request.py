import abc
import asyncio
import httpx
from httpx import HTTPStatusError, RequestError, TimeoutException

MAX_TRIES = 5
DELAY = 0.5


class ResultsObserver(abc.ABC):
    @abc.abstractmethod
    def observe(self, data: bytes) -> None: ...


async def do_reliable_request(url: str, observer: ResultsObserver) -> None:
    """
    Одна из главных проблем распределённых систем - это ненадёжность связи.

    Ваша задача заключается в том, чтобы таким образом исправить этот код, чтобы он
    умел переживать возвраты ошибок и таймауты со стороны сервера, гарантируя
    успешный запрос (в реальной жизни такая гарантия невозможна, но мы чуть упростим себе задачу).

    Все успешно полученные результаты должны регистрироваться с помощью обсёрвера.
    """

    async with httpx.AsyncClient(timeout=10.0) as client:
        # YOUR CODE GOES HERE
        for attempt in range(1, MAX_TRIES + 1):
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.read()

                observer.observe(data)
                return
            except HTTPStatusError as e:
                if 400 <= e.response.status_code < 500:
                    raise
                if attempt == MAX_TRIES:
                    raise
                await asyncio.sleep(DELAY * 2 ** attempt)
            except (RequestError, TimeoutError) as e:
                if attempt == MAX_TRIES:
                    raise
                await asyncio.sleep(DELAY * 2 ** attempt)
        #####################
