from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters 
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated
from watchlist_app.models import Watchlist,StreamPlatform,Review
from watchlist_app.api.serializers import (WatchListSerializer, 
                                           StreamPlatformSerializer, ReviewSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from watchlist_app.api.permissions import AdminOrReadonly,Review_userOrReadonly 
from watchlist_app.api.throtling import ReviewCreateThrottle,ReviewListThrottle
from watchlist_app.api.pagination import WatchlistPagination,WatchlistPaginationLO,WatchlistpaginationCursor
 
 
 
 
# to get review done by a particular user
class UserReview(generics.ListAPIView):
    serializer_class=ReviewSerializer
    def get_queryset(self):
        # username=self.kwargs['username']
        # return Review.objects.filter( user_name__username=username)
        
        username=self.request.query_params.get('username')
        return Review.objects.filter( user_name__username=username)
        
class ReviewCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    
    authentication_class=[permissions.IsAuthenticated]
    
    throttle_classes=[ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()
        
    def perform_create(self,serializer):
        
        review_user=self.request.user
        pk=self.kwargs['pk']
        movie=Watchlist.objects.get(pk=pk)
        review_queryset=Review.objects.filter(watchlist=movie,user_name=review_user)
        if review_queryset.exists():
            raise ValidationError("Reviewd already!")
        
        if movie.avg_numbering == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating=(movie.avg_rating+serializer.validated_data['rating'])/2
            
        movie.avg_numbering=movie.avg_numbering + 1
        movie.save()
            
        serializer.save(watchlist=movie,user_name=review_user)
    
    

class ReviewList(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    # queryset=Review.objects.all()
    throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    serializer_class=ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_name__username', 'active']        
    def get_queryset(self):
        id=self.kwargs.get('pk')
        print(id)
        return Review.objects.filter(watchlist=id)
      
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    # permission_classes = [AdminOrReadonly]
    permission_classes=[Review_userOrReadonly]
    # throttle_classes = [UserRateThrottle,AnonRateThrottle]
    throttle_classes=[ScopedRateThrottle]
    throttle_scope='review_detail'
    pagination_class=[]
    
    
    
    
# class ReviewDetail(mixins.RetrieveModelMixin,
#                    generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)

# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
    
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)


# class Streamplatform2(viewsets.ReadOnlyModelViewSet):
#     queryset=StreamPlatform.objects.all()
#     serializer_class=StreamPlatformSerializer

class Streamplatform2(viewsets.ModelViewSet):
    permission_classes=[AdminOrReadonly]
    queryset=StreamPlatform.objects.all()
    serializer_class=StreamPlatformSerializer

# class Streamplatform2(viewsets.ViewSet):
#     def list(self,request):
#         platforms=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializer(platforms, many=True)
#         return Response(data=serializer.data)
    
#     def create(self,request):
#         serializer=StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         return Response(data=serializer.errors)
    
#     def retrieve(self,request,*args,**kwargs):
#         id=kwargs.get('pk')
#         qs=StreamPlatform.objects.get(id=id)
#         serializer=StreamPlatformSerializer(qs,many=False)
#         return Response(data=serializer.data)
    
#     def update(self,request,*args,**kwargs):
#         pk=kwargs.get('pk')
#         platform=StreamPlatform.objects.get(pk=pk)
#         serializer=StreamPlatformSerializer(platform,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         return Response(data=serializer.data)
#     def destroy(self,request,*args,**kwargs):
#         pk=kwargs.get('pk')
#         StreamPlatform.objects.filter(pk=pk).delete()
#         return Response(data='DELETED')


class Streamplatform(APIView):
    permission_classes=[AdminOrReadonly]
    def get(self,request):
        platforms=StreamPlatform.objects.all()
        serializer=StreamPlatformSerializer(platforms, many=True, context={'request': request})
        return Response(data=serializer.data)
    def post(self,request):
        serializer=StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
        
class StreamPlatformDetail(APIView):
    permission_classes=[AdminOrReadonly]
    def get(self,request,pk):
        try:
            platform=StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Eror':'Platform does not exist'},status=status.HTTP_404_NOT_)
        serializer=StreamPlatformSerializer(platform)
        return Response(data=serializer.data)
    
    def put(self,request,pk):
        platform=StreamPlatform.objects.get(pk=pk)
        serializer=StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        movie=StreamPlatform.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# CREATING WATCHLIST CLASS FOR TESTING GENERIC FILTERS
class Watchlist2(generics.ListAPIView):
    queryset=Watchlist.objects.all()
    serializer_class=WatchListSerializer
    
    # pagination_class=WatchlistPagination
    # pagination_class=WatchlistPaginationLO
    pagination_class=WatchlistpaginationCursor
    
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']
    
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']
    
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']
    

    



class WatchList(APIView):
    permission_classes=[AdminOrReadonly]
    def get(self,request):
        movies=Watchlist.objects.all()
        serializer=WatchListSerializer(movies,many=True)
        return Response(data=serializer.data)
    def post(self,request):
        serializer=WatchListSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)  
        else:
            return Response(data=serializer.errors)
        
class WatchDetail(APIView):
    permission_classes=[AdminOrReadonly]
    def get(self,request,pk):
        try:
            movie=Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({'Eror':'Movie does not exist'},status=status.HTTP_404_NOT_)
        serializer=WatchListSerializer(movie)
        return Response(data=serializer.data)
    
    def put(self,request,pk):
        movie=Watchlist.objects.get(pk=pk)
        serializer=WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        movie=Watchlist.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET','POST'])
def movie_list(request):
    if request.method=='GET':
        movies=Movie.objects.all()
        serializer=MovieSerailizer(movies,many=True)
        return Response(data=serializer.data)
    
    if request.method=='POST':
        serializer=MovieSerailizer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)  
        else:
            return Response(data=serializer.errors)
     

@api_view(['GET','PUT','DELETE'])
def movie_detail(request,pk):
    
    if request.method=='GET':
        try:
            movie=Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'Eror':'Movie does not exist'},status=status.HTTP_404_NOT_)
        serializer=MovieSerailizer(movie)
        return Response(data=serializer.data)
    
    if request.method=='PUT':
        movie=Movie.objects.get(pk=pk)
        serializer=MovieSerailizer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    if request.method=='DELETE':
        movie=Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
    
        
        
           

     
