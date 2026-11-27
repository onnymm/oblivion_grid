from galaxy_life_api_wrapper import APIWrapper
from galaxy_life_api_wrapper.typing import AllianceAttributes, User


class GalaxyLifeService:
    def __init__(self, api: APIWrapper) -> None:
        self._api = api

    async def get_player_by_name(self, name: str) -> User:
        return await self._api.users.name(name=name)

    async def get_alliance_by_name(self, name: str) -> AllianceAttributes:
        return await self._api.alliances.get(name=name)
