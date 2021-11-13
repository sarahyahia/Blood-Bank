from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

def check_user(user):
    return not user.is_authenticated


user_logout_required = user_passes_test(check_user, 'profile', None)


def auth_user_should_not_access(viewfunc):
    return user_logout_required(viewfunc)



def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)



class NotAuthenticatedMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated