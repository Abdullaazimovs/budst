from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from base.models import Room, Topic, Message
from .forms import RoomForm


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, 'base/login_register.html', context={'form': form})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "USER NOT EXISTS")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR password does not exist")

    context = {
        "page": page,
    }
    return render(request, 'base/login_register.html', context=context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    count_room = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        "rooms": rooms,
        "topics": topics,
        "count_room": count_room,
        "room_messages": room_messages,
    }

    return render(request, 'base/home.html', context=context)


def room(request, pk):
    rooms = Room.objects.get(id=pk)
    room_messages = rooms.message_set.all().order_by('-created')  # many to one
    participants = rooms.participants.all()  # many to many
    if request.method == "POST":
        Message.objects.create(
            user=request.user,
            room=rooms,
            body=request.POST.get('body')
        )
        rooms.participants.add(request.user)
        return redirect('room', pk=rooms.id)
    context = {
        "rooms": rooms,
        "messages": room_messages,
        "participants": participants,
    }
    return render(request, 'base/room.html', context=context)


def userProfile(request, pk):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'base/profile.html', context=context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        # else:

    context = {
        'form': form,
    }
    return render(request, 'base/room_form.html', context=context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You re not allowed here")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'base/room_form.html', context=context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You re not allowed here")
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {"obj": room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You re not allowed here")
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {"obj": message})
