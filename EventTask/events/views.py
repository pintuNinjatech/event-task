import logging

from django.core.cache import cache
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event
from .serializers import (
    CreateEventSerializer,
    ListEventSerializer,
    QueryParamsSerializer,
)

logger = logging.getLogger(__name__)


class EventListAPIView(APIView):

    def get_params(self):
        starts_at = self.request.GET.get('starts_at')
        ends_at = self.request.GET.get('ends_at')
        if not all([starts_at, ends_at]):
            logger.info("Missing 'starts_at' or 'ends_at' fields")
        return starts_at, ends_at

    @swagger_auto_schema(
        query_serializer=QueryParamsSerializer,
        responses={
            200: openapi.Response("Success response", ListEventSerializer),
            400: openapi.Response("Error response"),
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            starts_at, ends_at = self.get_params()
            if starts_at and ends_at:
                events = Event.objects.in_datetime_range(starts_at, ends_at)
            else:
                events = Event.objects.all()
            serialized_events = ListEventSerializer(events, many=True)
            return Response(
                {
                    'message': 'Data fetched successfully.',
                    'status': status.HTTP_200_OK,
                    'data': {'events': serialized_events.data}
                }
            )
        except (ValueError, TypeError) as error:
            logger.error(f"Error processing request: {error}")
            raise APIException(code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    @swagger_auto_schema(auto_schema=None)
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def list_of_ids(request):
    try:
        last_data = cache.get('last_polled_ids')

        if last_data:
            logger.info("Returning data from cache")
            return JsonResponse(last_data, safe=False)
        logger.info("Updating data from DB")
        event_ids = Event.objects.values('base_event_id', 'event_id')
        data = [
            f"{event.get('base_event_id')}:{event.get('event_id')}" for event in event_ids
        ]
        cache.set('last_polled_ids', data, timeout=600)
        return JsonResponse(data, safe=False)
    except Exception as error:
        raise APIException(code=status.HTTP_400_BAD_REQUEST, detail=str(error))
