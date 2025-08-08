from django.contrib.auth.models import User
from rest_framework import serializers

def validated_username(value,instance=None):
    if instance and instance.username == value:
        return value
    if User.objects.filter(username=value).exists():
        raise serializers.ValidationError(f'Username: {value} is exists')
    return value