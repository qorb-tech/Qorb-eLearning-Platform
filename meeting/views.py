import json
import random
import time

from agora_token_builder import RtcTokenBuilder
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .accounts.decorators import allow_user

# Local imports goes here
from .models import RoomMember


# Create your views here.
@login_required(login_url="login_view")
@allow_user(["is_teacher", "is_student"])
def lobby(request, name):
    room_name = name
    user_name = request.user
    context = {"room_name": room_name, "user_name": user_name}
    return render(request, "base/lobby.html", context)


def room(request):
    return render(request, "base/room.html")


def getToken(request):
    appId = "ea8afd3db07a44eeb9878e48c8295ea6"
    appCertificate = "064e5d3b00404057881f77bd81e3e2f9"
    channelName = request.GET.get("channel")
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    # if request.user.is_teacher:
    #     role = 1
    # elif request.user.is_student:
    #     role = 2

    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs
    )

    return JsonResponse({"token": token, "uid": uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data["name"], uid=data["UID"], room_name=data["room_name"]
    )

    return JsonResponse({"name": data["name"]}, safe=False)


def getMember(request):
    uid = request.GET.get("UID")
    room_name = request.GET.get("room_name")

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({"name": member.name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data["name"], uid=data["UID"], room_name=data["room_name"]
    )
    member.delete()
    return JsonResponse("Member deleted", safe=False)
