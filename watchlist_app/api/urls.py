from django.urls import path,include
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_list,movie_detail
from watchlist_app.api.views import  (WatchList,WatchDetail,Streamplatform,Streamplatform2,
                                      StreamPlatformDetail,ReviewList,ReviewDetail,ReviewCreate,UserReview
                                      ,Watchlist2)



router=DefaultRouter()
router.register('stream1', Streamplatform2 , basename='stream1')


urlpatterns = [ 
            #    path('list/',movie_list,name='movie-list'),
            #    path('<int:pk>',movie_detail,name='movie_detail')
            path('list/',WatchList.as_view(),name='movie'),
            path('list/<int:pk>',WatchDetail.as_view(),name='movie_detail'),
            # path('',include(router.urls)),
            # path('stream/',Streamplatform.as_view(),name='stream'),
            path('list2/',Watchlist2.as_view(),name='movie2'),
            # path('stream/<int:pk>',StreamPlatformDetail.as_view(),name='stream_detail'),
            path('list/<int:pk>/review_create/',ReviewCreate.as_view(),name='review_create'),
            path('list/<int:pk>/review/',ReviewList.as_view(),name='review'),
            path('list/review/<int:pk>',ReviewDetail.as_view(),name='review_detail'),
            path('list/review/<str:username>',UserReview.as_view(),name='review_detail'),
            # Filtering aginst par-postman-lochost/watch/list/review/?username=neema
            path('list/review/',UserReview.as_view(),name='review_user_detail'),
             
]+router.urls