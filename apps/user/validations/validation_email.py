from rest_framework import serializers
from django.contrib.auth.models import User

def validated_email(value,instance=None):
    if instance and instance.name == value:
        return value

    user = instance.user if instance else None
    if user and User.objects.filter(email=value).exclude(id=user.id).exists():
        raise serializers.ValidationError(f'Email: {value} is exists')
    return value
