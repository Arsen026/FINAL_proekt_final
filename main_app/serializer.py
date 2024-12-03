from rest_framework.serializers import ModelSerializer
from .models import *

class FilmSerializer(ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'

    # to_representation -> Функция в сериалайзере, которая конвертирует из Объекта в JSON
    def to_representation(self, instance):  # instance -> Джанговский Объект, который конвертируем
        # representation = {}
        # representation['name'] = instance.name.upper()

        representation = super().to_representation(instance)  # JSON где id вместо author и genres

        representation['producer'] = ProducerSerializer(instance.producer, many=False).data
        representation['genre'] = GenreSerializer(instance.genre, many=False).data
        representation['languages'] = LanguageSerializer(instance.languages, many=True).data
        representation['awards'] = AwardsSerializer(instance.awards, many=True).data
        # Конверитую автора через AuthorSerializer и запихиваю в ключик 'author'

        # representation['author'] = {
        #     'id': instance.author.id,
        #     'name': instance.author.name,
        #     'surname': instance.author.surname
        # }

        representation['publisher'] = 'ABC Public Library'
        return representation

class ProducerSerializer(ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'

    def to_representation(self, instance):  # instance -> Джанговский Объект, который конвертируем
        representation = super().to_representation(instance)  # JSON где id вместо author и genres

        representation['country'] = CountrySerializer(instance.country, many=False).data
        return representation

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class AwardsSerializer(ModelSerializer):
    class Meta:
        model = Awards
        fields = '__all__'

class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

from django.contrib.auth.models import User
class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'date_joined']