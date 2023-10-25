 
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from watchlist_app.models import StreamPlatform,Review,Watchlist
from watchlist_app.api.serializers import StreamPlatformSerializer,WatchListSerializer,ReviewSerializer

# Create your tests here.

class StreamPlatformTestcase(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='example',
                                       password='example123')
        self.token=Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # for taking detail-third function
        self.stream=StreamPlatform.objects.create(name='Netflix',
              about='description1',
              website='https://netflix.com')
        
    def test_streamplatform_create(self):
        data={'name':'Netflix',
              'about':'description1',
              'website':'https://netflix.com'}
        response=self.client.post(reverse('stream1-list'),data)
        # steam1 is the basename in url
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        # here frorbiden is given bcs we are creating setup with not admin
        # and in persmission adminor user is given
        
    def test_streamplatform_list(self):
        response=self.client.get(reverse('stream1-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatfrom_detail(self):
        response=self.client.get(reverse('stream1-detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
class WatchlistTestCase(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='example',password='example123')
        self.token=Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream=StreamPlatform.objects.create(name='Netflix',
              about='description1',
              website='https://netflix.com')
        self.watchlist=Watchlist.objects.create(platform=self.stream,title='Example',
                                                storyline='example',active=True)
        
    def test_watchlist_create(self):
        data={'platfrom':self.stream,
              'title':'Example Movie',
              'storyline':'Example Storyline',
              'active':True}
        response=self.client.post(reverse('movie'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response=self.client.get(reverse('movie'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_watchlist_detail(self):
        response=self.client.get(reverse('movie_detail',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(Watchlist.objects.count(),1)
        self.assertEqual(Watchlist.objects.get().title,'Example')
    def test_watchlist_put(self):
        data={'platfrom':self.stream,
              'title':'Example Movie-1',
              'storyline':'Example Storyline',
              'active':True}
        response=self.client.put(reverse('movie_detail',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_(self):
        response=self.client.delete(reverse('movie_detail' ,args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
class ReviewTestCase(APITestCase):
     
    def setUp(self):
        self.user=User.objects.create_user(username='example',password='example123')
        self.token=Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream=StreamPlatform.objects.create(name='Netflix',
                about='description1',
                website='https://netflix.com')
        self.watchlist=Watchlist.objects.create(platform=self.stream,title='Example',
                                                    storyline='example',active=True)
        
        # Here new watchlist created bcs when already review is given in !st create method,it cannot happen
        self.watchlist2=Watchlist.objects.create(platform=self.stream,title='Example',
                                                    storyline='example',active=True)
        self.review=Review.objects.create(user_name=self.user,rating=3,
               description='good',watchlist=self.watchlist2,active=True)   
    def test_review_create(self):
        
        data={'user_name':self.user,'rating':3,
              ' description':'good','watchlist':self.watchlist,'active':True
            
        }    
        response=self.client.post(reverse('review_create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        # self.assertEqual(Review.objects.count(),2)
        # self.assertEqual(Review.objects.get().rating,3)
        
        # ONLY ALLOWED TO REVIEW FOR 1 TIME-SO 400 BADREQUEST
        response=self.client.post(reverse('review_create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    
    def test_review_create_unauth(self):
        
        
        data={'user_name':'example1','rating':3,
              ' description':'good','watchlist':self.watchlist,'active':True
            
        }
        
        # # force auth-logout,or another use login
        # self.client.force_authenticate(user=None )
        # response=self.client.post(reverse('review_create',args=(self.watchlist.id,)),data)
        # self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        data={'user_name':'example1-updated','rating':4,
              ' description':'good','watchlist':self.watchlist,'active':True
            
        }
        
        response=self.client.put(reverse('review_detail',args=(self.review.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_review_list(self):
        response=self.client.get(reverse('review',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    def test_review_detail(self):
        response=self.client.get(reverse('review_detail',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    # WE ACCES REVIEW HERE BY URL PARAMETER?USERNAME=NEEMA
    def test_review_user(self):
        response=self.client.get('/watch/list/review/?username'+ self.user.username)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    def test_review_user(self):
        response=self.client.get(reverse('review_user_detail'),args=(self.user))
        self.assertEqual(response.status_code,status.HTTP_200_OK)