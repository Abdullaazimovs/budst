from django.urls import path

from base.views import (
                        home,
                        room,
                        create_room,
                        updateRoom,
                        deleteRoom,
                        loginPage,
                        logoutUser,
                        registerPage,
                        deleteMessage,
                        userProfile,
                    )


urlpatterns = [
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('register/', registerPage, name="register"),

    path('', home, name="home"),
    path('room/<int:pk>/', room, name='room'),
    path('profile/<str:pk>/', userProfile, name="user-profile"),

    path('create-room/', create_room, name='create-room'),
    path('update-room/<int:pk>/', updateRoom, name='update-room'),
    path('delete-room/<int:pk>/', deleteRoom, name='delete-room'),

    path('delete-message/<int:pk>/', deleteMessage, name='delete-message'),
]
