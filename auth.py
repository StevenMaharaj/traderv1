from dataclasses import dataclass
import json

@dataclass
class Auth:
    api_key: str
    secret_key: str

@dataclass
class DeribtAuth(Auth):
    grant_type: str = 'client_credentials'



    async def auth(self,websocket):
        msg: dict= \
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "public/auth",
                "params": {
                    "grant_type": self.grant_type,
                    "client_id": self.api_key,
                    "client_secret": self.secret_key
                }
            }
        await websocket.send(json.dumps(msg))
        res = await websocket.recv()
        res_dict = json.loads(res)
        try: 
            auth_scope = res_dict['result']["scope"]
            print(f"Authentication Successful - Scope: {auth_scope}")
        except KeyError:
            print(f"Authentication Unsuccessful")
        # return res

