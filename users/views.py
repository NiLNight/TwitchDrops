from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserProfile


class UserRegistration(APIView):
    serializer_class = UserSerializer

    @extend_schema(
        summary="Регистрация пользователя",
        description="Создаёт нового пользователя",
        request=UserSerializer,
        responses={
            201: OpenApiResponse(response=UserSerializer, description="Пользователь успешно создан"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.data['username'],
                email=serializer.data['email'],
                password=serializer.data['password']
            )
            user.save()
            return Response({"status": "User created", "id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
