from rest_framework.permissions import BasePermission,SAFE_METHODS
from apps.booking.models.models_booking import BookingModel
from apps.user.models.models import UserProfileModel
from django.core.exceptions import ObjectDoesNotExist


class IsUser(BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in SAFE_METHODS and request.user.is_staff:
            return True
        return  obj.user == request.user


class IsTenantOrLandlord(BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False
        try:
            user_profile = UserProfileModel.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return False

        if user_profile.role == 'L':
            return True

        if not BookingModel.objects.filter(user=user_profile).exists():
            return True
        return  user_profile.id == request.user.id


    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id

class IsRoleMethod(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            user_profile = UserProfileModel.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return False
        if request.method in ['PUT', 'PATCH','GET'] and user_profile.role == 'L':
            return  obj.housing_details.address.user.id == user_profile.id
        if request.method in ['PUT','PATCH','GET','POST','DELETE'] and user_profile.role == 'T':
            return obj.user.id == request.user.id
        return False