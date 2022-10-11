from django.urls import path
from history.views import *

urlpatterns = [
    path("test", detect, name="detect"),
    path("events/", events, name="events"),
    path("events/<event_pk>/", event_detail, name="event_detail"),
    path("event/add-laugh-score/", add_laugh_score, name="add_laugh_score")
]