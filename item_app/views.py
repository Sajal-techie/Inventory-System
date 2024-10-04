import logging
from rest_framework import status 
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializser


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializser
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        print(args,kwargs,request.data)
        item_id = kwargs.get('pk')
        cache_key = f"item_{item_id}"

        cached_item = cache.get(cache_key)
        print(cached_item, cache_key, 'cache')
        if  cached_item:
            return Response(cached_item)
        print('after cache')
        item = self.get_object()
        serializer = self.get_serializer(item)

        cache.set(cache_key, serializer.data, timeout=60*15)

        return Response(serializer.data)

        
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        item_id = kwargs.get('pk')
        cache_key= f"item_{item_id}"
        cache.delete(cache_key)

        return response
    
    def destroy(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        cache_key = f"item_{item_id}"
        cache.delete(cache_key)

        return super().destroy(request, *args, **kwargs)