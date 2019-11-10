import json
 
from rest_framework.permissions import BasePermission

"""
Custom Permission Class
"""
class JWTPermission(BasePermission):
    
    def has_permission(self, request, view):
        
        #Add Extra logic

        return True
        
        
