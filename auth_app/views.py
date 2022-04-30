from django.shortcuts import redirect, render
from custom_exception import CustomException
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def login_api(request):
    """ This function is responsible for check authorization of entered username and password and Login"""
    try:
        if request.method == "POST":
     
            user = authenticate(
                request, username=request.POST.get("username"), password=request.POST.get("password")
            )
            if user:
                login(request, user)
                return redirect('/')
            else:
                raise CustomException(
                    description="Invalid username/password", status_code=412
                )

        else:
            return render(request, 'login.html', {})
    except CustomException as e:
        return render(request, 'login.html',{"login_error_msg": e.description}, status=e.status_code)
    except Exception as e:
        return render(request, 'login.html',{"login_error_msg": "Unable to login"}, status=500)

@login_required
def logout_api(request):
    """ This function is responsible for Logout"""
    logout(request)
    return render(request, 'login.html', {})


