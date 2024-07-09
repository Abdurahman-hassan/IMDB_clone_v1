"""Views for the API."""
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, viewsets, mixins, filters
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView

from watchlist.api.pagination import WatchlistPagination, WatchlistOffsetPagination, WatchlistCursorPagination
from watchlist.api.permissions import (
    AdminOrReadOnly,
    ReviewUserOrReadOnly
)
from watchlist.api.serializers import (WatchListSerializer,
                                       StreamPlatformSerializer,
                                       ReviewSerializer,
                                       ManualWatchListSerializer)
from watchlist.api.throttling import ReviewListThrottle, ReviewCreateThrottle
from watchlist.models import WatchList, StreamPlatform, Review
from django.http import JsonResponse
from watchlist.models import WatchList


############################################################################################################
############################################################################################################
# function based views manual serialization/ deserialization
############################################################################################################

def watch_list_manual_serializer_deserializer(request):
    movies = WatchList.objects.all()
    # all returns a queryset, so we need to convert it to a list
    print(movies.values('name', 'description'))
    data = {
        'movies': list(movies.values('name', 'description'))
    }
    return JsonResponse(data)


def single_watch_list_manual_serializer_deserializer(request, movie_id):
    movie = WatchList.objects.get(pk=movie_id)
    # get returns a single object, so we can access its attributes directly
    data = {
        'movie': {
            'name': movie.name,
            'description': movie.description,
        }
    }
    return JsonResponse(data)


def watch_list_detail_manual_serializer_deserializer(request, movie_id):
    movie = WatchList.objects.filter(pk=movie_id)
    # filter returns a queryset, so we need to convert it to a list
    data = {
        'movie':
            list(movie.values('name', 'description'))
    }
    return JsonResponse(data)


############################################################################################################
# function based views using a serializer class
############################################################################################################
@api_view(['GET', 'POST'])
def watch_list_using_serializer_class(request):
    if request.method == 'GET':
        movies = WatchList.objects.all()
        serializer = ManualWatchListSerializer(movies, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ManualWatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # this serializer.data is the data that we just created of the return of the serializer created function
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'put', 'delete'])
def single_watch_list_using_serializer_class(request, movie_id):
    if request.method == 'GET':
        try:
            movie = WatchList.objects.get(pk=movie_id)
        except WatchList.DoesNotExist:
            return Response(data={'Error': 'Movie not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = ManualWatchListSerializer(movie)
        return Response(serializer.data)

    if request.method == 'PUT':
        # if we didn't get which movie to update and send it to serializer
        # it will create a new movie instead of updating the existing one
        # we need to send the movie id in the request {'id':1, ...}
        # or we can get which movie to update and send it to the serializer
        movie = WatchList.objects.get(pk=movie_id)
        serializer = ManualWatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        movie = WatchList.objects.get(pk=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def watch_list_detail_using_serializer_class(request, movie_id):
    movie = WatchList.objects.filter(pk=movie_id)
    # filter returns a queryset, so we need to convert it to a list
    serializer = ManualWatchListSerializer(movie, many=True)
    # if I will use JsonResponse i need to pass safe=False
    return JsonResponse(serializer.data, safe=False)


############################################################################################################
############################################################################################################
# class based views
############################################################################################################

############################################################################################################
# ApiViewClass
############################################################################################################
class WatchListAV(APIView):
    """List all movies with ApiViewClass."""
    permission_classes = [AdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # this serializer.data is the data that we just created of the return of the serializer created function
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailAV(APIView):
    """Retrieve, update or delete a movie instance."""
    permission_classes = [AdminOrReadOnly]

    def get_object(self, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            return movie
        except WatchList.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = self.get_object(pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformAV(APIView):
    """List all stream platforms."""
    permission_classes = [AdminOrReadOnly]

    def get(self, request):
        stream_platforms = StreamPlatform.objects.all()
        # we add context={'request': request} to get the url of the related objects in the serializer
        # that if we use the HyperlinkedModelSerializer
        serializer = StreamPlatformSerializer(stream_platforms,
                                              many=True,
                                              context={'request': request})

        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):
    """Retrieve a stream platform."""
    permission_classes = [AdminOrReadOnly]

    def get_object(self, platform_id):
        try:
            platform = StreamPlatform.objects.get(pk=platform_id)
            return platform
        except StreamPlatform.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        platform = self.get_object(pk)
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform = self.get_object(pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = self.get_object(pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


############################################################################################################
############################################################################################################
# Mixins
############################################################################################################

class ReviewDetailMV(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    """Retrieve, update or delete a review."""

    # These are attributes names and we can't change them
    permission_classes = [AdminOrReadOnly]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReviewListMXV(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    """List all reviews."""
    permission_classes = [ReviewUserOrReadOnly]

    # These are attributes names and we can't change them
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # the perform_create method is a place where you can modify
    # how the instance save operation is managed.
    # This method is called by the create method just before it saves an instance.
    # If you override the create method, you would need to handle all steps manually.
    # like create a new instance, check if the instance is valid, save the instance, and return the response.
    # On the other hand, perform_create is specifically designed to handle the save operation.
    # It receives the validated serializer, and its only job is to save the instance.
    # This makes it a suitable place to add any custom logic that should run just before or after saving the instance.
    # the reviewer is not part of the incoming data, but is instead based on the current request.
    def perform_create(self, serializer):
        # sets the reviewer to the currently authenticated user when creating a Review.
        serializer.save(reviewer=self.request.user)


############################################################################################################
############################################################################################################
# generic class based views with relationships
############################################################################################################

# We will use the generic class based views itself
# we don't need to define the get, post, put, delete methods
# it will be done automatically because it's inherited the mixins.

# this class for testing purposes only
class WatchListCreateGNV(generics.ListCreateAPIView):
    """List all movies or create a new movie."""
    permission_classes = [AdminOrReadOnly]
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # pagination_class = WatchlistPagination
    # pagination_class = WatchlistOffsetPagination
    pagination_class = WatchlistCursorPagination  # ordering with time if we choose there created
    # we must have ordering_field field here
    # ordering_fields = ['avg_rating', 'created'] # the default ordering

    # we can override the perform_create method to add extra logic
    def perform_create(self, serializer):
        # we can add extra logic here
        serializer.save()


class ReviewCreateGNV(generics.CreateAPIView):
    """Create a review,
       This class doesn't have a queryset because we don't need to get the reviews.
    """
    permission_classes = [ReviewUserOrReadOnly]

    queryset = Review.objects.none()
    serializer_class = ReviewSerializer

    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # the pk is the watchlist_id
        watchlist_id = self.kwargs['watchlist_id']
        watchlist = WatchList.objects.get(pk=watchlist_id)

        user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, reviewer=user)
        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie')

        if watchlist.number_rating == 0:
            # if the movie has no rating, we will set the rating to 5
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        # we need to pass the movie to the serializer to save it in the review model
        # now we don't need to send the movie id and the reviewer id in the request
        serializer.save(watchlist=watchlist, reviewer=user)


class ReviewListGNV(generics.ListAPIView):
    """List all reviews."""
    # ListCreate will give us the get and post methods
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['watchlist_id']
        return Review.objects.filter(watchlist=pk)

    # or

    # def get_queryset(self):
    #     if self.kwargs.get('platform_id'):
    #         return Review.objects.filter(watchlist=self.kwargs.get('platform_id'))
    #     return Review.objects.all()


class ReviewDetailGNV(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a review."""
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ReviewCreateThrottle, AnonRateThrottle]

    # RetrieveUpdateDestroy will give us the get, put, delete methods
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        watch_list = self.kwargs['watchlist_id']
        return Review.objects.filter(watchlist=watch_list)


class UserReviewGNV(generics.ListAPIView):
    """List all reviews by a user."""
    serializer_class = ReviewSerializer

    # permission_classes = [IsAuthenticated]
    # the django-filter will only work with GenericAPIView
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['reviewer__username', 'active']
    filter_backends = [filters.SearchFilter]
    search_fields = ['reviewer__username', 'active']
    pagination_class = WatchlistPagination

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = Review.objects.none()
        if username is not None:
            queryset = Review.objects.filter(reviewer__username=username)
        return queryset


############################################################################################################
############################################################################################################
# ViewSets
############################################################################################################

class StreamPlatformVSV(viewsets.ViewSet):
    """List all stream platforms."""
    permission_classes = [AdminOrReadOnly]
    # if we define the throttle_classes manually here, it will override the default throttle_classes
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'stream_platform'

    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True,
                                              context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        platform = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(platform,
                                              context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data,
                                              context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data,
                                              context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


############################################################################################################
############################################################################################################
# model viewSet
############################################################################################################
class StreamPlatformMVV(viewsets.ModelViewSet):
    """List all stream platforms."""
    permission_classes = [AdminOrReadOnly]

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class StreamPlatformMVVR(viewsets.ReadOnlyModelViewSet):
    """List all stream platforms."""
    permission_classes = [AdminOrReadOnly]

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
