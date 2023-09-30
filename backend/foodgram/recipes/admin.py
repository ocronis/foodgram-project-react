from django.contrib import admin

from recipes.models import (
    Favorite,
    Ingredient,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag,
)


class RecipeIngredientInline(admin.StackedInline):
    model = Ingredient
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'ingredients_list', 'favorite_count',)
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('favorite_count',)
    inlines = [RecipeIngredientInline]
    prepopulated_fields = {"tags": ("name",)}

    def ingredients_list(self, obj):
        ingredients = obj.ingredients_amount.values_list('ingredient__name',
                                                         flat=True)
        return ', '.join(ingredients)

    @admin.display(description='Количество избранного')
    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
