from django.shortcuts import render
from datetime import datetime as dt
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from register.serializers import RegistrationSerializer
from register.renderers import RegistrationJSONRenderer
from register.models import Registration, RegistrationEnquiry
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from register.filters import RegistrationFilter
from utils.permissions import (
    CanEditUsers,
    # IsClientAdmin,
    IsOwner,
    ReadOnly,
)


class CreateAndListRegistrationView(generics.ListCreateAPIView):
    """Handle requests for creation of property"""

    serializer_class = RegistrationSerializer
    # permission_classes = (IsClientAdmin | ReadOnly,)
    renderer_classes = (RegistrationJSONRenderer,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filter_class = RegistrationFilter
    search_fields = (
        'firstName',
        'lastName',
        'otherName',
        'nextOfKin1Name',
        'nextOfKin2Name',
        'sponsored')
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        """Change the queryset to use depending
        on the user making the request"""
        user = self.request.user

        if user.is_authenticated and user.role == 'FA':
            # admins view all clients, no filtering
            return Registration.objects.all()

        if user.is_authenticated and user.role == 'CA':
            # other users can only see published clients
            return Registration.active_objects.all_published()


    def create(self, request, *args, **kwargs):
        """Create a client listing and save it to the database.
        """
        # enable the request body to be mutable so that we can
        # modify the data to pass to the DB
        request.POST._mutable = True
        payload = request.data
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'data': {"user": serializer.data}
        }
        return Response(response, status=status.HTTP_201_CREATED)
