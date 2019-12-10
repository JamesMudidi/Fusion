import uuid
from django.db import models
from account.models import User


class Registation(models.Model):

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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, format='int')
    slug = models.SlugField(max_length=250, unique=True)
    title = models.CharField(max_length=255)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    otherName = models.CharField(max_length=50)
    dateOfBirth = models.DateField()
    phoneNumber = models.CharField(max_length=16)
    phoneNumberOwner = models.CharField()
    email = models.EmailField()
    emailOwner = models.CharField()
    educationLevel = models.CharField(max_length=1, choices=EDUCATION)
    educationClass = models.CharField()
    career = models.CharField()
    nextOfKin1Title = models.CharField()
    nextOfKin1Name = models.CharField()
    nextOfKin1Number = models.CharField()
    nextOfKin2Title = models.CharField()
    nextOfKin2Name  = models.CharField()
    nextOfKin2Number = models.CharField()
    shirtSize = models.CharField(max_length=3, choices=SHIRT_SIZE)
    tribe = models.CharField(max_length=100)
    homeChurch = models.CharField()
    otherChurches = models.CharField()
    otherChurches = models.CharField()
    sponsored = models.CharField(max_length=1, choices=SPONSORED)
    health = models.TextField()
    createdBy = models.ForeignKey(User, to_field="username", on_delete=models.DO_NOTHING)
    publish_status = models.BooleanField(default=True)
    createdAt = models.DateField(null=True, blank=True)
    updatedAt = models.DateField(null=True, blank=True)
    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return self.title
