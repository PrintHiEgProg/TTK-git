from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClientSerializer, IntentSerializer
from admin_interface.models import Client, Intent


@api_view(["GET", "POST"])
def get_routes(request):
    routes = [
        {"method": "GET", "url": "/api/clients", "description": "List all clients"},
        {"method": "GET", "url": "/api/intents", "description": "List all intents"},
        {"method": "POST", "url": "/api/clients/create", "description": "Create a new client"},
        {"method": "POST", "url": "/api/intents/create", "description": "Create a new intent"},
        {"method": "DELETE", "url": "/api/clients/delete/<id>", "description": "Delete a specific client by ID"},
        {"method": "DELETE", "url": "/api/intents/delete/<id>", "description": "Delete a specific intent by ID"},
    ]
    return Response(routes)


@api_view(["GET"])
def get_clients(request):
    projects = Client.objects.all()
    serializer = ClientSerializer(projects, many=True).data
    return Response(serializer)


@api_view(["GET"])
def get_intents(request):
    projects = Intent.objects.all()
    serializer = IntentSerializer(projects, many=True).data
    return Response(serializer)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_intent(request):
    serializer = IntentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE", "POST"])
@permission_classes([IsAuthenticated])
def delete_intent(request, id):
    try:
        intent = Intent.objects.get(id=id)
        intent.delete()
        return Response({"message": "Intent deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Intent.DoesNotExist:
        return Response({"message": "Intent not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["DELETE", "POST"])
@permission_classes([IsAuthenticated])
def delete_client(request, id):
    try:
        client = Client.objects.get(id=id)
        client.delete()
        return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Intent.DoesNotExist:
        return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

