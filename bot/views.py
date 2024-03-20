# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from telegram import Bot, Update
# from telegram.ext import CommandHandler, Dispatcher
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from django.utils import timezone

TELEGRAM_TOKEN = '7190755231:AAFMaoYCCIGDDyEwlIhYIXOr6rasT6I2Bj8'

# @login_required
def home(request):
    # user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    # context = {'user_profile': user_profile}
    return render(request, 'home.html', context)

@login_required
def claim_points(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]

    # Check if it's been 10 minutes since last claim
    if user_profile.last_claimed is None or (timezone.now() - user_profile.last_claimed).total_seconds() >= 600:
        user_profile.points += 1
        user_profile.last_claimed = timezone.now()
        user_profile.save()
        message = "Points claimed successfully!"
    else:
        message = "You can claim points again in 10 minutes."

    context = {'message': message}
    return render(request, 'claim_points.html', context)

def webhook(request):
    if request.method == 'POST':
        bot = Bot(token=TELEGRAM_TOKEN)
        dispatcher = Dispatcher(bot, None)

        update = Update.de_json(request.POST, bot)
        dispatcher.process_update(update)
        return HttpResponse("")

    return HttpResponseNotAllowed(['POST'])



def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
