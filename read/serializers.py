from rest_framework import serializers
from account.models import User
from read.models import ArtWork, Magazine, Work

class ArtworkSerializer(serializers.ModelSerializer):
  class Meta:
    model = ArtWork
    fields = ('pk', 'artist', 'image', 'title', 'order', 'custom_display_name', 'original_work', 'created_at')
    
  def to_representation(self, instance):
    data = super().to_representation(instance)
    data['artist'] = UserSerializer(User.objects.get(pk=data['artist'])).data

    return data

class MagazineSerializer(serializers.ModelSerializer):
  class Meta:
    model = Magazine
    fields = ('pk', 'title', 'description', 'special_link', 'featured', 'active', 'cover_image', 'issue_editor', 'custom_issue_editor', 'art_editor', 'custom_art_editor', 'created_at')

  def to_representation(self, instance):
    data = super().to_representation(instance)
    data['cover_image'] = ArtworkSerializer(ArtWork.objects.get(pk = data['cover_image'])).data
    data['issue_editor'] = UserSerializer(User.objects.get(pk=data['issue_editor'])).data
    data['art_editor'] = UserSerializer(User.objects.get(pk=data['art_editor'])).data

    return data

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('pk', 'email', 'url_username', 'display_name', 'first_name', 'last_name', 'bio', 'year_joined', 'graduation_year', 'board')

class WorkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Work
    fields = ('pk', 'title', 'art_work', 'magazine', 'writer', 'content', 'created_at', 'voice_file', 'active', 'classic', 'custom_display_name', 'featured', 'laugh_score', 'original_work')

  def to_representation(self, instance):
    data = super().to_representation(instance)
    data['art_work'] = ArtworkSerializer(ArtWork.objects.get(pk=data['art_work'])).data
    data['magazine'] = MagazineSerializer(Magazine.objects.get(pk=data['magazine'])).data
    data['writer'] = UserSerializer(User.objects.get(pk=data['writer'])).data

    return data
    