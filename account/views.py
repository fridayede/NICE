
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def login_user(request):
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email =request.POST.get("email")
        user =  authenticate(request, username=username, password=password,email=email)
        if user is not None:
                login(request,user)
                return redirect('product:home')
        messages.error(request, "Invalid credentials. Please try again.")
        print(username)
        print(email)
        print(password)    
    return render(request,'account/login.html')





def register_user(request):
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     email = request.POST.get('email')
    #     password1 = request.POST.get('password1')
    #     password2 = request.POST.get('password2')

    #     if password1 != password2:
    #         messages.error(request, "Passwords do not match.")
    #         return redirect('register')

    #     if User.objects.filter(username=username).exists():
    #         messages.error(request, "Username already exists.")
    #         return redirect('register')

    #     if User.objects.filter(email=email).exists():
    #         messages.error(request, "Email already exists.")
    #         return redirect('register')

    #     # Create the user
    #     user = User.objects.create_user(username=username, password=password2, email=email)
    #     user.save()
    #     messages.success(request, "Account created successfully.")
    #     return redirect('login')

    # return render(request, 'account/register.html')
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        confirmPassword2 = request.POST.get("confirmPassword2")

        if password1 != confirmPassword2:
            messages.error(request, "Passwords do not match.")
            return redirect('account:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('account:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('account:register')

        user = User.objects.create_user(username=username, password=confirmPassword2, email=email)
        login(request, user)
        return redirect('product:home')
    return render(request, 'account/register.html')



def logout_user(request):
    if request.method =="POST":
        logout(request)
    return redirect('home')
    pass 