from rest_framework import serializers

from . import models
import datetime
import os

from django.conf import settings

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

    event_image_url = serializers.SerializerMethodField()
    event_date = serializers.SerializerMethodField()

    class Meta:
        model = models.EventData
        fields = ('id', 'user_profile', 'name', 'code', 'description', 'start_date', 'end_date', 'place', 'schedule', 'event_image', 'event_image_url', 'event_date')

    def get_event_image_url(self, obj):
        return ImageSerializer(obj.event_image).data.get('image')

    def get_event_date(self, obj):
        return obj.start_date.strftime("%A %B %d") + ' - ' + obj.end_date.strftime("%A %B %d")

class ChairsDataSerializer(serializers.ModelSerializer):
    '''A serializer for chairs manage.'''

    person_data = serializers.SerializerMethodField()

    class Meta:
        model = models.ChairsData
        fields = ('id', 'event', 'person', 'person_data')

    def get_person_data(self, obj):
        return PeopleDataSerializer(obj.person).data

class ChairsPOSTSerializer(serializers.Serializer):

    people = serializers.ListField(required=True)

    def create(self, user):

        event = models.EventData.objects.get(user_profile=user)
        chairs = models.ChairsData.objects.filter(event=event)

        for chair in chairs:
            chair.delete()

        for person in self.data.get('people'):
            chair = models.ChairsData(
                event = event,
                person = models.PeopleData.objects.get(id=person)
            )
            chair.save()

        chairs = models.ChairsData.objects.filter(event=event)

        return ChairsDataSerializer(chairs, many=True).data

class SketchDataSerializer(serializers.ModelSerializer):
    '''A serializer for sketch event.'''

    image_url_url = serializers.SerializerMethodField()

    class Meta:
        model = models.SketchData
        fields = ('id', 'event', 'image_url', 'description', 'image_url_url')

    def get_image_url_url(self, obj):
        return ImageSerializer(obj.image_url).data.get('image')

class SketchPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SketchData
        fields = ('image_url', 'description')

    def create(self, user):
        event = models.EventData.objects.get(user_profile=user)

        sketches = models.SketchData.objects.filter(event=event)
        for sketch in sketches:
            sketch.delete()

        sketch = models.SketchData(
            description = self.data.get('description'),
            image_url = models.ImageData.objects.get(id=self.data.get('image_url')),
            event = event
        )

        sketch.save()

        return SketchDataSerializer(sketch).data

class DevelopersDataSerializer(serializers.ModelSerializer):
    '''A serializer for developers event.'''

    person_data = serializers.SerializerMethodField()

    class Meta:
        model = models.DevelopersData
        fields = ('id', 'event', 'person', 'person_data')

    def get_person_data(self, obj):
        return PeopleDataSerializer(obj.person).data

class DeveloperPOSTSerializer(serializers.Serializer):

    people = serializers.ListField(required=True)

    def create(self, user):

        event = models.EventData.objects.get(user_profile=user)
        developers = models.DevelopersData.objects.filter(event=event)

        for developer in developers:
            developer.delete()

        for person in self.data.get('people'):
            developer = models.DevelopersData(
                event = event,
                person = models.PeopleData.objects.get(id=person)
            )
            developer.save()

        developers = models.DevelopersData.objects.filter(event=event)

        return DevelopersDataSerializer(developers, many=True).data

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

class StreamPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StreamData
        fields = ('url', 'description')

    def create(self, user):
        event = models.EventData.objects.get(user_profile=user)

        stream = models.StreamData(
            url = self.data.get('url'),
            description = self.data.get('description'),
            event = event
        )

        stream.save()

        return StreamDataSerializer(stream).data

class SponsorDataSerializer(serializers.ModelSerializer):

    person_data = serializers.SerializerMethodField()

    class Meta:
        model = models.SponsorData
        fields = ('id', 'person', 'event', 'person_data')

    def get_person_data(self, obj):
        return PeopleDataSerializer(obj.person).data

class SponsorPOSTSerializer(serializers.Serializer):

    people = serializers.ListField(required=True)

    def create(self, user):

        event = models.EventData.objects.get(user_profile=user)
        sponsors = models.SponsorData.objects.filter(event=event)

        for sponsor in sponsors:
            sponsor.delete()

        for person in self.data.get('people'):
            sponsor = models.SponsorData(
                event = event,
                person = models.PeopleData.objects.get(id=person)
            )
            sponsor.save()

        sponsors = models.SponsorData.objects.filter(event=event)

        return SponsorDataSerializer(sponsors, many=True).data

class ActivityTypeDataSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.ActivityTypeData
        fields = ('id', 'name', 'description', 'created', 'show_in_app', 'event', 'image', 'image_url')

    def get_image_url(self, obj):
        return ImageSerializer(obj.image).data.get('image')

class ActivityTypePOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ActivityTypeData
        fields = ('name', 'description', 'show_in_app', 'image')
        extra_kwargs = {'show_in_app': {'required': True}}

    def create(self, user):

        event = models.EventData.objects.get(user_profile=user)

        activityType = models.ActivityTypeData(
            name = self.data.get('name'),
            description = self.data.get('description'),
            show_in_app = self.data.get('show_in_app'),
            image = models.ImageData.objects.get(id=self.data.get('image')),
            event = event
        )

        activityType.save()

        return ActivityTypeDataSerializer(activityType).data

class ActivityDataSerializer(serializers.ModelSerializer):

    activity_type_name = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    place_name = serializers.SerializerMethodField()
    activity_type_image = serializers.SerializerMethodField()

    class Meta:
        model = models.ActivityData
        fields = ('id', 'title', 'subtitle', 'description', 'notes', 'price', 'start_date', 'end_date', 'activity_type', 'place', 'schedule', 'activity_type_name', 'date', 'place_name', 'activity_type_image')

    def get_activity_type_name(self, obj):
        return obj.activity_type.name

    def get_date(self, obj):
        return obj.start_date.strftime("%a %b %d %H:%M") + ' - ' + obj.end_date.strftime("%a %b %d %H:%M")

    def get_place_name(self, obj):
        return obj.place.name

    def get_activity_type_image(self, obj):
        return ImageSerializer(obj.activity_type.image).data.get('image')

class ActivityPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ActivityData
        fields = ('title', 'subtitle', 'description', 'notes', 'price', 'start_date', 'end_date', 'activity_type', 'place')
        extra_kwargs = {'price': {'required': True}}

    def create(self, user):

        event = models.EventData.objects.get(user_profile=user)
        schedule = models.ScheduleData.objects.get(event=event)
        placeCategories = models.PlaceCategoryData.objects.filter(event=event)

        activity = models.ActivityData(
            title = self.data.get('title'),
            subtitle = self.data.get('subtitle'),
            description = self.data.get('description'),
            notes = self.data.get('notes'),
            price = self.data.get('price'),
            start_date = self.data.get('start_date'),
            end_date = self.data.get('end_date'),
            activity_type = models.ActivityTypeData.objects.get(id=self.data.get('activity_type'), event=event),
            place = models.PlaceData.objects.get(id=self.data.get('place'), place_category__in=placeCategories),
            schedule = schedule
        )

        activity.save()

        return ActivityDataSerializer(activity).data

class ActivityPeopleDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ActivityPeopleData
        fields = ('id', 'activity', 'person')

class ActivityPeoplePOSTSerializer(serializers.ModelSerializer):

    person = serializers.ListField(required=True)

    class Meta:
        model = models.ActivityPeopleData
        fields = ('activity', 'person')

    def create(self, user):
        activityPeople = []
        activity = models.ActivityData.objects.get(id=self.data.get('activity'))

        for person in self.data.get('person'):

            activityPerson = models.ActivityPeopleData(
                activity = activity,
                person = models.PeopleData.objects.get(id=person)
            )

            activityPerson.save()
            activityPeople.append(activityPerson)

        return ActivityPeopleDataSerializer(activityPeople, many=True).data

class PeopleDataSerializer(serializers.ModelSerializer):

    photo_url = serializers.SerializerMethodField()
    provenance_name = serializers.SerializerMethodField()

    class Meta:
        model = models.PeopleData
        fields = ('id', 'name', 'surname', 'birthdate', 'photo', 'resume', 'email', 'phone', 'provenance', 'event', 'photo_url', 'provenance_name')

    def get_photo_url(self, obj):
        return ImageSerializer(obj.photo).data.get('image')

    def get_provenance_name(self, obj):
        return obj.provenance.name

class PeoplePOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model= models.PeopleData
        fields = ('name', 'surname', 'birthdate', 'photo', 'resume', 'email', 'phone', 'provenance')

    def create(self, user):
        event = models.EventData.objects.get(user_profile=user)

        person = models.PeopleData(
            name = self.data.get('name'),
            surname = self.data.get('surname'),
            birthdate = self.data.get('birthdate'),
            photo = models.ImageData.objects.get(pk=self.data.get('photo')),
            resume = self.data.get('resume'),
            email = self.data.get('email'),
            phone = self.data.get('phone'),
            provenance = models.PlaceData.objects.get(pk=self.data.get('provenance')),
            event = event
        )

        person.save()

        return PeopleDataSerializer(person).data

class PeopleSocialNetwoeksDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PeopleSocialNetworksData
        fields = '__all__'

class PlaceCategoryDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PlaceCategoryData
        fields = '__all__'

class PlaceCategoryPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PlaceCategoryData
        fields = ('name', 'description', 'show_in_app')
        extra_kwargs = {'show_in_app': {'required': True}}

    def create(self, user):
        event = models.EventData.objects.get(user_profile=user)
        placeCategory = models.PlaceCategoryData(
            name = self.data.get('name'),
            description = self.data.get('description'),
            show_in_app = self.data.get('show_in_app'),
            event = event
        )

        placeCategory.save()

        return PlaceCategoryDataSerializer(placeCategory).data

class PlaceDataSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()
    place_category_name = serializers.SerializerMethodField()

    class Meta:
        model = models.PlaceData
        fields = '__all__'

    def get_image_url(self, obj):
        return ImageSerializer(obj.image).data.get('image')

    def get_place_category_name(self, obj):
        return obj.place_category.name

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

        schedule = models.ScheduleData(
            event = event
        )

        schedule.save()

        return EventDataSerializer(event).data

class EventPATCHSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventData
        fields = ('name', 'code', 'description', 'start_date', 'end_date', 'place')
        extra_kwargs = {
            'name': {'required': False},
            'code': {'required': False},
            'description': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False},
            'place': {'required': False}
        }

    def partial_update(self, user, pk):

        event = models.EventData.objects.get(id=pk, user_profile=user)
        print(self.data.get('place'))
        #
        if self.data.get('place'):
            placeCateory = models.PlaceCategoryData.objects.filter(event=event)
            place = models.PlaceData.objects.get(id=self.data.get('place'), place_category__in=placeCateory)
            event.place = place

        event.save()

        return EventDataSerializer(event).data
