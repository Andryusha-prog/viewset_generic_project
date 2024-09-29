from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (UserCreateApiView, UserDestroyApiView,
                         UserListApiView, UserRetrieveApiView,
                         UserUpdateApiView)

app_name = UsersConfig.name


urlpatterns = [
    path("create/", UserCreateApiView.as_view(), name="create"),
    path("list/", UserListApiView.as_view(), name="list"),
    path("detail/<int:pk>/", UserRetrieveApiView.as_view(), name="detail"),
    path("update/<int:pk>/", UserUpdateApiView.as_view(), name="update"),
    path("delete/<int:pk>/", UserDestroyApiView.as_view(), name="delete"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
