from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()

            username = new_user.username
            password = request.POST.get('password1')

            authenticated_user = authenticate(
                request,
                username=username,
                password=password
            )

            if authenticated_user is not None:
                login(request, authenticated_user)
                return HttpResponseRedirect(reverse('index'))

            # fallback seguro
            return HttpResponseRedirect(reverse('login'))

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                error = "Usuário ou senha inválidos"
        else:
            error = "Preencha todos os campos"

    return render(request, 'users/login.html', {'error': error})