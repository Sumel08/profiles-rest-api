from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers

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
