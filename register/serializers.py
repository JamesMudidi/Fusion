from django.contrib.auth import authenticate
from rest_framework import serializers
from register.models import Registration
from django.core.validators import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    """This class handles serializing and
       deserializing of Registration objects"""

    firstName = serializers.CharField(
        required=True,
        error_messages={
            "error": "Hello, Kindly provide us with your First name"
        }
    )

    lastName = serializers.CharField(
        required=True,
        error_messages={
            "error": "Hello, Kindly provide us with your Last name",
        }
    )

    dateOfBirth = serializers.DateField(
        required=True,
        error_messages={
            "error": "Hello, Kindly provide us with your date of birth",
        }
    )

    phoneNumber = serializers.CharField(
        required=True,
        error_messages={
            "error": "Hello, Kindly provide us with a working Phone Number that we can contact you on",
        }
    )

    phoneNumberOwner = serializers.CharField(
        required=True,
        error_messages={
            "error": "Hello, Kindly let us know who owns this Phone number",
        }
    )

    email = serializers.EmailField(
        required=True,
        error_messages={
            "error": "Hello, Kindly provide us with a working Email that we can contact you on",
        }
    )

    emailOwner = serializers.CharField(
        required=True,
        error_messages={
            "error": "Hello, Kindly let us know who owns this Email",
        }
    )

    nextOfKin1Title = serializers.CharField(
        required=True,
        error_messages={
            "error": "Hello, How are you related",
        }
    )

    nextOfKin1Name = serializers.CharField(
        required=True,
        error_messages={
            "error": "Hello, Kindly provide us with the Name of your Next of kin",
        }
    )

    nextOfKin1Number = serializers.CharField(
        required=True,
        error_messages={
            "error": "Hello, Kindly provide us with the Phone number of your next of kin",
        }
    )

    tribe = serializers.CharField(
        required=True,
        error_messages={
            "error": "Hello, Kindly let us know your Tribe",
        }
    )

    homeChurch = serializers.CharField(
        required=True,
        error_messages={
            "error": "Hello, Kindly let us know where you fellowship from",
        }
    )

    sponsored = serializers.CharField(
        required=True,
        error_messages={
            "error": "Hello, Are you sponsered by Compassion",
        }
    )

    class Meta:
        model = Registration
        fields = ('firstName', 'lastName', 'dateOfBirth', 'phoneNumber',
                'phoneNumberOwner', 'email', 'emailOwner', 'nextOfKin1Title',
                'nextOfKin1Name', 'nextOfKin1Number', 'tribe', 'homeChurch', 'sponsored')
        read_only_fields = ('createdBy', 'publish_status', 'createdAt',
                            'updatedAt', 'delete_status')