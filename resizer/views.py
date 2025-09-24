# resizer/views.py
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ImageResizeSerializer

from PIL import Image
import io


class ImageResizeView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageResizeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        image_file = validated_data['image']
        width = validated_data['width']
        height = validated_data['height']

        try:
            img = Image.open(image_file)
            resized_img = img.resize((width, height))

            img_byte_arr = io.BytesIO()
            img_format = img.format if img.format in ['JPEG', 'PNG', 'GIF'] else 'PNG'
            resized_img.save(img_byte_arr, format=img_format)
            img_byte_arr = img_byte_arr.getvalue()

            # ✅ استفاده از HttpResponse برای ارسال تصویر باینری
            response = HttpResponse(img_byte_arr, content_type=f'image/{img_format.lower()}')
            response['Content-Disposition'] = f'attachment; filename="resized_{image_file.name}"'
            return response

        except Exception as e:
            return Response({'error': f'Image processing failed: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)