from django_filters import FilterSet
from django_filters import rest_framework as filters
from register.models import Registration


class RegistrationFilter(FilterSet):
    """
    Create a filter class that inherits from FilterSet. This class will help
    us search for properties using specified fields.
    """
    sponsored = filters.CharFilter(lookup_expr='icontains')
    createdBy = filters.CharFilter(lookup_expr='icontains')
    nextOfKin1Name = filters.CharFilter(lookup_expr='icontains')
    nextOfKin2Name = filters.CharFilter(lookup_expr='icontains')
    phoneNumberOwner = filters.CharFilter(lookup_expr='icontains')
    emailOwner = filters.CharFilter(lookup_expr='icontains')
    dateOfBirth = filters.RangeFilter()

    class Meta:
        model = Registration
        fields = (
            'firstName',
            'lastName',
            'otherName',
            'dateOfBirth',
            'phoneNumberOwner',
            'email',
            'emailOwner',
            'educationLevel',
            'educationClass',
            'career',
            'nextOfKin1Name',
            'nextOfKin2Name',
            'tribe',
            'sponsored',
            'createdBy',
        )