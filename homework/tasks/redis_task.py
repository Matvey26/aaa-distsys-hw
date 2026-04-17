import redis.asyncio as aredis


class UsersByTitleStorage:
    def __init__(self):
        self._client = aredis.StrictRedis(host="127.0.0.1", port=6379, db=0)

    async def connect(self) -> None:
        await self._client.ping()

    async def disconnect(self) -> None:
        await self._client.aclose()

    async def save_item(self, user_id: int, title: str) -> None:
        """
        Напишите код для сохранения записей таким образом, чтобы в дальнейшем
        можно было за один запрос получить список уникальных пользователей,
        имеющих объявления с заданным заголовком.
        """
        # YOUR CODE GOES HERE
        await self._client.sadd(str(hash(title)), str(user_id))

    async def find_users_by_title(self, title: str) -> list[int]:
        """
        Напишите код для поиска уникальных user_id, имеющих хотя бы одно объявление
        с заданным title.
        """
        # YOUR CODE GOES HERE
        result_bytes = await self._client.smembers(str(hash(title)))
        # print(result_bytes, file=)
        return [int(uid) for uid in result_bytes]
