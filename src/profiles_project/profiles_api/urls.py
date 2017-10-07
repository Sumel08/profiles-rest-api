from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet, base_name='login')
router.register('feed', views.UserProfileFeedViewSet)
router.register('event', views.EventDataViewSet, base_name='event')
router.register('chair', views.ChairsDataViewSet)
router.register('sketch', views.SketchDataViewSet)
router.register('developer', views.DevelopersDataViewSet)
router.register('schedule', views.ScheduleDataViewSet)
router.register('stream', views.StreamDataViewSet)
router.register('sponsor', views.SponsorDataViewSet)
router.register('activityType', views.ActivityTypeDataViewSet)
router.register('activity', views.ActivityDataViewSet)
router.register('activityPeople', views.ActivityPeopleDataViewSet)
router.register('people', views.PeopleDataViewSet)
router.register('peopleSocialNetworks', views.PeopleSocialNetworksDataViewSet)
router.register('placeCategory', views.PlaceCategoryDataViewSet)
router.register('place', views.PlaceDataViewSet)
router.register('placeSocialNetworks', views.PlaceSocialNetworksDataViewSet)
router.register('socialNetworks', views.SocialNetworksDataViewSet)
router.register('image', views.ImageDataViewSet)

urlpatterns = [
    url(r'^hello-view/', views.HelloApiView.as_view()),
    url(r'', include(router.urls))
]
