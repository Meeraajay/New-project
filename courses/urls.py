from django.urls import path
from . import views

urlpatterns = [

    path(
        'computer-science/',
        views.computer_science,
        name='computer_science'
    ),

    path(
        'bio-maths/',
        views.bio_maths,
        name='bio_maths'
    ),

    path(
        'commerce/',
        views.commerce,
        name='commerce'
    ),

    path(
        'humanities/',
        views.humanities,
        name='humanities'
    ),

]