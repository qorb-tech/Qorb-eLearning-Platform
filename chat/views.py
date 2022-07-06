from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from teacher.models import Course




def room(request, room_name):
    user = request.user.username
    return render(request, 'chat/room.html', {
        'room_name': room_name, 
        'loged_user':user
    })
