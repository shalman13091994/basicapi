from django.urls import path
from django.urls.conf import include
from .views import GenericAPIView,ArticleViewSet
from rest_framework.routers import DefaultRouter #this is for viewsets.ViewSet

app_name = 'articleapi'
router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')

urlpatterns = [
    #router - url will be http://localhost:8000/api/article/viewset/article/
    path('viewset/', include(router.urls)), 
    path('viewset/<int:pk>', include(router.urls)),
    # path('', articlelistapiview.as_view(), name='article-list'),
    #path('', article_list, name='article-list'),
    # path('detail/<int:pk>/', article_detail, name='article-detail'),
    # path('', ArticleView.as_view(),name='article-list'),
    # path('<int:id>/', ArticleDetailView.as_view(),name='article-detail'),
    path('', GenericAPIView.as_view(), name='article-list'),
    path('<int:id>/', GenericAPIView.as_view(), name='article-detail'),

]
