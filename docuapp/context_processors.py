from .models import Office

def user_groups_processor(request):
    return {
        'is_admin': request.user.groups.filter(name='uAdmin').exists(),
        'is_query': request.user.groups.filter(name='uQuery').exists(),
        'is_mpmtc': request.user.groups.filter(name='mpmtc').exists(),
    }

def user_offices_by_group(request):
    if request.user.is_authenticated:
        user_groups = request.user.groups.all()
        offices = Office.objects.filter(groups__in=user_groups).distinct()
        return {'user_offices': offices}
    return {'user_offices': []}