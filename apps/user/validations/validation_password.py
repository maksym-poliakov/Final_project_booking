from django.contrib.auth.models import User
from rest_framework import serializers
import re

def validated_password(value):

    if len(value) < 8 or len(value) > 12:
        raise serializers.ValidationError('password must be 8 - 12 symbols ')
    if not any(char.isupper() for char in value):
        raise serializers.ValidationError('The password must contain at least one capital letter')
    if not re.search(r'[1-9]', value):
        raise serializers.ValidationError('the password must contain at least one digit')
    if not any(char.islower() for char in value):
        raise serializers.ValidationError('The password must contain at least one lowercase letter')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise serializers.ValidationError('The password must contain at least one special character.')
    return value