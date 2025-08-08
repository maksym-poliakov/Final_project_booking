from rest_framework import serializers
from apps.booking.models.models_habitation import HabitationModel
from apps.booking.models.models_booking import BookingModel
from apps.user.serializers.user_serializers import UserBasicSerializer
from apps.booking.serializers.serializer_habitation import(
    HabitationListSerializer,

)
from django.utils import timezone


class BookingListSerializer(serializers.ModelSerializer):
    housing_details = HabitationListSerializer()
    user = UserBasicSerializer()
    total_price = serializers.SerializerMethodField()


    def get_total_price(self,obj):
        start_date = obj.start_date
        end_date =  obj.end_date
        price = obj.housing_details.price
        count_days = end_date - start_date
        total_price = count_days.days * price
        return {'count_days':count_days.days,'total_price':total_price}


    class Meta:
        model = BookingModel
        fields = ['id','start_date','end_date','total_price','status_order','confirmation','housing_details','user']


class BookingRetrieveUpdateDestroyViewSerializer(serializers.ModelSerializer):
    housing_details = serializers.PrimaryKeyRelatedField(queryset = HabitationModel.objects.all())
    tenant = UserBasicSerializer(source='user')


    class Meta:
        model = BookingModel
        fields = ['id','start_date','end_date','tenant','is_active','housing_details']


    def validate(self,data):
        if data['end_date'] <= data['start_date'] :
            raise serializers.ValidationError({'end_date': 'End date must be greater than start date.'})
        if data['start_date'] < timezone.now().date():
            raise serializers.ValidationError({'message': 'Booking date cannot be in the past'})

        user = data.get('user')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        housing_details = data.get('housing_details')

        if user and housing_details and start_date and end_date :
            exists_booking = BookingModel.objects.filter(
                user=user,
                start_date=start_date,
                end_date=end_date,
                housing_details=housing_details
            ).exists()
            if exists_booking:
                raise serializers.ValidationError(
                    {'detail': 'A booking with these details already exists for this user.'})

        return data


class BookingLandlordUpdateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    housing_details = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = BookingModel
        fields = ['id','start_date','end_date','user','confirmation','housing_details']