from django.shortcuts import render


from django.http import HttpResponse

#from django.shortcuts import render, get_object_or_404
from django.utils.timezone import utc
# from datetime import timedelta, datetime
from rest_framework.decorators import api_view
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
    print("hellozzzzzzzzzzzzz")
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Users.objects.all()
        username = self.request.query_params.get('username', None)
        password = self.request.query_params.get('password', None)
        flag = self.request.query_params.get('flag', None)
        # print(flag)
        # print(type(flag))
        if flag == "1":
            newuser = Users(Username=username, Password=password)
            newuser.save()
            return queryset
        elif flag == "2":
            print("helloqqqqqqqqqqqqqqqqqqqq")
            if username and password is not None:
                queryset = queryset.filter(Username=username, Password=password)
            return queryset



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



@api_view(['GET', 'POST'])
def user_list(request, format=None):
    """
    List all snippets, or create a new snippet.
    """

    username = request.query_params.get('username', None)
    password = request.query_params.get('password', None)
    flag = request.query_params.get('flag', None)
    print('++++++++++++++++++++++++++++++++++++++++')
    print(flag)

    if flag == '1':
        print("----------------------------------------------")
        user = Users(Username=username, Password=password)
        print(user)
        serializer = UserSerializer(user)
        print(serializer.data)
        serializer = UserSerializer(data=serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    users = Users.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
    


class CreateUser(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    print("hello")


    def create(self, request, *args, **kwargs):
        print(request.data)
        print('|||||||||||||||||||||||||||||||||||||||')
        print(request.query_params)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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




class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

def createUserObject(username, password, email,firstname, lastname, address, telephone, datejoined):
    print([username, password, email,firstname, lastname, address, telephone, datejoined])
    try:
        user = Users(Username=username,
                        Password=password,
                        Email=email,
                        FirstName = firstname,
                        LastName = lastname,
                        Address = address,
                        Telephone = telephone,
                        DateJoined = datejoined)

    except Exception as err:
                print("In createArticleObject():"+ err)
    return user