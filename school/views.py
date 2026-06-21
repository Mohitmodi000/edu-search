from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import school,parent_info

# Create your views here.
def school_info(request):
    try:
        if request.method=='POST':
         school_name=request.POST['school_name']
         board=request.POST['board']
         stablished_year=request.POST['established_year']
         affiliation_number=request.POST['affiliation_number']
         udise_code=request.POST['udise_code']
         owner=request.POST['owner']
         city=request.POST['city']
         description=request.POST['description']
         rating=request.POST['rating']   
         school_logo=request.FILES.get('school_logo')
         recognition_certificate=request.FILES.get('recognition_certificate')
         address=request.POST['address']
         link=request.POST['website_link']


         obj=school(school_name=school_name,board=board,stablished_year=stablished_year,owner=owner,city=city,description=description,
                    rating=rating,school_logo=school_logo,link=link,address=address,udise_code=udise_code,affiliation_number=affiliation_number,
                    recognition_certificate=recognition_certificate)
         obj.save()
         return redirect('show')
        
        
    except Exception as e:
        print(e)
    return render(request,'index.html')
def send(request):
   obj=school.objects.all()
   data={
      'school':obj
   }
   return render(request,'show_school.html',data)
def show_info(request):
   obj=school.objects.all()
   data={
      'school':obj
   }
   return render(request,'info.html',data)
def sigin(request):
   return render(request,'singin.html')

def seat(request):

      return render(request,'class_seat.html')
   
def parent(request):
   obj=parent_info.objects.all()
   data={"parent":obj}
   return render(request,'parent.html',data)

def parent_login(request):
    if request.method == "POST":

        # Register Form
        if "username" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("parentlogin")

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(request, "Account Created Successfully")
            return redirect("parentlogin")

        # Login Form
        else:
            email = request.POST.get("email")
            password = request.POST.get("password")

            try:
                user_obj = User.objects.get(email=email)

                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )

                if user is not None:
                    login(request, user)
                    return redirect("home")

            except User.DoesNotExist:
                messages.error(request, "Invalid Credentials")

    return render(request, "parent_login.html")


def home(request):
    if not request.user.is_authenticated:
        return redirect("parentlogin")

    return render(request, "home.html")


def user_logout(request):
    logout(request)
    return redirect("parentlogin")
def payment(request):

   return render(request,'payment.html')