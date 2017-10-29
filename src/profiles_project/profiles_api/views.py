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
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404

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

    @list_route(methods=['GET'], permission_classes=[IsAuthenticated])
    def event(self, request):
        print('Estamos obteniendo el evento---------------------')
        print(request.user)
        event = get_object_or_404(models.EventData, user_profile=request.user)

        return Response(serializers.EventDataSerializer(event).data)

class LoginViewSet(viewsets.ViewSet):
    '''Checks email and password and returns an auth token'''

    serializer_class = AuthTokenSerializer

    def create(self, request):
        '''Use the ObtainAuthToken APIView to validate and create a token'''
        print(request.data)
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
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

    def create(self, request):
        serializer = serializers.EventPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            resp = serializer.create(request.user)
            return Response(resp)
        except Exception as err:
            return Response({'detail':str(err)}, status=500)

        return Response(serializer.create(request.user))

    def partial_update(self, request, pk):
        serializer = serializers.EventPATCHSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = serializer.partial_update(request.user, pk)
            return Response(result)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

    @list_route(methods=['GET'], permission_classes=[IsAuthenticated])
    def getMyEvent(self, request):
        print(self.request.user)
        event = models.EventData.objects.filter(user_profile=request.user).first()
        if event:
            print(event)
            return Response(serializers.EventDataSerializer(event).data)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['GET'], permission_classes=[IsAuthenticated])
    def sketch(self, request):
        event = models.EventData.objects.get(user_profile=request.user)
        try:
            sketch = models.SketchData.objects.get(event=event)
            return Response(serializers.SketchDataSerializer(sketch).data)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

    @detail_route(methods=['GET'], permission_classes=[IsAuthenticated])
    def images(self, request, pk):
        event = models.EventData.objects.get(pk=pk)
        images = []
        images.append(event.event_image)
        images.append(models.SketchData.objects.get(event=event).image_url)
        activitiesType = models.ActivityTypeData.objects.filter(event=event)
        print(activitiesType)
        for x in activitiesType:
            images.append(x.image)
        people = models.PeopleData.objects.filter(event=event)
        for x in people:
            images.append(x.photo)
        placeCategory = models.PlaceCategoryData.objects.filter(event=event)
        places = models.PlaceData.objects.filter(place_category__in=placeCategory)
        for x in places:
            images.append(x.image)
        # images.append([x.image for x in activitiesType])

        # images = sum(images, [])
        print(images)
        images = set(list(images))
        # print(images)

        # return Response('OK')
        return Response(serializers.ImageSerializer(images, many=True).data)

class ChairsDataViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading and updating chairs.'''

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ChairsDataSerializer
    queryset = models.ChairsData.objects.all()
    permission_classes = (permissions.ManageOwnEvents,)

    def create(self, request):
        serializer = serializers.ChairsPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = serializer.create(request.user)
            return Response(result)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

class SketchDataViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading and updating sketch.'''

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.SketchDataSerializer
    queryset = models.SketchData.objects.all()
    permission_classes = (permissions.ManageOwnEvents,)

    def create(self, request):
        serializer = serializers.SketchPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # try:
        result = serializer.create(request.user)
        return Response(result)
        # except Exception as err:
        #     return Response({'detail': str(err)}, status=500)

class DevelopersDataViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading, and updating developers.'''

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.DevelopersDataSerializer
    queryset = models.DevelopersData.objects.all()
    permission_classes = (permissions.ManageOwnEvents,)

    def create(self, request):
        serializer = serializers.DeveloperPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = serializer.create(request.user)
            return Response(result)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

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

    def create(self, request):
        serializer = serializers.StreamPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = serializer.create(request.user)
            return Response(result)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

class SponsorDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.SponsorDataSerializer
    queryset = models.SponsorData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

    def create(self, request):
        serializer = serializers.SponsorPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = serializer.create(request.user)
            return Response(result)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

class ActivityTypeDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ActivityTypeDataSerializer
    queryset = models.ActivityTypeData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

    def list(self, request):
        event = models.EventData.objects.get(user_profile=request.user)
        activitiesType = models.ActivityTypeData.objects.filter(event=event)
        return Response(serializers.ActivityTypeDataSerializer(activitiesType, many=True).data)

    def create(self, request):
        serializer = serializers.ActivityTypePOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = serializer.create(request.user)
            return Response(result)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

class ActivityDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ActivityDataSerializer
    queryset = models.ActivityData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

    def list(self, request):
        event = models.EventData.objects.get(user_profile=request.user)
        schedule = models.ScheduleData.objects.get(event=event)
        activities = models.ActivityData.objects.filter(schedule=schedule).order_by('start_date')

        return Response(serializers.ActivityDataSerializer(activities, many=True).data)

    def create(self, request):
        serializer = serializers.ActivityPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = serializer.create(request.user)
            return Response(result)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

class ActivityPeopleDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ActivityPeopleDataSerializer
    queryset = models.ActivityPeopleData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

    def create(self, request):
        serializer = serializers.ActivityPeoplePOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = serializer.create(request.user)
            return Response(result)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

class PeopleDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PeopleDataSerializer
    queryset = models.PeopleData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

    def list(self, request):
        event = models.EventData.objects.get(user_profile=request.user)
        people = models.PeopleData.objects.filter(event=event)

        return Response(serializers.PeopleDataSerializer(people, many=True).data)

    def create(self, request):
        serializer = serializers.PeoplePOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            resp = serializer.create(request.user)
            return Response(resp)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

    def retrieve(self, request, pk):
        try:
            event = models.EventData.objects.get(user_profile=request.user)
            person = models.PeopleData.objects.get(event=event, pk=pk)
            return Response(serializers.PeopleDataSerializer(person).data)
        except models.EventData.DoesNotExist as err:
            return Response({'detail': str(err)}, status=404)
        except models.PeopleData.DoesNotExist as err:
            return Response({'detail': str(err)}, status=404)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

class PeopleSocialNetworksDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PeopleSocialNetwoeksDataSerializer
    queryset = models.PeopleSocialNetworksData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

class PlaceCategoryDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PlaceCategoryDataSerializer
    queryset = models.PlaceCategoryData.objects.all()
    permission_classes = (permissions.GenericPermissions,IsAuthenticated)

    def list(self, request):
        try:
            event = models.EventData.objects.get(user_profile=request.user)
            place_categories = models.PlaceCategoryData.objects.filter(event=event)
            return Response(serializers.PlaceCategoryDataSerializer(place_categories, many=True).data)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

    def retrieve(self, request, pk):
        event = get_object_or_404(models.EventData, user_profile=request.user)
        try:
            place_category = models.PlaceCategoryData.objects.get(pk=pk, event=event)
            return Response(serializers.PlaceCategoryDataSerializer(place_category).data)
        except models.PlaceCategoryData.DoesNotExist as err:
            return Response({'detail': str(err)}, status=404)

    def create(self, request):
        serializer = serializers.PlaceCategoryPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            resp = serializer.create(request.user)
            return Response(resp)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

    def destroy(self, request, pk):
        event = get_object_or_404(models.EventData, user_profile=request.user)
        try:
            place_category = models.PlaceCategoryData.objects.get(pk=pk, event=event)
            place_category.delete()
            return Response(serializers.PlaceCategoryDataSerializer(place_category).data)
        except models.PlaceCategoryData.DoesNotExist as err:
            return Response({'detail': str(err)}, status=404)

class PlaceDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PlaceDataSerializer
    queryset = models.PlaceData.objects.all()
    permission_classes = (permissions.GenericPermissions,)

    def list(self, request):
        try:
            event = models.EventData.objects.get(user_profile=request.user)
            place_categories = models.PlaceCategoryData.objects.filter(event=event)
            places = models.PlaceData.objects.filter(place_category__in=place_categories)
            return Response(serializers.PlaceDataSerializer(places, many=True).data)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

    def retrieve(self, request, pk):
        try:
            event = models.EventData.objects.get(user_profile=request.user)
            place_categories = models.PlaceCategoryData.objects.filter(event=event)
            places = models.PlaceData.objects.get(place_category__in=place_categories, pk=pk)
            return Response(serializers.PlaceDataSerializer(places).data)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

    def destroy(self, request, pk):
        try:
            event = models.EventData.objects.get(user_profile=request.user)
            place_categories = models.PlaceCategoryData.objects.filter(event=event)
            places = models.PlaceData.objects.get(place_category__in=place_categories, pk=pk)
            places.delete()
            return Response(serializers.PlaceDataSerializer(places).data)
        except Exception as err:
            return Response({'detail': str(err)}, status=500)

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

class ImageDataViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ImageSerializer
    queryset = models.ImageData.objects.all()
    permission_classes = (permissions.GenericPermissions,)
