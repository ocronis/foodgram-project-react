from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .filters import IngredientFilter, RecipeFilter
from .paginators import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    FavoriteSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipesWriteSerializer,
    TagsSerializer,
)
from recipes.models import Favorite, Recipe, ShoppingCart

from .utils import (
    get_recipe_queryset,
    add_recipe_to_list,
    remove_recipe_from_list,
    download_shopping_cart,
    get_tags_queryset,
    get_ingredients_queryset,
    follow_user,
    unfollow_user,
    get_subscriptions_queryset,
)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['favorite', 'shopping_cart']:
            return FavoriteSerializer
        return RecipesWriteSerializer

    def get_queryset(self):
        return get_recipe_queryset(self.request)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return add_recipe_to_list(Favorite, request.user, pk)
        return remove_recipe_from_list(Favorite, request.user, pk)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return add_recipe_to_list(ShoppingCart, request.user, pk)
        return remove_recipe_from_list(ShoppingCart, request.user, pk)

    @action(methods=['GET'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_list = download_shopping_cart(request.user)
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; '
            f'filename="{self.request.user.username}_shopping_list.txt"'
        )
        return response


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_tags_queryset()
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_ingredients_queryset()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [IngredientFilter]
    search_fields = ['^name']
    pagination_class = None


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        return follow_user(request, id)

    def delete(self, request, id):
        return unfollow_user(request, id)


class SubscriptionsView(ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_subscriptions_queryset(self.request)
