from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions

# Create your views here.

class HelloApiView(APIView):
    '''Test API View.'''

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        '''Returns a list of APIView features.'''

        an_apiView = [
            'Uses HTTP methods as functions (get, post, put, patch, delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over you logic',
            'Is mapped manually to URL\'s'
        ]

        return Response({'message': 'Hello', 'an_apiView': an_apiView})

    def post(self, request):
        '''Create a Hello message with our name'''

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        '''Handles updating an object'''

        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        '''Handles partially update of an object'''

        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        '''Handles delete object'''

        return Response({'method': 'delete'})

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message."""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)'
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        '''Create a new Hello message.'''

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)

            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        '''Handles getting an object by its ID.'''

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        '''Handles updating an object'''

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        '''Handles updating part of an object'''

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        '''Handles removing an object'''

        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading and updating profiles.'''

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class LoginViewSet(viewsets.ViewSet):
    '''Checks email and password and returns an auth token'''

    serializer_class = AuthTokenSerializer

    def create(self, request):
        '''Use the ObtainAuthToken APIView to validate and create a token'''

        return ObtainAuthToken().post(request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading and updating profile feed items.'''

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        '''Sets the user profile to the logged in user.'''

        serializer.save(user_profile=self.request.user)

class EventDataViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading and updating events.'''

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.EventDataSerializer
    queryset = models.EventData.objects.all()
    permission_classes = (permissions.ManageOwnEvents,)

    def perform_create(self, serializer):
        '''Sets the user profile to the logged in user.'''

        serializer.save(user_profile=self.request.user)

class ChairsDataViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading and updating chairs.'''

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ChairsDataSerializer
    queryset = models.ChairsData.objects.all()
    permission_classes = (permissions.ManageOwnEvents,)

class SketchDataViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading and updating sketch.'''

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.SketchDataSerializer
    queryset = models.SketchData.objects.all()
    permission_classes = (permissions.ManageOwnEvents,)

class DevelopersDataViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading, and updating developers.'''

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.DevelopersDataSerializer
    queryset = models.DevelopersData.objects.all()
    permission_classes = (permissions.ManageOwnEvents,)

class ScheduleDataViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading and updating schedule.'''

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ScheduleDataSerializer
    queryset = models.ScheduleData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class StreamDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.StreamDataSerializer
    queryset = models.StreamData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class SponsorDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.SponsorDataSerializer
    queryset = models.SponsorData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class ActivityTypeDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ActivityTypeDataSerializer
    queryset = models.ActivityTypeData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class ActivityDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ActivityDataSerializer
    queryset = models.ActivityData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class ActivityPeopleDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ActivityPeopleDataSerializer
    queryset = models.ActivityPeopleData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class PeopleDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PeopleDataSerializer
    queryset = models.PeopleData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class PeopleSocialNetworksDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PeopleSocialNetwoeksDataSerializer
    queryset = models.PeopleSocialNetworksData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class PlaceCategoryDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PlaceCategoryDataSerializer
    queryset = models.PlaceCategoryData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class PlaceDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PlaceDataSerializer
    queryset = models.PlaceData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class PlaceSocialNetworksDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PlaceSocialNetworksSerializer
    queryset = models.PlaceSocialNetworksData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class SocialNetworksDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.SocialNetworksSerializer
    queryset = models.SocialNetworksData.objects.all()
    permission_classes = (permissions.GenericPermissions,)
