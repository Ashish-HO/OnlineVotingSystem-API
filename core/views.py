from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
)

from django.contrib.auth.models import User

from .models import Candidate, Post, Voter
from .serializers import (
    CandidateSerializer,
    UserSerializer,
    PostSerializer,
    VoterSerializer,
    ElectionSettingSerializer,
    BallotSerializer,
    LoginSerializer,
)


class CandidateView(ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateDetail(RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.select_related("post").all()
    serializer_class = CandidateSerializer


class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class VoterView(ListCreateAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer


class BallotView(APIView):

    def get(self, request):
        queryset = Candidate.objects.all()
        print(queryset)
        serializer = CandidateSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CandidateSerializer(data=request.data, many=True)
        serializer.is_valid()

        votes = serializer.validated_data
        for vote in votes:
            name = get_object_or_404(Candidate, name=vote["name"])
            post = get_object_or_404(Post, title=vote["post"])
            candidate = Candidate.objects.get(name=name)
            candidate.votes += 1
            candidate.save()

        # # make sure the user is not anonymous
        # voter = Voter.objects.get(user=request.user)
        # voter.voted = True
        # voter.save()

        return Response({"message": " Your Vote has been recorded"})


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)

        if user:
            return Response({"message": "Login Successful"}, status=HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=HTTP_401_UNAUTHORIZED
            )
