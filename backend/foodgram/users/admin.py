from django.contrib import admin
from django.contrib.auth import get_user_model, models

User = get_user_model()

# Определение класса UserAdmin для административного интерфейса пользователя
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email',)

# Отключение регистрации модели Group в административном интерфейсе
admin.site.unregister(models.Group)

