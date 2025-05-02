# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).resolve().parents[2]))

from utils.nas.integration import NasIntegration
from src.schema.nas_params import LoginNasParams, LogoutNasApi
from src.secret import NAS_USERNAME, NAS_PASSWORD


class NasAuthService:
    def __init__(self, nas: NasIntegration):
        self.nas = nas

    async def login(self) -> str:
        params = LoginNasParams(
            api="SYNO.API.Auth",
            version=3,
            method="login",
            session="FileStation",
            account=NAS_USERNAME,
            passwd=NAS_PASSWORD,
            format="cookie",
        )
        response = await self.nas.send_request(
            api=params.api, params=params.model_dump()
        )
        self.nas.sid = response["data"]["sid"]
        return self.nas.sid

    async def logout(self) -> dict:
        params = LogoutNasApi(
            api="SYNO.API.Auth",
            version=1,
            method="logout",
            session="FileStation",
        )
        return await self.nas.send_request(api=params.api, params=params.model_dump())


# import asyncio
# from utils.nas.integration import NasIntegration

# async def main():
#     nas = NasIntegration("192.168.100.105")
#     auth_service = NasAuthService(nas)

#     sid = await auth_service.login()
#     print("Logged in, SID:", sid)

#     await auth_service.logout()
#     print("Logged out")

# asyncio.run(main())
