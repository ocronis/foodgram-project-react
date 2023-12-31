from .models import Follow
from django.contrib import admin
from django.contrib.auth import models as auth_models
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email',)
    list_display = ('username', 'email', 'recipe_count', 'follower_count',)

    def recipe_count(self, obj):
        return obj.recipes.count()

    def follower_count(self, obj):
        return obj.follower.count()

    recipe_count.short_description = 'Количество рецептов'
    follower_count.short_description = 'Количество подписчиков'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.unregister(auth_models.Group)
