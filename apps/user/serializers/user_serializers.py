from rest_framework import serializers
from apps.user.models.models import UserProfileModel
from apps.user.validations.validation_email import validated_email
from apps.user.validations.validation_username import validated_username
from apps.user.validations.validation_phone_number import validated_phone_number
from apps.user.validations.validation_password import validated_password
from apps.user.validations.validation_date_of_birth import validated_date_of_birth
from apps.booking.serializers.serializer_address import  AddressUserRegistrationSerializer
from django.contrib.auth.models import User
from apps.user.choices.user_choices import GENDER_CHOICES,ROLE_CHOICES


class UserBasicSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfileModel
        fields = ['id', 'username', 'email', 'phone_number']


class UserProfileDetailSerializers(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    addresses = AddressUserRegistrationSerializer(many=True)

    class Meta:
        model = UserProfileModel
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'gender', 'role','addresses']

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user', {})
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            if 'password' in user_data:
                user.set_password(user_data['password'])
            user.save()


        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.role = validated_data.get('role',instance.role)
        instance.save()

        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True,validators=[validated_password], style={'input type':'password'})
    username = serializers.CharField(required=True,validators=[validated_username])
    email = serializers.EmailField(required=True, validators=[validated_email])
    phone_number = serializers.CharField(validators=[validated_phone_number])
    date_of_birth = serializers.DateField(validators=[validated_date_of_birth])
    gender = serializers.ChoiceField(choices=GENDER_CHOICES,required=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES,default='T')
    address = AddressUserRegistrationSerializer()

    class Meta:
        model = UserProfileModel
        fields = ['username', 'email','first_name', 'last_name', 'password', 'phone_number', 'role', 'date_of_birth','gender','address']


    def create(self, validated_data):
        address_data = validated_data.pop('address')


        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )

        user_profile = UserProfileModel.objects.create(
            user=user,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data['phone_number'],
            date_of_birth=validated_data['date_of_birth'],
            gender=validated_data['gender'],
            role=validated_data.get('role')
        )

        address_serializer = AddressUserRegistrationSerializer(data=address_data, context={'user_profile': user_profile})
        address_serializer.is_valid(raise_exception=True)
        address = address_serializer.save()

        user_profile.address = address
        user_profile.save()

        return user_profile


