from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.utils.html import format_html
from .models import school, parent_info, Booking

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
         rating = request.POST.get('rating')
         if not rating or rating == '':
             rating = 0.0
         school_logo=request.FILES.get('school_logo')
         recognition_certificate=request.FILES.get('recognition_certificate')
         address=request.POST['address']
         link=request.POST.get('website_link', '')


         obj=school(school_name=school_name,board=board,stablished_year=stablished_year,owner=owner,city=city,description=description,
                    rating=rating,school_logo=school_logo,link=link,address=address,udise_code=udise_code,affiliation_number=affiliation_number,
                    recognition_certificate=recognition_certificate)
         obj.save()
         request.session['registered_school_id'] = obj.id
         return redirect('payment')
        
        
    except Exception as e:
        print(e)
    return render(request,'index.html')
def send(request):
   obj=school.objects.all()
   data={
      'school':obj
   }
   return render(request,'show_school.html',data)
def show_info(request, school_id=None):
   if school_id is None:
      first_school = school.objects.first()
      if first_school:
         return redirect('link', school_id=first_school.id)
      return redirect('show')

   try:
      s = school.objects.get(id=school_id)
   except school.DoesNotExist:
      return redirect('show')
   
   data={
      's': s,
      'school': [s]
   }
   return render(request,'info.html',data)

def sigin(request):
   return render(request,'singin.html')

def seat(request):
    if not request.user.is_authenticated:
        return redirect("parent_login")

    if request.method == 'POST':
        # Retrieve the logged-in parent
        parent_obj = parent_info.objects.filter(E_mail=request.user.email).first()
        if not parent_obj:
            parent_obj = parent_info.objects.filter(parent_name=request.user.username).first()
        if not parent_obj:
            parent_obj = parent_info.objects.create(
                parent_name=request.user.username,
                city="Mumbai, Maharashtra",
                phone_no=9876543210,
                E_mail=request.user.email or "parent@email.com",
                pasward=1234
            )

        # Get form details
        child_name = request.POST.get("child_name")
        selected_class = request.POST.get("selected_class")
        seat_number = request.POST.get("seat_number")
        school_name = request.POST.get("school_name", "Sunrise International School")
        parent_name = request.POST.get("parent_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        # Update parent details if changed
        if parent_name and parent_name != parent_obj.parent_name:
            parent_obj.parent_name = parent_name
        if phone:
            try:
                phone_int = int(phone.replace(' ', '').replace('+', '').replace('-', ''))
                parent_obj.phone_no = phone_int
            except:
                pass
        if email and email != parent_obj.E_mail:
            parent_obj.E_mail = email
            request.user.email = email
            request.user.save()
        parent_obj.save()

        # Create the Booking record
        booking = Booking.objects.create(
            parent=parent_obj,
            child_name=child_name,
            school_name=school_name,
            class_grade=selected_class,
            seat_number=seat_number,
            status="Confirmed"
        )

        # Return JSON success or redirect
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'booking_id': booking.id,
                'child_name': booking.child_name,
                'class_grade': booking.class_grade,
                'seat_number': booking.seat_number,
                'school_name': booking.school_name
            })

        return redirect("parent")

    # GET request: render seat selection
    taken_bookings = Booking.objects.all()
    taken_seats_dict = {}
    for b in taken_bookings:
        if b.class_grade not in taken_seats_dict:
            taken_seats_dict[b.class_grade] = []
        taken_seats_dict[b.class_grade].append(b.seat_number)

    schools_list = school.objects.all()
    import json
    data = {
        "taken_seats_json": json.dumps(taken_seats_dict),
        "schools": schools_list
    }
    return render(request, 'class_seat.html', data)

def parent(request):
    if not request.user.is_authenticated:
        return redirect("parent_login")

    # Get or create a parent_info profile for the logged in user
    obj = parent_info.objects.filter(E_mail=request.user.email).first()
    if not obj:
        obj = parent_info.objects.filter(parent_name=request.user.username).first()
    
    if not obj:
        obj = parent_info.objects.create(
            parent_name=request.user.username,
            city="Mumbai, Maharashtra",
            phone_no=9876543210,
            E_mail=request.user.email or "parent@email.com",
            pasward=1234
        )

    # Fetch parent's actual bookings
    bookings = Booking.objects.filter(parent=obj).order_by('-created_at')

    # Calculate stats dynamically
    seats_booked = bookings.count()
    children_enrolled = bookings.values('child_name').distinct().count()
    school_selected = bookings.values('school_name').distinct().count()

    # Generate dynamic recent activity
    activities = []
    for b in bookings[:4]:
        time_str = b.created_at.strftime("%I:%M %p, %b %d")
        activities.append({
            "title": format_html("Seat booked for <strong>{}</strong> — Class {}, Seat {}", b.child_name, b.class_grade, b.seat_number),
            "time": f"{time_str}",
            "icon": "act-seat",
            "icon_class": "bi-ticket-perforated-fill"
        })

    if not activities:
        time_str = obj.resister.strftime("%b %d, %Y") if obj.resister else "Recently"
        activities.append({
            "title": "Account created and <strong>profile verified</strong>",
            "time": f"{time_str}",
            "icon": "act-notif",
            "icon_class": "bi-person-plus-fill"
        })

    data = {
        "parent": [obj],
        "bookings": bookings,
        "seats_booked": seats_booked,
        "children_enrolled": children_enrolled,
        "school_selected": school_selected,
        "activities": activities
    }
    return render(request, 'parent.html', data)

def parent_edit(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Unauthenticated'}, status=401)

    if request.method == 'POST':
        obj = parent_info.objects.filter(E_mail=request.user.email).first()
        if not obj:
            obj = parent_info.objects.filter(parent_name=request.user.username).first()

        if not obj:
            return JsonResponse({'status': 'error', 'message': 'Profile not found'}, status=404)

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')

        if name:
            obj.parent_name = name
        if email:
            obj.E_mail = email
            request.user.email = email
        if phone:
            try:
                phone_int = int(phone.replace(' ', '').replace('+', '').replace('-', ''))
                obj.phone_no = phone_int
            except:
                pass
        if city:
            obj.city = city

        obj.save()
        request.user.save()

        return JsonResponse({
            'status': 'success',
            'name': obj.parent_name,
            'email': obj.E_mail,
            'phone': obj.phone_no,
            'city': obj.city
        })

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def change_cover(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Unauthenticated'}, status=401)

    if request.method == 'POST' and request.FILES.get('cover_image'):
        obj = parent_info.objects.filter(E_mail=request.user.email).first()
        if not obj:
            obj = parent_info.objects.filter(parent_name=request.user.username).first()

        if not obj:
            return JsonResponse({'status': 'error', 'message': 'Profile not found'}, status=404)

        obj.cover_image = request.FILES['cover_image']
        obj.save()

        return JsonResponse({
            'status': 'success',
            'cover_url': obj.cover_image.url
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def parent_login(request):
    if request.user.is_authenticated:
        return redirect("show")

    if request.method == "POST":
        # Register Form
        if "username" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            city = request.POST.get("city", "Mumbai")
            phone = request.POST.get("phone", "9876543210")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("parent_login")

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect("parent_login")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            try:
                phone_int = int(phone.replace(' ', '').replace('+', '').replace('-', ''))
            except:
                phone_int = 9876543210

            parent_info.objects.create(
                parent_name=username,
                city=city,
                phone_no=phone_int,
                E_mail=email,
                pasward=1234
            )

            login(request, user)
            messages.success(request, "Account Created Successfully")
            return redirect("parent")

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
                    return redirect("parent")
                else:
                    messages.error(request, "Invalid Credentials")

            except User.DoesNotExist:
                messages.error(request, "Invalid Credentials")

    return render(request, "parent_login.html")


def user_logout(request):
    logout(request)
    return redirect("parent_login")

def payment(request):
    schools_list = school.objects.all()
    
    # Try to fetch the school registered in this session
    school_id = request.session.get('registered_school_id')
    if school_id:
        target_school = school.objects.filter(id=school_id).first()
    else:
        target_school = school.objects.last()
        
    data = {
        'school': [target_school] if target_school else [],
        'schools': schools_list
    }
    return render(request, 'payment.html', data)