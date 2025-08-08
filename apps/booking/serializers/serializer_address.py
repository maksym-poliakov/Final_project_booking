from rest_framework import serializers
from apps.booking.models.models_address import AddressModel


class AddressListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ['id','city','street','postcode','haus_number','house_letter']


    def create(self, validated_data):
        user_profile = self.context.get('user_profile')
        if not user_profile:
            raise serializers.ValidationError({"user": "UserProfile is required to create an address."})
        validated_data['user'] = user_profile
        return AddressModel.objects.create(**validated_data)


class AddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ['id','city','street','postcode','haus_number','house_letter']


class AddressUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ['id', 'city', 'street', 'postcode', 'haus_number', 'house_letter']


    def create(self, validated_data):
        user_profile = self.context.get('user_profile')
        if not user_profile:
            raise serializers.ValidationError("UserProfile must be provided in context")
        validated_data['user'] = user_profile
        return super().create(validated_data)


class AddressRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ['id', 'city', 'street', 'postcode', 'haus_number', 'house_letter']