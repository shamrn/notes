from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings


def main(request):
    """Main page view"""

    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, template_name='main.html')


@login_required
def main_note(request):
    return render(request, template_name='note/main-note.html')

