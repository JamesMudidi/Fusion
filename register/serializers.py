from django.contrib.auth import authenticate
from rest_framework import serializers
from register.models import Registration
from django.core.validators import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    """This class handles serializing and
       deserializing of Registration objects"""

    firstname = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Kindly provide us with your First name",
            "blank": "The First name field cannot be left blank"
        }
    )

    lastname = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Kindly provide us with your Last name",
            "blank": "The Last name field cannot be left blank"
        }
    )

    class Meta:
        model = Registration
        exclude = ('is_deleted',)
        read_only_fields = ('view_count', 'slug', 'createdBy',
                            'publish_status', 'createdAt', 'updatedAt', 'delete_status')
