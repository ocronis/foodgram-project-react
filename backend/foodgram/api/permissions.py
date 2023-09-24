from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    message = 'Вы не можете изменять или удалять контент, созданный другими пользователями.'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author)
