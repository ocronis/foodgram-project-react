from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .filters import IngredientFilter, RecipeFilter
from .paginators import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    FavoriteSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeListSerializer,
    RecipesWriteSerializer,
    TagsSerializer,
)
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend


def get_recipe_queryset(request):
    queryset = Recipe.objects.all()
    author = request.user
    if request.GET.get('is_favorited'):
        favorite_recipes_ids = Favorite.objects
             .filter(user=author).values('recipe_id')
        return queryset.filter(pk__in=favorite_recipes_ids)
    if request.GET.get('is_in_shopping_cart'):
        cart_recipes_ids = ShoppingCart.objects
             .filter(user=author).values('recipe_id')
        return queryset.filter(pk__in=cart_recipes_ids)
    return queryset


def get_tags_queryset():
    return Tag.objects.all()


def get_ingredients_queryset():
    return Ingredient.objects.all()


def follow_user(request, id):
    author = get_object_or_404(User, id=id)
    if request.user.follower.filter(author=author).exists():
        error_message = "Вы уже подписаны на автора"
        return Response({"errors": error_message},
                        status=status.HTTP_400_BAD_REQUEST)
    follow_instance = request.user.follower.create(author=author)
    serializer = FollowSerializer(follow_instance,
                                  context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def unfollow_user(request, id):
    author = get_object_or_404(User, id=id)
    if request.user.follower.filter(author=author).exists():
        request.user.follower.filter(author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    error_message = "Автор отсутствует в списке подписок"
    return Response({"errors": error_message},
                    status=status.HTTP_400_BAD_REQUEST)


def get_subscriptions_queryset(request):
    return request.user.follower.all()


def add_recipe_to_list(model, user, pk):
    if model.objects.filter(user=user, recipe__id=pk).exists():
        error = f'Рецепт уже добавлен в {model.__name__}'
        response_data = {'errors': error}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(Recipe, pk=pk)
    model.objects.create(user=user, recipe=recipe)
    return Response(status=status.HTTP_201_CREATED)


def remove_recipe_from_list(model, user, pk):
    obj = model.objects.filter(user=user, recipe__id=pk)
    if obj.exists():
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    error_message = f'Рецепт не добавлен в {model.__name__}'
    return Response({'errors': error_message},
                    status=status.HTTP_400_BAD_REQUEST)


def download_shopping_cart(user):
    ingredients = user.shopping_cart.values(
        'recipe__ingredients_amount__ingredient__name',
        'recipe__ingredients_amount__ingredient__measurement_unit'
    ).annotate(amount=Sum('recipe__ingredients_amount__amount'))
    shopping_list = 'Список покупок:\n'
    count_ingredients = 0
    unit = (
        'ingr["recipe__ingredients_amount__ingredient"]'
        '["measurement_unit"]'
    )

    for ingr in ingredients:
        count_ingredients += 1
        shopping_list += (
            f'{count_ingredients}) '
            f'{ingr["recipe__ingredients_amount__ingredient__name"]} - '
            f'{ingr["amount"]} '
            f'({unit})\n'
        )
    return shopping_list
