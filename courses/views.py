from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def computer_science(request):
    return render(request, 'computer_science.html')


@login_required
def bio_maths(request):
    return render(request, 'bio_maths.html')


@login_required
def commerce(request):
    return render(request, 'commerce.html')


@login_required
def humanities(request):
    return render(request, 'humanities.html')