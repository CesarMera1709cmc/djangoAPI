from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

# Simulación de base de datos en memoria
data_list = [
    {'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True},
    {'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True},
    {'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False},
]

# Vista para GET y POST
class DemoRestApi(APIView):
    def get(self, request):
        return Response(data_list, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Campos "name" y "email" son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        new_item = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'email': data['email'],
            'is_active': True
        }
        data_list.append(new_item)
        return Response({'message': 'Creado exitosamente', 'data': new_item}, status=status.HTTP_201_CREATED)

# Vista para PUT, PATCH y DELETE
class DemoRestApiItem(APIView):
    def find_item(self, item_id):
        for item in data_list:
            if item['id'] == item_id:
                return item
        return None

    def put(self, request, item_id):
        item = self.find_item(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Campos "name" y "email" son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        item['name'] = data['name']
        item['email'] = data['email']
        item['is_active'] = data.get('is_active', item['is_active'])

        return Response({'message': 'Actualizado exitosamente', 'data': item}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        item = self.find_item(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        item.update(request.data)
        return Response({'message': 'Actualizado parcialmente', 'data': item}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        item = self.find_item(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        item['is_active'] = False
        return Response({'message': 'Eliminado lógicamente'}, status=status.HTTP_200_OK)
