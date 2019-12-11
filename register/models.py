import uuid
from django.db import models
from account.models import User
from utils.models import BaseAbstractModel
from utils.managers import CustomQuerySet, RegistrationQuery, RegistrationEnquiryQuery


class Registration(models.Model):

    SHIRT_SIZE = (
        ('S', 'SMALL'),
        ('M', 'MEDIM'),
        ('L', 'LARGE'),
        ('XL', 'EXTRA LARGE'),
        ('XXL', 'EXTRA EXTRA LARGE')
    )

    EDUCATION = (
        ('P', 'PRIMARY'),
        ('S', 'SECONDARY'),
        ('T', 'TERTIARY')
    )

    SPONSORED = (
        ('Y', 'YES'),
        ('N', 'NO')
    )

    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    otherName = models.CharField(max_length=50)
    dateOfBirth = models.DateField()
    phoneNumber = models.CharField(max_length=16)
    phoneNumberOwner = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    emailOwner = models.CharField(max_length=100)
    educationLevel = models.CharField(max_length=1, choices=EDUCATION)
    educationClass = models.CharField(max_length=50)
    career = models.CharField(max_length=255)
    nextOfKin1Title = models.CharField(max_length=50)
    nextOfKin1Name = models.CharField(max_length=255)
    nextOfKin1Number = models.CharField(max_length=16)
    nextOfKin2Title = models.CharField(max_length=50)
    nextOfKin2Name  = models.CharField(max_length=255)
    nextOfKin2Number = models.CharField(max_length=16)
    shirtSize = models.CharField(max_length=3, choices=SHIRT_SIZE)
    tribe = models.CharField(max_length=255)
    homeChurch = models.CharField(max_length=255)
    otherChurches = models.CharField(max_length=255)
    sponsored = models.CharField(max_length=1, choices=SPONSORED)
    health = models.TextField()
    createdBy = models.ForeignKey(User, to_field="username", null=True, blank=True, on_delete=models.DO_NOTHING)
    is_published = models.BooleanField(default=True)
    createdAt = models.DateField(null=True, blank=True)
    updatedAt = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = RegistrationQuery.as_manager()

    def __str__(self):
        return self.firstName, self.lastName


class RegistrationEnquiry(BaseAbstractModel):
    """This class defines the model for enquiries that are made by the user"""

    enquiry_id = models.CharField(
        max_length=100, blank=True, unique=True, default=uuid.uuid4)
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='client')
    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='enquiry_requester')
    target_property = models.ForeignKey(
        Registration, on_delete=models.CASCADE, related_name='enquired_property')
    visit_date = models.DateTimeField()
    message = models.TextField(max_length=1000)
    is_resolved = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = RegistrationEnquiryQuery.as_manager()

    def __str__(self):
        return f'Enquiry {self.enquiry_id} by {self.requester}'
