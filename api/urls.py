from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)

urlpatterns = [
    path("", views.endpoints, name="endpoints"),
    path("blogposts/", views.BlogPostListCreate.as_view(), name="blogpost-view-create"),
    path("blogposts/<uuid:pk>/", views.BlogPostRetrieveUpdatesDestroy.as_view(), name="blog-update-delete"),
    path("comment/", views.CommentListCreate.as_view(), name="comment"),
    path("comment/<uuid:pk>/", views.CommentRetrieveUpdateDestroy.as_view(), name="comment-update-delete"),
    path("post_filter_by/<str:category_name>/", views.BlogPostByCategory.as_view(), name='posts-by-category'),
    path("like/", views.LikeListCreate.as_view(), name="like"),
    path("like/<int:pk>/delete/", views.LikeDeleteView.as_view(), name="like-delete"),
    path("login/", views.login, name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
