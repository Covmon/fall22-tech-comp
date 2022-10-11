from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
import json

from history.models import HistoryEvent
from history.serializers import EventSerializer

def detect(request):
  return render(request, "read/smile_detect.html")

def events(request):
  filter_qs = request.GET.get("filter", "")
  events = HistoryEvent.objects.filter(active=True).filter(
  Q(title__icontains=filter_qs)|
  Q(writer__first_name__icontains=filter_qs)|
  Q(writer__last_name__icontains=filter_qs)|
  Q(writer__display_name__icontains=filter_qs)|
  Q(custom_display_name__icontains=filter_qs)).order_by("?").distinct()
  paginator = Paginator(events, 20)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  serializer = EventSerializer(page_obj, context={'request': request}, many=True)

  context = {
      "events": serializer.data,
      "filter": filter_qs
  }
  get_copy = request.GET.copy()
  if get_copy.get("page"):
      get_copy.pop("page")
  context["get_copy"] = get_copy

  return JsonResponse(context)
  # return render(request, "history/events.html", context)

def event_detail(request, event_pk):
  event = get_object_or_404(HistoryEvent, pk=event_pk)
  # view = View.objects.get_or_create(event = event, cookie = request.COOKIES.get("_ga", None))
  serializer = EventSerializer(event, context={'request': request})

  context = {
      "event": serializer.data,
      "PRODUCT_API_URL": settings.PRODUCT_API_URL
  }

  return JsonResponse(context)
  # return render(request, "history/event.html", context)
    

def add_laugh_score(request):
  if request.method=="POST":
    data = json.loads(request.body)
    event_pk = data.get("event_pk")
    event = HistoryEvent.objects.get(pk=event_pk)
    event.laugh_score+=1
    event.save()
    return JsonResponse({"score": event.laugh_score})
