from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    # for readonly access to the model or object 
    def has_permission(self, request, view):
        print(view.action)
        if view.action  == 'list' : # restricting list view
            return False
        return request.method in permissions.SAFE_METHODS



class IsUser(permissions.BasePermission) :

    ''' Description : IsUser will help us to give permission to the 
                     requested user to access data related to him only '''

    def has_permission(self, request, view):

        return  request.user.is_authenticated and request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):

        return obj.user == request.user


class IsOnBoard(permissions.BasePermission) :
    ''' Description : IsOnBoard will check whether requested user is onboard or not
                  has_permission mehtod will check that  the requested user has that permission or not
                  has_object_permission will check that requested method is safe or not for detailed access   '''
    def has_permission(self, request, view):
        if request.user.is_superuser :
          return True
        return request.user.is_authenticated and request.user.profile.is_onboard 


    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS and (request.user.is_authenticated and request.user.profile.is_onboard)  : # safe method is a tuple containing get ,Options ,Head etc.
          return True
          # safe method is a tuple containing get ,Options ,Head etc.

        return obj.user == request.user  and  (request.user.is_authenticated and request.user.profile.is_onboard)  

