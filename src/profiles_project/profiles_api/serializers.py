from rest_framework import serializers

from . import models
import datetime
import os

class HelloSerializer(serializers.Serializer):
    '''Serializes a name field for testing our APIView'''

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    '''A serializer for our user profile object'''

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        '''Create and return a new user'''

        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    '''A Serializer for profile feed item'''

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}

class EventDataSerializer(serializers.ModelSerializer):
    '''A serializer for events manage'''

    class Meta:
        model = models.EventData
        fields = ('id', 'user_profile', 'name', 'code', 'description', 'start_date', 'end_date', 'place', 'schedule', 'event_image')

class ChairsDataSerializer(serializers.ModelSerializer):
    '''A serializer for chairs manage.'''

    class Meta:
        model = models.ChairsData
        fields = ('id', 'event', 'person')

class SketchDataSerializer(serializers.ModelSerializer):
    '''A serializer for sketch event.'''

    class Meta:
        model = models.SketchData
        fields = ('id', 'event', 'image_url', 'description')

class DevelopersDataSerializer(serializers.ModelSerializer):
    '''A serializer for developers event.'''

    class Meta:
        model = models.DevelopersData
        fields = ('id', 'event', 'person')

class ScheduleDataSerializer(serializers.ModelSerializer):
    '''A serializer for schedule data event.'''

    class Meta:
        model = models.ScheduleData
        fields = ('id', 'created_on', 'event')
        extra_kwargs = {'created_on': {'read_only': True}}

class StreamDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StreamData
        fields = ('id', 'url', 'description', 'event')

class SponsorDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SponsorData
        fields = ('id', 'person', 'event')

class ActivityTypeDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ActivityTypeData
        fields = ('id', 'name', 'description', 'created', 'show_in_app', 'event')

class ActivityDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ActivityData
        fields = ('id', 'title', 'subtitle', 'description', 'notes', 'price', 'start_date', 'end_date', 'activity_type', 'place', 'schedule')

class ActivityPeopleDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ActivityPeopleData
        fields = ('id', 'activity', 'person')

class PeopleDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PeopleData
        fields = ('id', 'name', 'surname', 'birthdate', 'photo', 'resume', 'email', 'phone', 'provenance', 'event')

class PeopleSocialNetwoeksDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PeopleSocialNetworksData
        fields = '__all__'

class PlaceCategoryDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PlaceCategoryData
        fields = '__all__'

class PlaceDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PlaceData
        fields = '__all__'

class PlaceSocialNetworksSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PlaceSocialNetworksData
        fields = '__all__'

class SocialNetworksSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SocialNetworksData
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ImageData
        fields = '__all__'

class EventPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventData
        fields = ('name', 'code', 'description', 'start_date', 'end_date', 'event_image')

    def create(self, user):

        print('Data')
        print(user)
        print(self.data)
        event = models.EventData(
            user_profile=user,
            name=self.data.get('name'),
            code=self.data.get('code'),
            description=self.data.get('description'),
            start_date=self.data.get('start_date'),
            end_date=self.data.get('end_date'),
            event_image=models.ImageData.objects.get(pk=self.data.get('event_image'))
            )

        print(event)
        event.save()

        return EventDataSerializer(event).data
