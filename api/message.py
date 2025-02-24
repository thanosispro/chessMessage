from .models import Message 
from .serializers import MessageSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class getMessage(APIView):
    def get(self,request):
        return Response(MessageSerializer(Message.objects.all(),many=True).data)