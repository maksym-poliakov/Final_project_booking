from rest_framework import serializers
from apps.booking.models.models_habitation import HabitationModel
from apps.booking.models.models_address import AddressModel
from apps.booking.serializers.serializer_address import (
    AddressDetailSerializer,
    AddressListCreateSerializer,
    AddressRetrieveUpdateDestroySerializer,
)


class HabitationListSerializer(serializers.ModelSerializer):
    address = AddressDetailSerializer()
    class Meta:
        model = HabitationModel
        fields = ['id','title','description','type_housing','number_of_rooms','status','address','price','avg_rating']


class HabitationDetailSerializer(serializers.ModelSerializer):
    address = AddressDetailSerializer(many=True)
    class Meta:
        model = HabitationModel
        fields = ['id','title','description','type_housing','number_of_rooms','address','status','price']


class HabitationListCreateSerializer(serializers.ModelSerializer):
    address = AddressListCreateSerializer()
    class Meta:
        model = HabitationModel
        fields = ['id','title', 'description', 'type_housing', 'number_of_rooms','address','status','price']


    def create(self, validated_data):
        address_data = validated_data.pop('address')
        request = self.context.get('request')
        user_profile = request.user.profile if request and request.user.is_authenticated else None

        if not user_profile:
            raise serializers.ValidationError({'message': 'User profile not found'})

        address, created = AddressModel.objects.get_or_create(
            street=address_data['street'],
            city=address_data['city'],
            postcode=address_data['postcode'],
            haus_number=address_data['haus_number'],
            user=user_profile,
            defaults={
                'house_letter': address_data.get('house_letter'),
            }
        )
        if HabitationModel.objects.filter(
            title=validated_data['title'],
            description=validated_data['description'],
            type_housing=validated_data['type_housing'],
            status=validated_data['status'],
            number_of_rooms=validated_data['number_of_rooms'],
            price=validated_data['price'],
            address=address
        ).exists():
            raise serializers.ValidationError({'message': 'This habitation already exists'})

        habitation = HabitationModel.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            type_housing=validated_data['type_housing'],
            status=validated_data['status'],
            number_of_rooms=validated_data['number_of_rooms'],
            price=validated_data['price'],
            address=address
        )
        return habitation


class HabitationRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    address = AddressRetrieveUpdateDestroySerializer()


    class Meta:
        model = HabitationModel
        fields = ['id','title', 'description', 'type_housing', 'number_of_rooms', 'address', 'status','price']


    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address_serializer = AddressRetrieveUpdateDestroySerializer(instance.address,data=address_data)
        address_serializer.is_valid(raise_exception=True)
        address_serializer.save()

        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.type_housing = validated_data.get('type_housing',instance.type_housing)
        instance.status = validated_data.get('status',instance.status)
        instance.number_of_rooms = validated_data.get('number_of_rooms',instance.number_of_rooms)
        instance.price = validated_data.get('price',instance.price)

        if HabitationModel.objects.exclude(id=instance.id).filter(
                title=instance.title,
                description=instance.description,
                type_housing=instance.type_housing,
                number_of_rooms=instance.number_of_rooms,
                status=instance.status,
                address=instance.address
        ).exists():
            raise serializers.ValidationError(
                {'message': 'This combination of fields already exists for another habitation.'})

        instance.save()

        return instance