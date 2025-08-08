from rest_framework import serializers
from datetime import date

def validated_date_of_birth(value):

    if not isinstance(value,date):
        raise serializers.ValidationError('Date of birth must be in the format YYYY-MM-DD')

    current_date = date.today()

    age = current_date.year - value.year - ((current_date.month,current_date.day) < (value.month,value.day))

    if age < 18:
        raise serializers.ValidationError('Age must be greater than or equal to 18')
    if age > 120:
        raise serializers.ValidationError('Age cannot be more than 120')
    return value