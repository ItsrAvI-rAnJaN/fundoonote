from django.urls import path,include
from . import views

urlpatterns = [
    path('registration/', views.registration , name='registration'),
    path('loginapi/', views.loginapi , name='loginapi'),
]
def registration(request):
    """
    method : To registerd user
    """
    try:
        data= json.loads(request.body)
        if request.method == 'POST':
            u = User.objects.create(username=data.get('username'),password=data.get('password'))
            return JsonResponse({"message" : "User registered sucessfully"})
        else:
            return JsonResponse({"message":"some"})

    except Exception as err:
            print(err)
            logging.exception(err)
            return JsonResponse({"message": str(err)})
