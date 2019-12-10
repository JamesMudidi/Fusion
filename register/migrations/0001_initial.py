# Generated by Django 2.1 on 2019-12-10 22:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('otherName', models.CharField(max_length=50)),
                ('dateOfBirth', models.DateField()),
                ('phoneNumber', models.CharField(max_length=16)),
                ('phoneNumberOwner', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('emailOwner', models.CharField(max_length=100)),
                ('educationLevel', models.CharField(choices=[('P', 'PRIMARY'), ('S', 'SECONDARY'), ('T', 'TERTIARY')], max_length=1)),
                ('educationClass', models.CharField(max_length=50)),
                ('career', models.CharField(max_length=255)),
                ('nextOfKin1Title', models.CharField(max_length=50)),
                ('nextOfKin1Name', models.CharField(max_length=50)),
                ('nextOfKin1Number', models.CharField(max_length=50)),
                ('nextOfKin2Title', models.CharField(max_length=50)),
                ('nextOfKin2Name', models.CharField(max_length=50)),
                ('nextOfKin2Number', models.CharField(max_length=50)),
                ('shirtSize', models.CharField(choices=[('S', 'SMALL'), ('M', 'MEDIM'), ('L', 'LARGE'), ('XL', 'EXTRA LARGE'), ('XXL', 'EXTRA EXTRA LARGE')], max_length=3)),
                ('tribe', models.CharField(max_length=100)),
                ('homeChurch', models.CharField(max_length=255)),
                ('otherChurches', models.CharField(max_length=255)),
                ('sponsored', models.CharField(choices=[('Y', 'YES'), ('N', 'NO')], max_length=1)),
                ('health', models.TextField()),
                ('is_published', models.BooleanField(default=True)),
                ('createdAt', models.DateField(blank=True, null=True)),
                ('updatedAt', models.DateField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.User', to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationEnquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('enquiry_id', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('visit_date', models.DateTimeField()),
                ('message', models.TextField(max_length=1000)),
                ('is_resolved', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='account.User')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enquiry_requester', to='account.User')),
                ('target_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enquired_property', to='register.Registration')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
