from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)
from applications.security.forms.user import UserForm
from applications.security.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class UserListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/users/list.html'
    model = User
    context_object_name = 'users'
    permission_required = 'view_user'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        queryset = self.model.objects.all().order_by('id')
        if q1:
            queryset = queryset.filter(
                Q(username__icontains=q1) |
                Q(first_name__icontains=q1) |
                Q(last_name__icontains=q1) |
                Q(dni__icontains=q1) |
                Q(email__icontains=q1)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:user_create')
        # Si quieres ver permisos en consola, sino elimina el print
        print(context.get('permissions'))
        return context


class UserCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = User
    template_name = 'security/users/form.html'
    form_class = UserForm
    success_url = reverse_lazy('security:user_list')
    permission_required = 'add_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar User'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        form.save_m2m()  
        
        messages.success(self.request, f"Éxito al crear el usuario con DNI {user.dni or 'N/A'}.")
        return super().form_valid(form)



class UserUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = User
    template_name = 'security/users/form.html'
    form_class = UserForm
    success_url = reverse_lazy('security:user_list')
    permission_required = 'change_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar User'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        messages.success(self.request, f"Éxito al actualizar el usuario {user.username}.")
        return response


class UserDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = User
    template_name = 'core/delete.html'
    success_url = reverse_lazy('security:user_list')
    permission_required = 'delete_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar User'
        context['description'] = f"¿Desea eliminar el usuario: {self.object.username}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        user_name = self.object.username
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar lógicamente el usuario {user_name}.")
        return response
