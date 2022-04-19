from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (PasswordChangeForm, PasswordResetForm,
                                       SetPasswordForm)
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above
from django.views.decorators.vary import vary_on_cookie
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.manage_user.controller.serializers.profile_management.serializers import (
    UpdateUserSerializer, UserSerializer, WishListSerializer)
from apps.manage_user.controller.serializers.user_search_and_categories.serializers import \
    ProfileAvailabilitySerializer
from apps.manage_user.controller.serializers.utils.decorators import \
    time_calculator
from apps.profiles.models import Profile
from apps.profiles.producer import RabbitMq
from apps.profiles.serializers import ProfileSerializer

User = get_user_model()


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile


# API to fetch all registered users
class AllUsersAPIView(ListAPIView):
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]

    serializer_class = UserSerializer
    queryset = User.objects.filter(available=True)

    @time_calculator
    def time(self):
        return 0

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        all_emails = User.objects.filter(is_active=True).values_list('email', flat=True)
        date_created_list = User.objects.filter(is_active=True).values_list('created', flat=True)

        response = {
            "users": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    #     return JsonResponse({'users': list(all_emails),
    #                          'date_created': list(date_created_list)})

# API to fetch User details by ID
class UserDetailView(APIView):
    permission_classes = permission_classes = (AllowAny,)

    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(
                profile, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return  Response({"detail": _("User is not found!")},
            status=status.HTTP_404_NOT_FOUND
        )

# API to Post and Read Favorite Players
class WishListView(ListAPIView):
    serializer_class = WishListSerializer
    queryset = User.objects.filter(available=True)
    #permission_classes = (permissions.IsAuthenticated|permissions.IsAdminUser, )
    permission_classes = (AllowAny, )

    @time_calculator
    def time(self):
        return 0

    def get_queryset(self):
        self_user = self.request.user
        favorites = self_user.favorite_players.all()
        return favorites

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response(serializer.data)


class AddWishList(APIView):
    serializer_class = WishListSerializer
    queryset = User.objects.filter(available=True)
    #permission_classes = (permissions.IsAuthenticated|permissions.IsAdminUser, )
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return User.objects.filter(available=True)

    def post(self, request, *args, **kwargs):
        data = request.data
        user_item = self.request.user
        print(data)

        for fav in self.get_queryset():
            fav_obj = User.objects.get(pk=fav.pk)
            user_item.favorite_players.add(fav_obj)

        return Response(
            {"detail": _("The user has been added to the favorites")},
            status=status.HTTP_200_OK
        )

# API to Update Profile
class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UpdateUserSerializer

# API to Update a User's availability by User-ID
class UpdateAvailability(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ProfileAvailabilitySerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        data_to_change = {'available': request.data.get("available")}

        serializer = self.serializer_class(request.user, data=data_to_change, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)

        return Response(serializer.data)

# API to Delete a User. Only admin is authorized.
class DestroyUserAPIView(DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    # queryset = User.objects.all()

    def get_object(self, username):
        try:
            return get_object_or_404(User, username=username)
        except User.DoesNotExist:
            raise Http404

    def destroy(self, request, username):
        instance = self.get_object(username)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!s", instance)
        instance.delete()
        print("username ", username)
        publish_data = {
            "username": str(username)
        }
        p = RabbitMq()
        RabbitMq.publish(p, 'user_deleted', publish_data)

        return Response({"detail": "User deleted",
                         "user": str(instance)})


# API to Delete My own Profile.
class DeleteAccount(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user=self.request.user
        user.delete()

        return Response({"result": "user deleted"})

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context

# API to reset password
class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "registration/password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "registration/password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_exempt)#csrf_protect
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)

INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"

# API to show that password reset is done
class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = "registration/password_reset_done.html"
    # template_name = "localhost:8080/reset/done/"
    title = _("Password reset sent")

# API to confirm the password reset
class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = "set-password"
    success_url = reverse_lazy("password_reset_complete")
    template_name = "registration/password_reset_confirm.html"
    title = _("Enter new password")
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context["validlink"] = True
        else:
            context.update(
                {
                    "form": None,
                    "title": _("Password reset unsuccessful"),
                    "validlink": False,
                }
            )
        return context

# API to show the password reset completion
class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = "registration/password_reset_complete.html"
    title = _("Password reset complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context

class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "registration/password_change_form.html"
    title = _("Password change")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = "registration/password_change_done.html"
    title = _("Password change successful")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



