__author__ = 'Jiandong Wang'

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from accounts.models import Users
from accounts.serializers import UserSerializer
from rest_framework import generics


# Create your views here.

class UserList(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

@api_view(['GET', 'POST'])
def user_register(request, format=None):
    """
    register an account with username and password parameters
    """

    username = request.query_params.get('username', None)
    password = request.query_params.get('password', None)

    user = Users(Username=username, Password=password)
    serializer = UserSerializer(user)
    serializer = UserSerializer(data=serializer.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def user_login(request):
    """
    log in an account with username and password parameters
    """
    username = request.query_params.get('username', None)
    password = request.query_params.get('password', None)

    # define customed response messages
    d1 = {"Info":["No such user"]}
    d2 = {"Info":["Wrong password"]}
    d3 = {"Info":["Sucessfully login"]}
    if not username:
        return Response(d1)
    try:
        user = Users.objects.get(Username=username)
        if password == user.Password:
            return Response(d3)
        else:
            return Response(d2)
                
    except Users.DoesNotExist:
        return Response(d1)

    
