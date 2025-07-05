from django.http import JsonResponse
from applications.security.models import Module, Menu
from django.contrib.auth.models import Permission

def get_modules_by_menus(request):
    menu_ids = request.GET.get('menus', '')
    menu_ids = menu_ids.split(',') if menu_ids else []
    modules = Module.objects.filter(menu__id__in=menu_ids).distinct()
    modules_data = [{'id': m.id, 'name': m.name} for m in modules]
    return JsonResponse({'modules': modules_data})

def get_permissions_by_module(request):
    module_id = request.GET.get('module_id')
    if module_id:
        permissions = Permission.objects.filter(module__id=module_id)
        permissions_data = [{'id': p.id, 'name': p.name} for p in permissions]
    else:
        permissions_data = []
    return JsonResponse({'permissions': permissions_data})