from django.contrib import admin
from .models import school
# Register your models here.
@admin.register(school)
class school_info(admin.ModelAdmin):
    list_display=('id','school_name','board','stablished_year','owner','city','description',
                  'rating','school_logo','upload_date','address','link')
    