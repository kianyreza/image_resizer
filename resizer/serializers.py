from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser


class ImageResizeSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    width = serializers.IntegerField(required=True, min_value=10, max_value=4000)
    height = serializers.IntegerField(required=True, min_value=10, max_value=4000)