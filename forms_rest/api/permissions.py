import rest_framework.permissions

import api.models


class IsOwnerOrReadonly(rest_framework.permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in rest_framework.permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner


class IsFormOwnerOrReadonly(rest_framework.permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in rest_framework.permissions.SAFE_METHODS:
            return True
        if not request.data:
            return True
        form = api.models.Form.objects.get(pk=request.data['form'])
        return request.user == form.owner
        
    def has_object_permission(self, request, view, obj):
        if request.method in rest_framework.permissions.SAFE_METHODS:
            return True
        
        return request.user == obj.form.owner