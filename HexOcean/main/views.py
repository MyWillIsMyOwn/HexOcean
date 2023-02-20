from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, GroupSerializer, ImageSerializer
from .models import Image
from rest_framework import generics, permissions, status, viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
import magic


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ImageList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)


class ImageUpload(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [FileUploadParser]

    def post(self, request):
        uploaded_photo = request.data["file"]
        mime = magic.Magic(mime=True)
        uploaded_photo_mime = mime.from_buffer(uploaded_photo.read())
        if uploaded_photo_mime not in ["image/jpeg", "image/png"]:
            return Response(
                {"error": "Wrong file type. Only JPEG and PNG are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        owner = request.user
        image_object = Image(
            owner=owner, picture=uploaded_photo, name=str(uploaded_photo)
        )
        image_object.save()
        serializer = ImageSerializer(image_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
