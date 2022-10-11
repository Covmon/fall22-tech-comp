from django.db import models
from django.conf import settings
from tinymce.models import HTMLField

class HistoryEvent(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(help_text="Written as YYYY-MM-DD")
    cover_image = models.ForeignKey("HistoryImage", related_name="events", on_delete=models.CASCADE, null=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    content = HTMLField(null=True, blank=True)
    created_at = models.DateField(null=True, blank=True, help_text="Written as YYYY-MM-DD")
    active = models.BooleanField(default=True)
    custom_display_name = models.CharField(max_length=200, null=True, blank=True, help_text="Leave blank if you want your name to show up")
    featured = models.BooleanField(default=False)
    laugh_score = models.PositiveBigIntegerField(default=0)

    # objects = WorkManager()

    def __str__(self) -> str:
        return self.title

    def get_display_name(self):
        if self.custom_display_name:
            return self.custom_display_name
        return self.writer.display_name
    
    def get_preview_image(self):
        return self.cover_image

class HistoryImage(models.Model):
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="history_images/")
    title = models.CharField(max_length=255)
    order = models.IntegerField(default=1)
    custom_display_name = models.CharField(max_length=200, null=True, blank=True)
    original_work = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def get_display_name(self):
        if self.custom_display_name:
            return self.custom_display_name
        return self.artist.display_name
        
    class Meta:
        ordering = ["-created_at"]

# class View(models.Model):
#     event = models.ForeignKey(HistoryEvent, on_delete=models.CASCADE, related_name="views")
#     created_at = models.DateTimeField(auto_now_add=True)
#     cookie = models.CharField(max_length=255, null=True)

#     def __str__(self) -> str:
#         return f"{self.event.title} view at {self.created_at}"
