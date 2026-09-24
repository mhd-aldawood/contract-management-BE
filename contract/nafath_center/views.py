from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NafathCenterAgreement
from .serializers import NafathCenterAgreementSerializer


class NafathCenterCreateView(APIView):
    """
    POST /api/nafath-center/create/
    Accepts both application/json and multipart/form-data.
    """
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = NafathCenterAgreementSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'تم حفظ الاتفاقية بنجاح', 'data': serializer.data},
            status=status.HTTP_201_CREATED,
        )


class NafathCenterListView(APIView):
    """GET /api/nafath-center/  — list all agreements."""

    def get(self, request, *args, **kwargs):
        qs = NafathCenterAgreement.objects.all()
        serializer = NafathCenterAgreementSerializer(
            qs, many=True, context={'request': request}
        )
        return Response({'data': serializer.data})