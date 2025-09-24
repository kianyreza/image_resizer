from django.urls import path
from .views import ImageResizeView

urlpatterns = [
    path('resize/', ImageResizeView.as_view(), name='resize-image'),
]