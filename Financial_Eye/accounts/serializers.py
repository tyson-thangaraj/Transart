__author__ = 'fanfan'

from rest_framework import serializers
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from accounts.models import Users

class UserSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        return Users.objects.create(**validated_data)
    #def update(args):
    
    class Meta:
        model = Users
        fields = ('Username', 'Password', 'Email', 'FirstName', 'LastName', 'Address', 'Telephone', 'DateJoined')

    
        