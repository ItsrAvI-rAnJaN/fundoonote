from user.models import UserLogs
from django.utils.deprecation import MiddlewareMixin


class CountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_logs = UserLogs.objects.filter(method=request.method, url=request.path)
        if user_logs.exists():
            log = user_logs.first()
            log.count += 1
            log.save()
        else:
            UserLogs.objects.create(method=request.method, url=request.path)
        return self.get_response(request)




