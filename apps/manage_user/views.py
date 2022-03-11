from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
# from rest_framework.parsers import JSONParser
#
# class CustomUserCreate(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, format='json'):
#         serializer = CustomUserSerializer(data=request.data)
#         email = request.POST['email']
#         print("############3", User.objects.filter(email=email).exists())
#
#         if serializer.is_valid():
#             email = serializer.validated_data.get('email')
#
#
#             if User.objects.filter(email=email).exists():
#                 print("#!!!!!!!!!!!!!!!!!!!!", serializer.errors)
#                 messages.add_message(request, messages.ERROR,
#                                      'Email is taken, choose another one')
#
#                 return Response({'message': 'Email is duplicate'}, status=status.HTTP_226_IM_USED)
#
#             user = serializer.save()
#             if user:
#                 json = serializer.data
#                 return Response(json, status=status.HTTP_201_CREATED)
#             # if serializer.validate_email(email):
#             #     return Response(serializer.errors, status=status.HTTP_226_IM_USED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # class UserProfileListCreateAPIView(generics.ListCreateAPIView):
# #     queryset = UserProfile.objects.all()
# #     serializer_class = CustomUserProfileSerializer
# #
# #     def post(self, request, format=None):
# #         serializer = CustomUserSerializer(data=request.data)
# #
# #         email = request.POST['email']
# #         print("############3", UserProfile.objects.filter(email=email).exists())
# #
# #         if serializer.is_valid():
# #             email = serializer.validated_data.get('email', False)
# #
# #             if UserProfile.objects.filter(email=email).exists():
# #                 print("#!!!!!!!!!!!!!!!!!!!!", serializer.errors)
# #                 messages.add_message(request, messages.ERROR,
# #                                      'Email is taken, choose another one')
# #
# #                 return Response({'message': 'Email is duplicate'}, status=status.HTTP_226_IM_USED)
# #
# #             user = serializer.save()
# #             if user:
# #                 json = serializer.data
# #                 return Response(json, status=status.HTTP_201_CREATED)
# #             # if serializer.validate_email(email):
# #             #     return Response(serializer.errors, status=status.HTTP_226_IM_USED)
# #
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# # class UserProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
# #     # permission_classes = [IsAdminUser]
# #     queryset = UserProfile.objects.all()
# #     serializer_class = CustomUserProfileSerializer
# #     # lookup_field = 'email'
# #     # def delete(self, request, *args, **kwargs):
# #     #     try:
# #     #         email_id = request.data.get('email_id', None)
# #     #         response = super().delete(request, *args, **kwargs)
# #     #
# #     #         if response.status_code == 204:
# #     #             from django.core.cache import cache
# #     #             cache.delete("{}".format(email_id))
# #     #             return response
# #     #     except:
# #     #         return Response({
# #     #             "Message": "Failed "
#     #         })
#
class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# def user_login(request):
#     email = request.POST['email']
#     print("I AM  HERERERERERE#########################################")
#     user_data = User.objects.filter(email=email).first()
#     print(user_data)
#     # models.Tennisplayer.objects.get(email=email, password=password)
#     if user_data:
#         # this will return this bool as a response in the browser, which we can utilize to save the userLoginStatus
#         # TODO: Check if user is admin or not
#         # print(user_data.is_staff), isAdmin -> to check if user is Admin
#         return JsonResponse({'bool': True,
#                              'isAdmin': user_data.is_staff})
#     else:
#         # user can is not logged in
#         return JsonResponse({'bool': False})
#
# ## getting back only emails and date_created from DB
# ## JsonResponse is going to serialize them automatically -- no need for a serializer.
# @api_view(['GET'])
# # @permission_classes([IsAdminUser])
# def get_users(request):
#     # toDO: fetch users only if you're admin
#     # get the user associated with that token, des
#     # user = request.email
#     # notes = user.note_set.all()
#     permission_classes = [IsAdminUser]
#     all_emails = User.objects.filter(is_active=True).values_list('email', flat=True)
#     date_created_list = User.objects.filter(is_active=True).values_list('date_created', flat=True)
#     return JsonResponse({'users': list(all_emails),
#                          'date_created': list(date_created_list)})
#
# # localhost:8002/api/user/delete-user/1
# # class UserViewSet(viewsets.ModelViewSet):
# #     queryset = NewUser.objects.all()
# #     serializer_class = CustomUserProfileSerializer
# #
# #     @action(detail=True, methods=['delete'])
# #     def delete_user_by_id(self, request, pk=None):
# #         # email = request.DELETE['email']
# #         permission_classes = [IsAdminUser]
# #         # get the right user
# #         # use pk to get the user with the right id
# #         email_by_id = NewUser.objects.get(pk=pk)
# #         # user_email = NewUser.objects.filter(email=email).first()
# #         email_by_id.delete()
# #         all_emails = NewUser.objects.filter(is_active=True).values_list('email', flat=True)
# #         date_created_list = NewUser.objects.filter(is_active=True).values_list('date_created', flat=True)
# #
# #         return JsonResponse({'message': 'User has been deleted successfully!',
# #                              'users': list(all_emails),
# #                              'date_created': list(date_created_list)})
# #
