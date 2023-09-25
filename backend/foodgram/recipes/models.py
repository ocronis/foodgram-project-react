from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator,
                                    validate_slug)
from django.db import models

from recipes.validators import ColorValidator
from users.validators import UserNameValidator
from users.models import User

class Ingredient(models.Model):
    name = models.CharField(
        max_length=settings.MAX_LENGTH_INGREDIENT,
        validators=[UserNameValidator()]
    )
    measurement_unit = models.CharField(
        max_length=settings.MAX_LENGTH_MEAS_UNIT
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredients',
            ),
        ]

class Tag(models.Model):
    name = models.CharField(
        max_length=settings.MAX_LENGTH_TAGS,
        unique=True,
        validators=[UserNameValidator()]
    )
    color = models.CharField(
        max_length=settings.MAX_LENGTH_TAGS_COLOR,
        unique=True,
        validators=[ColorValidator]
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_TAGS_SLUG,
        unique=True,
        validators=[validate_slug]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        max_length=settings.MAX_LENGTH_RECIPES,
        unique=True,
        validators=[UserNameValidator()]
    )
    image = models.ImageField(
        upload_to='recipes/image/'
    )
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField(auto_now_add=True)
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                 1, message='Время приготовления не может быть меньше 1 минуты!'
            ),
            MaxValueValidator(
                 240, message='Время приготовления не может превышать 4 часа!'
            ),
        ],
        default=1,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

class BaseFavorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(class)ss'
    )

    class Meta:
        abstract = True

class Favorite(BaseFavorite):
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite',
            ),
        ]

class ShoppingCart(BaseFavorite):
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        ]
