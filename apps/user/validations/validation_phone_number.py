from rest_framework import serializers
from apps.user.models.models import UserProfileModel
import re


def validated_phone_number(value,instance=None):
    phone_regex = r'^\+\d+$'
    if not re.match(phone_regex, value):
        raise serializers.ValidationError('The phone number must start with "+" and contain only numbers.')
    if len(value) < 8 or len(value) > 15:
        raise serializers.ValidationError('The number length must be from 8 to 15 characters')
    if instance and instance.phone_number == value :
        return value
    user = instance.user if instance else None
    if user and UserProfileModel.objects.filter(phone_number=value).exclude(id=user.id).exists():
        raise serializers.ValidationError(f'Phone numer {value} is exists')
    return value