from django.http.response import Http404, HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, mixins, serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from .serializers import ArticleSerializer
from .models import Article
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication,TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import viewsets


class GenericAPIView(generics.GenericAPIView,
mixins.ListModelMixin, 
mixins.CreateModelMixin, 
mixins.UpdateModelMixin,
mixins.RetrieveModelMixin, 
mixins.DestroyModelMixin):
  

  serializer_class = ArticleSerializer
  queryset = Article.objects.all()
  lookup_field ='id'
  
  # authentication_classes = [SessionAuthentication, BasicAuthentication]
  authentication_classes = [TokenAuthentication] 
  permission_classes = [IsAuthenticated]
  

  def get(self, request, id=None):
    if id:
      return self.retrieve(request)
    else:
      return self.list(request)


  def post(self,request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def put(self,request, id=None):
     return self.update(request, id)
  
  def delete(self,request, id=None):
    return self.destroy(request, id)

   


""""
A ViewSet class 
It is simply a type of class-based View, that does not provide any method handlers such as .get() or .post(), 
and instead provides actions such as .list() and .create(), .update(), .retrieve()
"""


""""
General viewset
"""
# detail": "Method \"GET\" not allowed to avoid while adding mixins 
# we need to add RetrieveModelMixin along with UpdateModelMixin
class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, 
mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
  serializer_class = ArticleSerializer
  queryset=Article.objects.all()




# class ArticleViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     def list(self, request):
#        article = Article.objects.all()
#        serializer =  ArticleSerializer(article, many=True)
#        return Response(serializer.data)

#     def create(self, request):
#       serializer = ArticleSerializer(data=request.data)

#       if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
#     def retrieve(self, request, pk=None):
#         queryset =Article.objects.all()
#         article = get_object_or_404(queryset, pk=pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
        
# # put/patch
#     def update(self, request, pk=None):
#         article = get_object_or_404(Article, pk=pk)
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#           serializer.save()
#           return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      



""""
class based views using APIView
"""
class ArticleView(APIView):
# list
  def get(self, request):
    article = Article.objects.all()
    serializer =  ArticleSerializer(article, many=True)
    return Response(serializer.data)

# TO POST
  def post(self, request):
    serializer = ArticleSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
  
  # def get_object(self, id):
  #   try:
  #     return Article.objects.get(id=id)
  #   except Article.DoesNotExist:
  #     return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
      

#to get  
  def get(self, request, id):
    # article =self.get_object(id)
    article = get_object_or_404(Article, id=id)
    serializer=ArticleSerializer(article)
    return Response(serializer.data)
  
#to put/patch
  def put(self, request, id):
    # article = self.get_object(id)
    article = get_object_or_404(Article, id=id)
    serializer = ArticleSerializer(article, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
#to delete
  def delete(self, request, id):
    # article =self.get_object(id)
    article = get_object_or_404 (Article, id=id)
    article.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


"""
function based views
"""


# @csrf_exempt
@api_view(['GET', 'POST'])
def article_list(request):
    
    if request.method == 'GET':
      article = Article.objects.all()
      serializer =  ArticleSerializer(article, many=True)
      # return JsonResponse(serializer.data, safe=False)
      return Response(serializer.data)

    elif request.method == 'POST':
      # data = JSONParser().parse(request)
      serializer = ArticleSerializer(data=request.data)

      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      # return JSONResponse(serializer.errors, status=400)
      return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @csrf_exempt
def article_detail(request, pk):
  try:
    article = Article.objects.get(pk = pk)

  except Article.DoesNotExist:
    return HttpResponse(status=404)
  
  if request.method == 'GET':
    serializer = ArticleSerializer(article)
    # return JsonResponse(serializer.data)
    return Response(serializer.data, status=HTTP_200_OK)


  elif request.method == 'PUT':
    data =JSONParser.parse(request)
    serializer = ArticleSerializer(article, data =data)
    if serializer.is_valid():
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)


  elif request.method == 'DELETE':
    article.delete()
    # return HttpResponse(status=204)
    return Response(status =status.HTTP_204_NO_CONTENT )


class articlelistapiview(generics.ListAPIView, mixins.CreateModelMixin):
    serializer_class = ArticleSerializer

    def get_queryset(self):
      return Article.objects.all()
    
    def post(self, request, *args, **kwargs):
      return self.create(request, *args, **kwargs)

