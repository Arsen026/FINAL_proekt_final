import json
from http.client import responses

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import *
from .serializer import *

class FilmApiView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAdminUser]
    # permission_classes -> Какие права доступа, применять на этот АПИ
    # AllowAny -> Доступен любому

    def get(self, request, pk=None):
        if pk is not None:
            try:
                film = Film.objects.get(pk=pk)
                data = FilmSerializer(film).data
                return Response(data, status=status.HTTP_200_OK)
            except Film.DoesNotExist:
                return Response({"detail": "Film not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            films = Film.objects.all()
            data = FilmSerializer(films, many=True).data
            return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FilmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = json.loads(request.body)
        pk = data.get('id')
        print(pk)
        if pk is not None:
            try:
                film = Film.objects.get(pk=pk)
                film.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Film.DoesNotExist:
                return Response({"detail": "Film not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"detail": "No film ID provided."}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        film_id = request.data.get('id')
        # request.data.get('<KEY>') -> Берет значение из запроса по ключу <KEY>,
        #   если такого ключа нету в теле запроса, то вернет None
        if film_id is None:
            return Response(data={'detail': 'Ты забыл добавить id! косяк!'}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     book = Book.objects.get(id=book_id)
        # except Book.DoesNotExist:
        #     return Response(data={'message': 'Book does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        from django.shortcuts import get_object_or_404
        film = get_object_or_404(Film, id=film_id)
        # get_object_or_404 ->

        film_serializer = FilmSerializer(film, data=request.data, partial=True)
        if film_serializer.is_valid():
            film_serializer.save()
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data=film_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProducerApiView(APIView):
    permission_classes = [AllowAny]
    # permission_classes -> Какие права доступа, применять на этот АПИ
    # AllowAny -> Доступен любому
    def get(self, request, pk=None):
        if pk is not None:
            try:
                producer = Producer.objects.get(pk=pk)
                data = ProducerSerializer(producer).data
                return Response(data, status=status.HTTP_200_OK)
            except Producer.DoesNotExist:
                return Response({"detail": "Producer not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            producers = Producer.objects.all()
            data = ProducerSerializer(producers, many=True).data
            return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        producer_id = request.data.get('id')
        if producer_id is None:
            return Response(data={'detail': 'Ты забыл добавить id! косяк!'}, status=status.HTTP_400_BAD_REQUEST)

        from django.shortcuts import get_object_or_404
        producer = get_object_or_404(Producer, id=producer_id)

        producer_serializer = ProducerSerializer(producer, data=request.data, partial=True)
        if producer_serializer.is_valid():
            producer_serializer.save()
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data=producer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # у меня такой патч что в country нужно кидать уже имеющийся айди("country": "2")!!!! нужен для патч запроса в постмане

class SecretApiView(APIView):
    permission_classes = [IsAdminUser]  # Проверяет авторизован ли пользователь

    def get(self, request):
        return Response(data={'secret': '1+1=11'}, status=status.HTTP_200_OK)

class RegistrationApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.db import IntegrityError
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            CustomUser.objects.create_user(email=email, password=password)
            return Response(data={'message': 'Registration success'}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(data={'message': 'email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

class AuthApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth import login, authenticate
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return Response(data={'message': 'Invalid email/password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            login(request, user)
            return Response(data={'message': 'Auth success!'}, status=status.HTTP_200_OK)

class CabinetApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user -> Если пользователь авторизован, то юзер лежит в request.user
        data = UserSerializer(request.user, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)

    def delete(self, request):
        request.user.delete()
        return Response(data={'message': 'OK!'}, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user

        userSerializer = UserSerializer(user, data=request.data, partial=True)
        if userSerializer.is_valid():
            userSerializer.save()
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data=userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CocktailApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        import requests  # pip install requests
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
        if response.status_code != 200:
            return Response(data={'Message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            cocktail = response.json()
            data = {
                'name': cocktail['drinks'][0]['strDrink'],
                'photo': cocktail['drinks'][0]['strDrinkThumb']
            }
            return Response(data=data, status=status.HTTP_200_OK)

class FilmgetApiView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes -> Какие права доступа, применять на этот АПИ


    def get(self, request, pk=None):
        if pk is not None:
            try:
                film = Film.objects.get(pk=pk)
                data = FilmSerializer(film).data
                return Response(data, status=status.HTTP_200_OK)
            except Film.DoesNotExist:
                return Response({"detail": "Film not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            films = Film.objects.all()
            data = FilmSerializer(films, many=True).data
            return Response(data, status=status.HTTP_200_OK)

class FavfilmApiView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]
    # permission_classes -> Какие права доступа, применять на этот АПИ
    # AllowAny -> Доступен любому

    def get(self, request):
        films_user = request.user.fav_films.all()
        data = FilmSerializer(films_user, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        film_id = request.data.get("id")
        if film_id is None:
            return Response({"detail": "Film id not found. Id is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            film = get_object_or_404(Film, id = film_id)
            if film not in request.user.fav_films.all():
                request.user.fav_films.add(film)
                return Response({"detail": "фильм добавлен в ваши любимые"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "фильм уже есть в любимых"}, status=status.HTTP_400_BAD_REQUEST)

class FilmSearchApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.GET.get('search')
        film_by_name = Film.objects.filter(name__contains=search)
        # __search -> Ищет слово целиком
        # __contains -> Ищет символы без регистра
        # __icontains -> Ищет символы c регистра

        data = FilmSerializer(film_by_name, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

class BookOrderApiView(APIView):
    # сортировка деск и аск
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # desc(Descending) убывание, asc(Ascending) возврастанию
        year = request.GET.get('year')
        name = request.GET.get('name')
        films = Film.objects.all()

        if year is not None:
            if year == 'desc':
                films = films.order_by('-year')  # 9 -> 0
            elif year == 'asc':
                films = films.order_by('year')  # 0 -> 9

        if name is not None:
            if name == 'desc':
                films = films.order_by('-name')  # Z -> A
            elif name == 'asc':
                films = films.order_by('name')  # A -> Z
        data = FilmSerializer(films, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)