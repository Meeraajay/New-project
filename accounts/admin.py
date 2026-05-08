from django.contrib import admin
from .models import Student
from .models import CBSEAcademicDetails
from .models import KeralaAcademicDetails
from .models import CoursePreference
from .models import Extracurricular

admin.site.register(Student)
admin.site.register(CBSEAcademicDetails)
admin.site.register(KeralaAcademicDetails)
admin.site.register(CoursePreference)
admin.site.register(Extracurricular)