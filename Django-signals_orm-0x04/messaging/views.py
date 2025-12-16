from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def delete_user(request):
    request.user.delete()
    return redirect('login')
