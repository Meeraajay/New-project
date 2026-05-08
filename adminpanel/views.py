from django.shortcuts import render
from calculation.models import AdmissionResult

def dashboard(request):

    courses = AdmissionResult.objects.values_list('course', flat=True).distinct()

    data = {}

    for course in courses:
        data[course] = AdmissionResult.objects.filter(course=course).order_by('rank')

    return render(request, 'adminpanel/dashboard.html', {
        'data': data
    })