from adrf.views import APIView
from apps.common.response import CustomResponse
from .models import User
from .serializers import (
    SocialAuthSerializer,
    SocialAuthResponseSerializer
)
from .utils import verify_google_token
from asgiref.sync import sync_to_async


PROVIDER_MAP ={
    "google": verify_google_token
}

class GoogleAuthAPIView(APIView):
    serializer_class = SocialAuthSerializer
    response_serializer = SocialAuthResponseSerializer

    async def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data["id_token"]
        provider = serializer.validated_data["provider"]
        verify_func = PROVIDER_MAP.get(provider)
        if not verify_func:
            return CustomResponse.error(message="Unsupported Provider")
        
        try:
            user_data = await verify_func(token)
        except Exception as e:
            return CustomResponse.error(message="Invalid Token")
        
        user, _ = await User.objects.aget_or_create(
            provider_user_id=user_data["provider_user_id"],
            defaults={
                "email": user_data["email"],
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "avatar": user_data["avatar"],
                "auth_provider": provider
            }
        )

        tokens = await sync_to_async(lambda: user.tokens)()

        response_data = {
            "email": user.email,
            "full_name": user.full_name,
            "avatar": user.avatar,
            "access": tokens.get("access"),
            "refresh": tokens.get("refresh")
        }

        serialized_response = self.response_serializer(response_data)
        return CustomResponse.success(message="Authenticated Successfully", data=serialized_response.data)
        

