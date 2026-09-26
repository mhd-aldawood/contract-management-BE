from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contract.life_long.serializers import LifeLongAgreementSerializer


class LifeLongCreateView(APIView):
    """
    POST /api/life-long/create/
    Accepts both application/json and multipart/form-data.
    """
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = LifeLongAgreementSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'تم حفظ الاتفاقية بنجاح'},
            status=status.HTTP_201_CREATED,
        )