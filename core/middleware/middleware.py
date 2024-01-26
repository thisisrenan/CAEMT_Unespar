from datetime import timedelta
from django.contrib.auth import logout
from django.utils import timezone
from core.models.users import UserActivity


class UpdateUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        inactive_users = UserActivity.objects.filter(last_activity__lt=timezone.now() - timedelta(minutes=1))
        inactive_users.delete()

        if request.user.is_authenticated:
            user_activity, created = UserActivity.objects.get_or_create(user=request.user)
            user_activity.update_activity()

        return response