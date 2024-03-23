from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Job
from job_scraper_app.models import Job, User, AttemptedJobs, Portfolio

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'job_title', 'job_company_name', 'job_location', 'job_id', 'job_level']


# class JobSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Job
#         fields = ['id', 'job_title', 'job_company_name', 'job_location', 'job_id', 'job_level']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_phone_code','password',
                  'user_phone_number', 'user_interest', 'user_avatar', 'user_permissions', 'groups']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


class AttemptedJobsSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField(required=False)
    user = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), required=False)
    job_object = JobSerializer(source='attempted_job', read_only=True)
    user_object = UserSerializer(source='user', read_only=True)

    class Meta:
        model = AttemptedJobs
        fields = ['id', 'user', 'job_id', 'job_object', 'user_object', 'attempted_job_status', 'date_attempted']

    def create(self, validated_data):
        job_id = validated_data.pop('job_id')
        user_id = self.context['request'].user.id

        try:
            user = User.objects.get(id=user_id)
            job = Job.objects.get(id=job_id)  # Retrieve the Job object based on job_id
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        except Job.DoesNotExist:
            raise serializers.ValidationError("Job does not exist.")

        if user.is_authenticated:
            validated_data.pop('user', None)  # remove the 'user' key from the validated_data dictionary
            attempted_job = AttemptedJobs.objects.create(
                user=user,
                attempted_job=job,  # Assign the retrieved Job object
                **validated_data
            )
            return attempted_job
        else:
            raise serializers.ValidationError("User must be authenticated to perform this action.")


class PortfolioSerializer(serializers.ModelSerializer):
    jobs = AttemptedJobsSerializer(many=True, read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', write_only=True, queryset=User.objects.all())

    class Meta:
        model = Portfolio
        fields = ['user_id', 'jobs']

    def update_portfolio(self, user_id, job_instance):
        try:
            portfolio_instance = Portfolio.objects.get(user_id=user_id)
        except Portfolio.DoesNotExist:
            # If Portfolio instance doesn't exist, create a new one
            portfolio_instance = Portfolio.objects.create(user_id=user_id)
        portfolio_instance.jobs.add(job_instance)
        portfolio_instance.save()

    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        job_instance = super().create(validated_data)
        self.update_portfolio(user_id, job_instance)
        return job_instance

    def update(self, instance, validated_data):
        user_id = validated_data.pop('user_id', None)
        job_instance = super().update(instance, validated_data)
        self.update_portfolio(user_id, job_instance)
        return job_instance
