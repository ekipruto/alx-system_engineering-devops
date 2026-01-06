from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        # Create a new token instance directly
        token = cls()

        # Use .pk (works regardless of field name) or your explicit UUID field
        token['user_id'] = str(user.pk)   # or str(user.user_id)

        # Add any extra claims you want
        token['email'] = user.email
        token['role'] = user.role

        return token

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return CustomRefreshToken.for_user(user)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer