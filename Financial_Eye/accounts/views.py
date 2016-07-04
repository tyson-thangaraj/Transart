from django.shortcuts import render


from django.http import HttpResponse

#from django.shortcuts import render, get_object_or_404
from django.utils.timezone import utc
# from datetime import timedelta, datetime
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from accounts.models import Users
from accounts.serializers import UserSerializer
from rest_framework import generics
from rest_framework import filters
import django_filters

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
    register a account with username and password parameters
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
    log in a account with username and password parameters
    """
    username = request.query_params.get('username', None)
    password = request.query_params.get('password', None)

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
    # flag = request.query_params.get('flag', None)
    # print('++++++++++++++++++++++++++++++++++++++++')
    # print(flag)

    # if flag == '1':
    #     print("----------------------------------------------")
    #     user = Users(Username=username, Password=password)
    #     print(user)
    #     serializer = UserSerializer(user)
    #     print(serializer.data)
    #     serializer = UserSerializer(data=serializer.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     print(serializer.errors)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # users = Users.objects.all()
    # serializer = UserSerializer(users, many=True)
    # return Response(serializer.data)
    
# class UserList(generics.ListCreateAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         """
#         Optionally restricts the returned purchases to a given user,
#         by filtering against a `username` query parameter in the URL.
#         """
#         queryset = Users.objects.all()
#         username = self.request.query_params.get('username', None)
#         password = self.request.query_params.get('password', None)
#         flag = self.request.query_params.get('flag', None)
#         # print(flag)
#         # print(type(flag))
#         if flag == "1":
#             newuser = Users(Username=username, Password=password)
#             newuser.save()
#             return queryset
#         elif flag == "2":
#             if username and password is not None:
#                 queryset = queryset.filter(Username=username, Password=password)
#             return queryset


# from django.contrib.auth.models import User
# from rest_framework import authentication
# from rest_framework import exceptions

# class ExampleAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         username = request.META.get('username')
#         password = request.META.get('password')
#         if not username:
#             return None
#         try:
#             user = Users.objects.get(Username=username)
#             if password != user.Password:
#                 raise exceptions.AuthenticationFailed('wrong password')
#         except User.DoesNotExist:
#             raise exceptions.AuthenticationFailed('No such user')
        
#         return (user, None)

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# class ExampleView(APIView):
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, format=None):
#         content = {
#             'user': unicode(request.user),  # `django.contrib.auth.User` instance.
#             'auth': unicode(request.auth),  # None
#         }
#         return Response(content)


# from django.contrib.auth.models import User
# from rest_framework import authentication
# from rest_framework import exceptions
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import authentication, permissions



    #return Response(d1, status=status.HTTP_400_BAD_REQUEST)   
    # try:
    #     user = Users.objects.get(Username=username)
    #     if password != user.Password:
    #         raise exceptions.AuthenticationFailed('wrong password')
    # except User.DoesNotExist:
    #     raise exceptions.AuthenticationFailed('No such user')
    # return (user, None)

    # content = {
    #     'user': unicode(request.user),  # `django.contrib.auth.User` instance.
    #     'auth': unicode(request.auth),  # None
    # }
    # return Response(content)

        







# class CreateUser(generics.ListCreateAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UserSerializer

#     print("hello")


#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         print('|||||||||||||||||||||||||||||||||||||||')
#         print(request.query_params)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def create(self, request, username, password):
    #     username = self.request.query_params.get('username', None)
    #     password = self.request.query_params.get('password', None)
    #     print("hello00000000000000000000")
    #     user = Users(Username=username, Password=password)
    #     serializer = UserSerializer(user)
    #     if serializer.is_valid():
    #         serializer.save()
    #         print("##################################################")
    #         return Response(serializer.data)
    #     else:
    #         print('++++++++++++++++++++++++++++++++++++++++++++++++++==')
    #         print(serializer.errors)
    #         return render(request, 'userlist')


# class CreateUser(generics.ListCreateAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UserSerializer
#     def get_queryset(self):
#         queryset = Users.objects.all()
#         print("hello")
#         username = self.request.query_params.get('username', None)
#         password = self.request.query_params.get('password', None)
#         newuser = Users(Username=username, Password=password)
#         if newuser.save():
#             print("created success!")
#             queryset = queryset.filter(Username=username, Password=password)
#             return queryset

        # if username and password is not None:
        #     queryset = queryset.filter(Username=username, Password=password)
        # return queryset






# def createUserObject(username, password, email,firstname, lastname, address, telephone, datejoined):
#     print([username, password, email,firstname, lastname, address, telephone, datejoined])
#     try:
#         user = Users(Username=username,
#                         Password=password,
#                         Email=email,
#                         FirstName = firstname,
#                         LastName = lastname,
#                         Address = address,
#                         Telephone = telephone,
#                         DateJoined = datejoined)

#     except Exception as err:
#                 print("In createArticleObject():"+ err)
#     return user