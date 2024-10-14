from rest_framework import generics, status 
from rest_framework.response import Response
from .models import BlogPost, Category, Like, Comment
from .serializers import BlogPostSerializer, UserSerializer,  CommentSerializer, LikeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.db.models import Count
from django.shortcuts import get_object_or_404

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def endpoints(request):
    return Response ("/blogposts/ , /blogposts/<uuid:pk>/, /signup/, /login/, /token/', /token/refresh/, /category, /comment/, comment/<uuid:pk>/, /like/, /like/<int:pk>/delete/ /post_by/<str:category_name>/")

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
    
@permission_classes([IsAuthenticated])
class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all().annotate(
        like_count=Count('like'),
        comment_count=Count('comment')
    )
    serializer_class = BlogPostSerializer
    pagination_class = CustomPagination
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(categories__name=category)
        return queryset

@permission_classes([IsAuthenticated])   
class BlogPostRetrieveUpdatesDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "pk"
    
    def get_object(self):
        obj = super().get_object()
       
        if not self.request.user.is_superuser and obj.author != self.request.user:
            self.permission_denied(self.request)
        return obj
    
    


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        })
    else:
        return Response({"detail": "Nieprawidłowe dane uwierzytelniające."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        })
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token is None:
                return Response({"detail": "Brak tokenu odświeżania."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Wylogowano pomyślnie."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"detail": "Token jest nieprawidłowy lub już został unieważniony."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

@permission_classes([IsAuthenticated])
class BlogPostByCategory(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # Pobierz nazwę kategorii z parametru URL
        category_name = self.kwargs.get('category_name')
        
        # Znajdź kategorię o podanej nazwie
        category = get_object_or_404(Category, name=category_name)
        
        # Zwróć posty przypisane do tej kategorii
        return BlogPost.objects.filter(categories=category)

@permission_classes([IsAuthenticated]) 
class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@permission_classes([IsAuthenticated]) 
class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'  

    def get_object(self):
        # Pobiera obiekt i sprawdza, czy użytkownik jest autorem komentarza
        obj = super().get_object()
        if not self.request.user.is_superuser and obj.author != self.request.user:
            self.permission_denied(self.request, message="Nie masz uprawnień do edycji lub usunięcia tego komentarza.")
        return obj
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@permission_classes([IsAuthenticated]) 
class LikeListCreate(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        like = self.get_object()
        
        # Sprawdzenie, czy użytkownik jest autorem polubienia
        if not self.request.user.is_superuser and like.author != request.user:
            return Response({"detail": "Nie masz uprawnień do usunięcia tego polubienia."},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Usunięcie polubienia
        like.delete()
        return Response({"detail": "Polubienie zostało usunięte."}, status=status.HTTP_204_NO_CONTENT)
