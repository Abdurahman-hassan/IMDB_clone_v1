"""URLs for the watchlist app."""
from django.urls import path, include
from rest_framework import routers

# function based views
from watchlist.api.views import (
    watch_list_manual_serializer_deserializer,
    single_watch_list_manual_serializer_deserializer,
    watch_list_detail_manual_serializer_deserializer
)
# function based views using a serializer class
from watchlist.api.views import (
    watch_list_using_serializer_class,
    single_watch_list_using_serializer_class,
    watch_list_detail_using_serializer_class
)

# class based views APIView
from watchlist.api.views import (
    WatchListAV,
    WatchListDetailAV,
    StreamPlatformAV,
    StreamPlatformDetailAV
)

# class based views Mixins views
from watchlist.api.views import (
    ReviewListMXV,
    ReviewDetailMV
)

# class based views generic class based views with relationships
from watchlist.api.views import (
    WatchListCreateGNV,
    ReviewListGNV,
    ReviewCreateGNV,
    ReviewDetailGNV,
    UserReviewGNV
)

# viewSets
from watchlist.api.views import StreamPlatformVSV

# viewSets using ModelViewSet
from watchlist.api.views import (
    StreamPlatformMVV,
    StreamPlatformMVVR
)

app_name = 'watchlist'

# routers help us to create urls for our models by combining the urls
router = routers.DefaultRouter()
# stream is the url name
router.register('stream-viewset', StreamPlatformVSV, basename='streamplatform-viewset')
router.register('stream-modelviewset', StreamPlatformMVV, basename='streamplatform-modelviewset')
router.register('stream-read', StreamPlatformMVVR, basename='streamplatform-read')
path('', include(router.urls)),

urlpatterns = [
    ##################################################################################
    ##################################################################################
    # function based views
    ##################################################################################
    # using manual serializer and deserializer
    ###################################################################################
    # path('fbv-watchlist-list', watch_list_manual_serializer_deserializer, name='fbv_watchlist'),
    # path('fbv-watchlist-detail/<int:movie_id>',
    # single_watch_list_manual_serializer_deserializer, name='fbv_movie_detail'),
    # path('fbv-watchlist-more-detail/<int:movie_id>',watch_list_detail_manual_serializer_deserializer,
    #      name='fbv_movie_more_detail'),
    ##################################################################################
    ##################################################################################
    # using a serializer class
    ##################################################################################
    path('fbv-watchlist-list', watch_list_using_serializer_class, name='fbv_watchlist'),
    path('fbv-watchlist-detail/<int:movie_id>', single_watch_list_using_serializer_class, name='fbv_movie_detail'),
    path('fbv-watchlist-more-detail/<int:movie_id>', watch_list_detail_using_serializer_class,
         name='fbv_movie_more_detail'),
    ##################################################################################
    ##################################################################################
    # class based views
    ##################################################################################
    # APIView
    ##################################################################################
    path('list/', WatchListAV.as_view(), name='watchlist-list'),
    path('list/<int:pk>/', WatchListDetailAV.as_view(), name='watchlist-detail'),
    path('stream/', StreamPlatformAV.as_view(), name='streamplatform-list'),
    path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    ##################################################################################
    # Mixins views
    ##################################################################################
    path('stream/review/', ReviewListMXV.as_view(), name='review-list'),
    path('stream/review/<int:pk>/', ReviewDetailMV.as_view(), name='review-detail'),
    ##################################################################################
    ##################################################################################
    # generic class based views with relationships
    ##################################################################################
    path('stream-create/', WatchListCreateGNV.as_view(), name='stream-create'),
    path('stream/<int:watchlist_id>/review-create/', ReviewCreateGNV.as_view(), name='review-create'),
    path('stream/<int:watchlist_id>/review/', ReviewListGNV.as_view(), name='review-list'),
    # path('stream/<int:watchlist_id>/review/<int:pk>/', ReviewDetailGNV.as_view(), name='review-detail'),
    path('stream/review/<int:pk>/', ReviewDetailGNV.as_view(), name='review-detail'),
    path('reviews/', UserReviewGNV.as_view(), name='user-review-detail'),

]
urlpatterns += router.urls
