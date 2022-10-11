from rest_framework import serializers
from history.models import HistoryEvent, HistoryImage
from read.serializers import UserSerializer
from account.models import User

class HistoryImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = HistoryImage
    fields = ('pk', 'image', 'title', 'order', 'custom_display_name', 'original_work', 'created_at')
    
  # def to_representation(self, instance):
  #   data = super().to_representation(instance)
  #   print("in history image serializer!")
  #   data['artist'] = UserSerializer(User.objects.get(pk=data['artist'])).data

  #   return data

class EventSerializer(serializers.ModelSerializer):
  class Meta:
    model = HistoryEvent
    fields = ('pk', 'title', 'cover_image', 'date', 'writer', 'content', 'created_at', 'active', 'custom_display_name', 'featured', 'laugh_score')

  def to_representation(self, instance):
    data = super().to_representation(instance)

    data['cover_image'] = HistoryImageSerializer(HistoryImage.objects.get(pk=data['cover_image'])).data
    data['writer'] = UserSerializer(User.objects.get(pk=data['writer'])).data

    return data
    