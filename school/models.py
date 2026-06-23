from django.db import models

# Create your models here.
class school(models.Model):
    choose_board=[('cbse','cbse'),('stAte board','state board'),('icse','icse')]
    school_name=models.CharField(max_length=50)
    owner=models.CharField(max_length=50)
    board=models.CharField(choices=choose_board, max_length=20)
    stablished_year=models.PositiveIntegerField()
    city=models.CharField(max_length=50)
    description=models.TextField()
    rating=models.DecimalField(max_digits=3,decimal_places=1,default=0.0)
    school_logo=models.ImageField(upload_to='img/school_logo/', null=True,blank=True)
    upload_date=models.DateField(auto_now=True)
    link=models.URLField()
    address=models.CharField()
    recognition_certificate=models.ImageField(upload_to='img/recognition_certificate/', null=True,blank=True)
    affiliation_number=models.PositiveIntegerField(default=1231)
    udise_code=models.PositiveIntegerField(default=123456789)


class teacher(models.Model):
    teacher_name=models.CharField(max_length=50)
    education=models.CharField(max_length=50)
    collage_name=models.CharField(max_length=80)
    teaching_exprience=models.PositiveIntegerField()
    core_subject=models.CharField(max_length=50)

class classes(models.Model):
    choose_class = [
    (1, "1st"),
    (2, "2nd"),
    (3, "3rd"),
    (4, "4th"),
    (5, "5th"),
    (6, "6th"),
    (7, "7th"),
    (8, "8th"),
    (9, "9th"),
    (10, "10th"),
    (11, "11th"),
    (12, "12th"),
                    ]
    classes=models.CharField(choices=choose_class)
    total_sets=models.PositiveIntegerField()
    avilable_sets=models.PositiveIntegerField()

class parent_info(models.Model):
    parent_name=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    phone_no=models.PositiveIntegerField()
    E_mail=models.EmailField()
    pasward=models.PositiveIntegerField(default=1234)
    resister=models.DateField(auto_now=True)
    cover_image=models.ImageField(upload_to='img/parent_covers/', null=True, blank=True)

class payment(models.Model):
    school_name = models.CharField(max_length=100)

    plan = models.CharField(max_length=50)

    amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    parent = models.ForeignKey(parent_info, on_delete=models.CASCADE, related_name='bookings')
    child_name = models.CharField(max_length=50)
    school_name = models.CharField(max_length=100)
    class_grade = models.CharField(max_length=20)
    seat_number = models.CharField(max_length=10)
    status = models.CharField(max_length=20, default="Confirmed")
    created_at = models.DateTimeField(auto_now_add=True)




 






