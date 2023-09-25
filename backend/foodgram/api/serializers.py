from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, RecipeIngredient, Recipe,
                            ShoppingCart, Tag)
from users.models import User


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(write_only=True)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Количество ингредиента должно быть больше нуля."
            )
        return value


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient_id')
    name = serializers.SerializerMethodField(read_only=True)
    measurement_unit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'amount', 'measurement_unit',)

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipesReadSerializer(serializers.ModelSerializer):

    tags = TagsSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'name',
            'image',
            'text',
            'id',
            'ingredients',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )
        read_only_fields = ['tags', 'author', 'name', 'image',
                            'text', 'id', 'ingredients', 'cooking_time']

    def get_image(self, obj):
        return obj.image.url

    def get_ingredients(self, obj):
        return RecipeIngredientReadSerializer(
            obj.ingredients_amount.all(), many=True
        ).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj,
                                           user=request.user).exists()


class RecipesWriteSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientWriteSerializer(many=True)
    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'image', 'text',
                  'ingredients', 'cooking_time',)

    def to_representation(self, instance):
        serializer = RecipesReadSerializer(instance, context=self.context)
        return serializer.data

    def add_ingredients(self, recipe, ingredients):
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient,
                    pk=ingr.get('id')),
                amount=ingr.get('amount')
            ) for ingr in ingredients
        ])

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError("Выберите хотя бы один тег.")
        if len(set(value)) != len(value):
            raise serializers.ValidationError("Теги должны быть уникальными.")
        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError("Выберите хотя "
                                              "бы один ингредиент.")

        ingredient_ids = [item['id'] for item in value]
        if len(set(ingredient_ids)) != len(ingredient_ids):
            raise serializers.ValidationError("Ингредиенты должны "
                                              "быть уникальными.")

        return value

    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError("Время приготовления "
                                              "должно быть больше нуля.")
        return value

    def validate_name(self, value):
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Название рецепта "
                                              "должно содержать буквы.")
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = self.initial_data.get('tags')
        cooking_time = validated_data.pop('cooking_time')
        author = serializers.CurrentUserDefault()(self)
        new_recipe = Recipe.objects.create(
            author=author,
            cooking_time=cooking_time,
            **validated_data
        )
        new_recipe.tags.set(tags)
        self.add_ingredients(new_recipe, ingredients)
        return new_recipe

    def update(self, recipe, validated_data):
        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            recipe.ingredients_amount.all().delete()
            self.add_ingredients(recipe, ingredients)
        tags = self.initial_data.pop("tags")
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('id',)


class RecipeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class FollowRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="author.email")
    id = serializers.ReadOnlyField(source="author.id")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        return obj.user.follower.filter(author=obj.author).exists()

    def get_recipes(self, obj):
        queryset = (
            obj.author.recipe.all().order_by('-pub_date'))
        limit = self.context.get('request').query_params.get('recipes_limit')
        if limit:
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                raise ValueError(
                    'Неверно указан параметр для ограничения рецептов.'
                )
        return FollowRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipe.all().count()
