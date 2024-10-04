import logging
from rest_framework import status 
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializser


logger = logging.getLogger(__name__)


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializser
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        cache_key = f"item_{item_id}"
        logger.debug(f"Retrieving item with ID: {item_id}")
        cached_item = cache.get(cache_key)

        if  cached_item:
            logger.info(f"Cache hit for item {item_id}")
            return Response(cached_item)
        
        logger.info(f"Cache miss for item {item_id}, fetching from database")        
        item = self.get_object()
        serializer = self.get_serializer(item)

        cache.set(cache_key, serializer.data, timeout=60*15)
        logger.debug(f"Cached item {item_id} for 15 minutes")

        return Response(serializer.data)

        
    def update(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        logger.debug(f"Updating item with ID: {item_id}")

        response = super().update(request, *args, **kwargs)

        cache_key= f"item_{item_id}"
        cache.delete(cache_key)
        logger.info(f"Cache for item {item_id} cleared after update")

        return response
    
    def destroy(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        logger.debug(f"Deleting item with ID: {item_id}")

        cache_key = f"item_{item_id}"
        cache.delete(cache_key)
        logger.info(f"Cache for item {item_id} cleared after deletion")

        return super().destroy(request, *args, **kwargs)