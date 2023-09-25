from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import download_shopping_cart
from api.filters import IngredientFilter, RecipeFilter
from api.paginators import CustomPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    FavoriteSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeListSerializer,
    RecipesWriteSerializer,
    TagsSerializer,
)
from recipes.models import (Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag, User)


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
        queryset = Recipe.objects.all()
        author = self.request.user
        if self.request.GET.get('is_favorited'):
            favorite_recipes_ids = (
                Favorite.objects
                .filter(user=author)
                .values('recipe_id')
            )
            return queryset.filter(pk__in=favorite_recipes_ids)

        if self.request.GET.get('is_in_shopping_cart'):
            cart_recipes_ids = (
                ShoppingCart.objects
                .filter(user=author)
                .values('recipe_id')
            )
            return queryset.filter(pk__in=cart_recipes_ids)
        return queryset

    def add_in_list(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            error = f'Рецепт уже добавлен в {model.__name__}'
            response_data = {'errors': error}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, pk=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeListSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_in_list(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        error_message = f'Рецепт не добавлен в {model.__name__}'
        return Response({'errors': error_message},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_in_list(Favorite, request.user, pk)
        return self.delete_in_list(Favorite, request.user, pk)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_in_list(ShoppingCart, request.user, pk)
        return self.delete_in_list(ShoppingCart, request.user, pk)

    @action(methods=['GET'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        response = download_shopping_cart(request.user)
        return response


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [IngredientFilter]
    search_fields = ['^name']
    pagination_class = None


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.user.follower.filter(author=author).exists():
            error_message = "Вы уже подписаны на автора"
            return Response({"errors": error_message},
                            status=status.HTTP_400_BAD_REQUEST)
        follow_instance = request.user.follower.create(author=author)
        serializer = FollowSerializer(follow_instance,
                                      context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.user.follower.filter(author=author).exists():
            request.user.follower.filter(author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        error_message = "Автор отсутствует в списке подписок"
        return Response({"errors": error_message},
                        status=status.HTTP_400_BAD_REQUEST)


class SubscriptionsView(ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.follower.all()
