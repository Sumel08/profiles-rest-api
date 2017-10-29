from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class UserProfileManager(BaseUserManager):
	'''Helps django work with our custom user model'''

	def create_user(self, email, name, password=None):
		'''Creates a new user profile object'''

		if not email:
			raise ValueError('Users must have an email address.')

		email = self.normalize_email(email)
		user = self.model(email=email, name=name)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, name, password):
		'''CReates and saves a new superuserwith given details.'''
		user = self.create_user(email, name, password)

		user.is_superuser = True
		user.is_staff = True

		user.save(using=self._db)

		return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
	'''User profile inside our system'''

	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserProfileManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	def get_full_name(self):
		'''Use to get a users full name.'''

		return self.name

	def get_short_name(self):
		'''Used to get a short name'''

		return self.name

	def __str__(self):
		'''Django used this when it needs to convert the object to a string'''

		return self.email

class ProfileFeedItem(models.Model):
	'''Profile status update.'''

	user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
	status_text = models.CharField(max_length=255)
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		'''Return the model as a string'''

		return self.status_text

# Models for WITCOM 2017
class EventData(models.Model):
	'''Event model for WITCOM'''

	user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=255)
	description = models.CharField(max_length=1000)
	created_on = models.DateTimeField(auto_now_add=True)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	# event_image_url = models.URLField(null=True)
	# event_image = models.ImageField(null=True)
	event_image = models.ForeignKey('ImageData', null=False)
	place = models.ForeignKey('PlaceData', null=True)
	schedule = models.ForeignKey('ScheduleData', null=True)

	def __str__(self):
		'''Return the name of the event'''

		return self.name

class ChairsData(models.Model):
	''' Model for Chairs in WITCOM 2017'''

	event = models.ForeignKey('EventData')
	person = models.ForeignKey('PeopleData')

class SketchData(models.Model):
	event = models.ForeignKey('EventData')
	# image_url = models.URLField()
	image_url = models.ForeignKey('ImageData', null=False)
	description = models.CharField(max_length=255)

class DevelopersData(models.Model):
	event = models.ForeignKey('EventData')
	person = models.ForeignKey('PeopleData')

class ScheduleData(models.Model):
	created_on = models.DateTimeField(auto_now_add=True)
	event = models.ForeignKey('EventData')

	def __str__(self):

		return self.event.name

class StreamData(models.Model):
	url = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	event = models.ForeignKey('EventData')

class SponsorData(models.Model):
	person = models.ForeignKey('PeopleData')
	event = models.ForeignKey('EventData')

class ActivityTypeData(models.Model):
	name = models.CharField(max_length=25)
	description = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	show_in_app = models.BooleanField(default=False)
	image = models.ForeignKey('ImageData', null=False)
	show_speakers_in_app = models.BooleanField(default=False)
	event = models.ForeignKey('EventData')

class ActivityData(models.Model):
	title = models.CharField(max_length=255)
	subtitle = models.CharField(max_length=255)
	description = models.CharField(max_length=1000)
	notes = models.CharField(max_length=255)
	price = models.FloatField(null=True)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	activity_type = models.ForeignKey('ActivityTypeData')
	place = models.ForeignKey('PlaceData')
	schedule = models.ForeignKey('ScheduleData')

class ActivityPeopleData(models.Model):
	activity = models.ForeignKey('ActivityData')
	person = models.ForeignKey('PeopleData')

class PeopleData(models.Model):
	name = models.CharField(max_length=255)
	surname = models.CharField(max_length=255)
	birthdate = models.DateField()
	photo = models.ForeignKey('ImageData', null=False)
	resume = models.CharField(max_length=1000)
	email = models.EmailField(max_length=255)
	phone = models.CharField(max_length=20)
	provenance = models.ForeignKey('PlaceData')
	event = models.ForeignKey('EventData')

class PeopleSocialNetworksData(models.Model):
	person = models.ForeignKey('PeopleData')
	social_network = models.ForeignKey('SocialNetworksData')

class PlaceCategoryData(models.Model):
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	show_in_app = models.BooleanField(default=False)
	event = models.ForeignKey('EventData')

class PlaceData(models.Model):
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=1000)
	longitude = models.CharField(max_length=255)
	latitude = models.CharField(max_length=255)
	altitude = models.CharField(max_length=255)
	indication = models.CharField(max_length=255)
	additional_info = models.CharField(max_length=255)
	website = models.URLField()
	email = models.EmailField()
	telephone = models.CharField(max_length=20)
	# image = models.URLField()
	image = models.ForeignKey('ImageData', null=False)
	place_category = models.ForeignKey('PlaceCategoryData')

class PlaceSocialNetworksData(models.Model):
	place = models.ForeignKey('PlaceData')
	social_networks = models.ForeignKey('SocialNetworksData')

class SocialNetworksData(models.Model):
	url = models.URLField()
	domain = models.CharField(max_length=255)
	event = models.ForeignKey('EventData')

class ImageData(models.Model):
	image = models.ImageField(null=False)
