from ..client import generate_client
from ..declaration.auth_pb2 import GetUserRequest


async def get_user(userid: int) -> dict:
    client = await generate_client()
    response = await client.GetUser(GetUserRequest(userid=userid))
    return response.user if response.success else None
