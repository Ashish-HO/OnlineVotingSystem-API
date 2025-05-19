from rest_framework import serializers
from .models import Candidate, Post, Voter, ElectionSetting
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "title"]


class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = ["id", "name", "votes", "imagelink", "party", "post"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "is_superuser"]


class VoterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Voter
        fields = ["id", "voted", "user"]

    def create(self, validated_data):
        user = User.objects.create(
            **validated_data["user"]
        )  # create user when voter is created
        print(user)
        return Voter.objects.create(user=user)  # create voter when user is created


class ElectionSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionSetting
        fields = ["name", "start_date", "end_date"]


class BallotSerializer(serializers.Serializer):
    candidates = CandidateSerializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
