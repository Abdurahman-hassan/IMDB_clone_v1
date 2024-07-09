"""Serializers for the watchlist app."""
from rest_framework import serializers

from watchlist.models import StreamPlatform, Review, WatchList


############################################################################################################
############################################################################################################
# Manual Serializer
############################################################################################################
# step by step to create a serializer, manually
# I need to convert the 3 simple views that handle
# manually the serialization and deserialization of the data
# to use the serializer class
# movie_list_manual_serializer_deserializer,
# single_movie_manual_serializer_deserializer,
# movie_detail_manual_serializer_deserializer

# serializer level validation
def description_length(value):
    if len(value) < 10:
        raise serializers.ValidationError('Description is too short')


class ManualWatchListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(validators=[description_length])
    active = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return WatchList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    # object level validation
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError('Name and description must be different')
        return data

    # field level validation
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Name is too short')
        return value


############################################################################################################
############################################################################################################
# Model Serializer
############################################################################################################


# each Stream has a list of movies -> many movies to one stream
# each movie has one stream -> one stream to many movies
# also each movie has a list of reviews -> many reviews to one movie
# each review has one movie -> one movie to many reviews

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the review model."""
    reviewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        # we need to use all fields to show the watchlist field
        # because we are using it with mixin views
        # fields = '__all__'
        # we can exclude the watchlist field
        # because we pass it automatically in the generic views
        exclude = ('watchlist',)


# we can use ModelSerializer to create a serializer
class WatchListSerializer(serializers.ModelSerializer):
    # we can add extra fields to the serializer
    len_name = serializers.SerializerMethodField()
    len_description = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')  # model_name.field_name platform is a foreign key

    class Meta:
        model = WatchList
        fields = '__all__'
        # exclude = ('active',)

    # The naming convention for the method should be get_fieldname
    def get_len_name(self, object):
        return len(object.title)

    def get_len_description(self, object):
        return len(object.storyline)

    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError('Name and description must be different')
        return data

    # field level validation
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Name is too short')

        elif WatchList.objects.filter(name=value).exists():
            raise serializers.ValidationError('Movie name already exists')
        return value


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the stream platform model."""
    # watchlist is the name of related_name in the WatchList model
    watchlist = WatchListSerializer(many=True, read_only=True)

    # add string related field to get specific fields of the related objects not all of them
    # watchlist = serializers.StringRelatedField(many=True, read_only=True)
    # add primary key related field to get the primary key of the related objects
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # add hyperlink related field to get the url of the related objects
    # we mapped the watchlist to the watchlist-detail url
    # we need to attach <appname>:<url-name> to the view_name
    # because we are using the app_name = watchlist in the urls.py
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watchlist:watchlist-detail'
    # )

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        # This is because we are using the HyperlinkedModelSerializer
        # and we need to specify the view name and the lookup field
        # we need to attach <appname>:<url-name> to the view_name
        # because we are using the app_name = watchlist in the urls.py
        # if we don't added the appname inside urls.y we can remove extra_kwargs
        # because it's automatically added by the HyperlinkedModelSerializer
        extra_kwargs = {
            'url': {'view_name': 'watchlist:streamplatform-detail', 'lookup_field': 'pk'}
        }

    def validateـabout(self, value):
        if len(value) > 500:
            raise serializers.ValidationError('About platform is too long it should be less than 500 characters')
        return value

        # we can use serializers.Serializer to create a serializer
        # other types of validators

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('name is too short')

        if StreamPlatform.objects.filter(name=value).exists():
            raise serializers.ValidationError("name already exists")

        return value
