from showtimes.models import Cinema
from rest_framework import serializers


class CinemaSerializer(serializers.ModelSerializer):
    movies = serializers.HyperlinkedRelatedField(
        # HyperlinkedRelatedField - because we want to show movies as links
        many=True,
        read_only=True,
        view_name='movies-detail'
    )

    class Meta:
        model = Cinema
        fields = ['name', 'city', 'movies']
