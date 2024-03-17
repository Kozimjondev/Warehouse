from rest_framework.response import Response
from rest_framework.views import APIView

from .calculators import MaterialRequirementsCalculator
from .serializers import ProductsQuantitySerializer


class ProductMaterialsInfoAPIView(APIView):
    def post(self, request):
        serializer = ProductsQuantitySerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        calculator = MaterialRequirementsCalculator(serializer.validated_data)
        result = calculator.calculate()
        return Response({"result": result})
