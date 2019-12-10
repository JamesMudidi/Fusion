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
    IsClientAdmin,
    IsOwner,
    ReadOnly,
)


class CreateAndListRegistrationView(generics.ListCreateAPIView):
    """Handle requests for creation of property"""

    serializer_class = RegistrationSerializer
    permission_classes = (IsClientAdmin | ReadOnly,)
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

        if user.is_authenticated and user.role == 'LA':
            # admins view all property, no filtering
            return Registration.objects.all()

        if user.is_authenticated and user.employer.first():
            # if the user is a client_admin, they see all published property
            # and also their client's published and unpublished property.
            client = user.employer.first()
            return Registration.active_objects.all_published_and_all_by_client(
                client=client)

        # other users only see published property
        return Registration.active_objects.all_published()

    def create(self, request, *args, **kwargs):
        """Create a property listing and save it to the database.
        We pass image and video files to be uploaded to Cloudinary
        we expect URLs to be returned. It is these URLs that we
        pass to be serialized and then saved if everything is okay.
        """
        # enable the request body to be mutable so that we can
        # modify the data to pass to the DB
        request.POST._mutable = True
        payload = request.data
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'data': {"register": serializer.data}
        }
        return Response(response, status=status.HTTP_201_CREATED)
