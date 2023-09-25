from django.http import HttpResponse
from django.db.models import Sum


def download_shopping_cart(user):
    ingredients = user.shopping_cart.values(
        'recipe__ingredients_amount__ingredient__name',
        'recipe__ingredients_amount__ingredient__measurement_unit'
    ).annotate(amount=Sum('recipe__ingredients_amount__amount'))
    shopping_list = 'Список покупок:\n'
    count_ingredients = 0
    unit = ('ingr["recipe__ingredients_amount__ingredient"]'
            '["measurement_unit"]')
    for ingr in ingredients:
        count_ingredients += 1
        shopping_list += (
            f'{count_ingredients}) '
            f'{ingr["recipe__ingredients_amount__ingredient__name"]} - '
            f'{ingr["amount"]} '
            f'({unit})\n'
        )
    response = HttpResponse(shopping_list, content_type='text/plain')
    response['Content-Disposition'] = (
        f'attachment; '
        f'filename="{user.username}_shopping_list.txt"'
    )
    return response
