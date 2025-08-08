from rest_framework import serializers

from apps.booking.models import BookingModel
from apps.booking.models.models_reviews import ReviewModel


class ReviewsDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    tenant = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()


    def get_owner(self,obj):
        owner = obj.booking.housing_details.address.user
        return {'id':owner.id,
                'username':owner.user.username
                }


    def get_tenant(self,obj):
        tenant = obj.booking.user
        return {
            'id':tenant.id,
            'username':tenant.user.username
        }


    def get_avg_rating(self, obj):
        habitation = obj.booking.housing_details
        return habitation.avg_rating


    class Meta:
        model = ReviewModel
        fields = ['id','tenant','booking','comment','owner','rating','avg_rating']


class ReviewsCreateSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(queryset=BookingModel.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = ReviewModel
        fields = ['id', 'user', 'booking', 'comment', 'rating']


    def validate(self, data):
        booking = self.context.get('booking')
        user_tenant = self.context['request'].user

        if not booking or not isinstance(booking, BookingModel):
            raise serializers.ValidationError({'message': 'Invalid or missing booking'})

        if not booking.user.id == user_tenant.id:
            raise serializers.ValidationError({'message': 'You can\'t leave a review'})

        if not booking.status_order == 'completed':
            raise serializers.ValidationError({'message': 'Feedback can only be left for a completed booking.'})

        if ReviewModel.objects.filter(user=user_tenant.profile, booking=booking).exists():
            raise serializers.ValidationError({"booking": "You have already submitted a review for this booking."})

        return data


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.profile
        validated_data['booking'] = self.context['booking']
        return super().create(validated_data)