from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.exceptions import AuthenticationFailed


async def verify_google_token(token):
    try:
        request = requests.Request()
        id_info = id_token.verify_oauth2_token(token, request)

        return {
            "provider_user_id": id_info["sub"],
            "email": id_info["email"],
            "first_name": id_info["given_name"],
            "last_name": id_info["family_name"],
            "avatar": id_info["picture"]
        }
    
    except ValueError as e:
        raise AuthenticationFailed("Invalid Token")