from .models import ExtendedUser


def extra_field_processor(request):
    if request.user.is_authenticated:
        ext_user = ExtendedUser.objects.get(user=request.user)
        return {'ext_user': ext_user}
    return {}
