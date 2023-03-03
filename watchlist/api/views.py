"""Views for the API."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from watchlist.api.serializers import MovieSerializer, StreamPlatformSerializer
from watchlist.models import WatchMoviesList, StreamPlatform


class StreamPlatformList(APIView):
    """List all stream platforms."""
    # add validation to the view
    def get(self, request):
        stream_platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(stream_platforms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetail(APIView):
    """Retrieve a stream platform."""

    def get_object(self, platform_id):
        try:
            platform = StreamPlatform.objects.get(pk=platform_id)
            return platform
        except StreamPlatform.DoesNotExist:
            return Response(data={'Error': 'Platform not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def get(self, request, platform_id):
        platform = self.get_object(platform_id)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, platform_id):
        platform = self.get_object(platform_id)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, platform_id):
        platform = self.get_object(platform_id)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class based view
class MovieList(APIView):
    """List all movies."""

    def get(self, request):
        movies = WatchMoviesList.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetail(APIView):
    """Retrieve a movie."""

    def get_object(self, movie_id):
        try:
            movie = WatchMoviesList.objects.get(pk=movie_id)
            return movie
        except WatchMoviesList.DoesNotExist:
            return Response(data={'Error': 'Movie not found'},
                            status=status.HTTP_404_NOT_FOUND)

    # def get(self, request, movie_id):
    #     movie = self.get_object(movie_id)
    #     serializer = MovieSerializer(movie)
    #     return Response(serializer.data)

    def get(self, request, movie_id):
        try:
            movie = WatchMoviesList.objects.get(pk=movie_id)
        except WatchMoviesList.DoesNotExist:
            return Response(data={'Error': 'Movie not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, movie_id):
        try:
            movie = WatchMoviesList.objects.get(pk=movie_id)
        except WatchMoviesList.DoesNotExist:
            return Response(data={'Error': 'Movie not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, movie_id):
        try:
            movie = WatchMoviesList.objects.get(pk=movie_id)
        except WatchMoviesList.DoesNotExist:
            return Response(data={'Error': 'Movie not found'},
                            status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# method view
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     """List all movies."""
#     if request.method == 'GET':
#         movies = WatchMoviesList.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         # get data from user i don't need to get data from db
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#             # this serializer.data is the data that
#             # we just created of the return of the serializer created function
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, movie_id):
#     """Retrieve a movie."""
#     if request.method == 'GET':
#         try:
#             movie = WatchMoviesList.objects.get(pk=movie_id)
#         except WatchMoviesList.DoesNotExist:
#             return Response(data={'Error': 'Movie not found'},
#                             status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         try:
#             movie = WatchMoviesList.objects.get(pk=movie_id)
#         except WatchMoviesList.DoesNotExist:
#             return Response(data={'Error': 'Movie not found'},
#                             status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         try:
#             movie = WatchMoviesList.objects.get(pk=movie_id)
#         except WatchMoviesList.DoesNotExist:
#             return Response(data={'Error': 'Movie not found'},
#                             status=status.HTTP_404_NOT_FOUND)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
