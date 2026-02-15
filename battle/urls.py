from django.urls import path
from .views import home, create_room, editor, run_code

urlpatterns = [
    path("", home),
    path("create/", create_room),
    path("room/<str:room>/", editor),
    path("run/", run_code),
]
