# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.views.generic import FormView,DetailView,DeleteView,ListView,UpdateView,CreateView
from django.contrib.auth.models import User
from permission.forms import RegisterForm,PermissionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from permission.models import Permission
from django.utils.translation import ugettext, ugettext_lazy as _

class UserRegister(LoginRequiredMixin,FormView):
    template_name = 'permission/userregister.html'
    form_class = RegisterForm
    success_url = reverse_lazy('userlist')

    def form_valid(self, form):
        username=form.cleaned_data['user']
        password=form.cleaned_data['newpassword1']
        email=form.cleaned_data['email']
        User.objects.create_user(username=username,email=email,password=password,is_active=False)
        return HttpResponseRedirect(self.get_success_url())

class UserList(LoginRequiredMixin,ListView):
    template_name='permission/userlist.html'
    model=User

class UserDelete(LoginRequiredMixin,DeleteView):
    template_name='permission/userdelete.html'
    model=User
    success_url = reverse_lazy('userlist')

class UserUpdate(LoginRequiredMixin,UpdateView):
    template_name='permission/userupdate.html'
    model=User
    fields=['email']
    success_url = reverse_lazy('userlist')


class PermissionCreate(LoginRequiredMixin,CreateView):
    model = Permission
    form_class = PermissionForm
    success_url = reverse_lazy('permissionlist')
    template_name = 'permission/permissioncreate.html'
    
    def get_context_data(self, **kwargs):
        context = super(PermissionCreate, self).get_context_data(**kwargs)
        context['title'] = _('Create Permission')
        return context

    def form_valid(self, form):
        user = form.cleaned_data['user']
        permissionset = form.cleaned_data['permissions']
        for permission in user.user_permissions.all():
            user.user_permissions.remove(permission)
            user.save()
        for permission in permissionset:
            user.user_permissions.add(permission)
            user.save()
        self.object = form.save()
        return super(PermissionCreate, self).form_valid(form)

class PermissionList(LoginRequiredMixin,ListView):
    model = Permission
    template_name = 'permission/permissionlist.html'

class PermissionUpdate(LoginRequiredMixin,UpdateView):
    model = Permission
    form_class = PermissionForm
    success_url = reverse_lazy('permissionlist')
    template_name = 'permission/permissioncreate.html'
    
    def get_context_data(self, **kwargs):
        context = super(PermissionUpdate, self).get_context_data(**kwargs)
        context['title'] = _('Update Permission')
        return context

    def form_valid(self, form):
        user = form.cleaned_data['user']
        permissionset = form.cleaned_data['permissions']
        for permission in user.user_permissions.all():
            user.user_permissions.remove(permission)
            user.save()
        for permission in permissionset:
            user.user_permissions.add(permission)
            user.save()
        self.object = form.save()
        return super(PermissionUpdate, self).form_valid(form)

class PermissionDelete(LoginRequiredMixin,DeleteView):
    model = Permission
    success_url = reverse_lazy('permissionlist')
    template_name = 'permission/permissiondelete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        user = self.object.user
        permissionset = self.object.permissions.all()
        for permission in permissionset:
            user.user_permissions.remove(permission)
            user.save()
        self.object.delete()
        return HttpResponseRedirect(success_url)