from movielist.models import Movie
from showtimes.models import Cinema, Screening
from rest_framework import serializers


# The serializers in REST framework work very similarly to Django's Form and ModelForm classes.
# We provide a Serializer class which gives you a powerful, generic way to control the output of your responses,
# as well as a ModelSerializer class which provides a useful shortcut for creating serializers that deal with model instances and querysets.


class CinemaSerializer(serializers.ModelSerializer):
    movies = serializers.HyperlinkedRelatedField(
        # HyperlinkedRelatedField - because we want to show movies as links
        many=True,
        read_only=True,
        view_name='movies-detail'
    )

    class Meta:
        model = Cinema
        fields = '__all__'


class ScreeningSerializer(serializers.ModelSerializer):
    cinema = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Cinema.objects.all()
    )
    movie = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Movie.objects.all()
    )

    class Meta:
        model = Screening
        fields = '__all__'
