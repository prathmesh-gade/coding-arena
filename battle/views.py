from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import json
import sys
import io


# =========================
# HOME PAGE
# =========================

def home(request):
    return render(request, "home.html")


# =========================
# CREATE ROOM
# =========================

def create_room(request):
    room_id = str(uuid.uuid4())[:8]
    return redirect(f"/room/{room_id}/")


# =========================
# EDITOR PAGE
# =========================

def editor(request, room):

    username = "User_" + str(uuid.uuid4())[:4]

    return render(request, "editor.html", {
        "room": room,
        "username": username
    })


# =========================
# RUN CODE
# =========================

@csrf_exempt
def run_code(request):

    if request.method == "POST":

        data = json.loads(request.body)
        code = data.get("code", "")

        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()

        try:
            exec(code, {})
            output = mystdout.getvalue()
        except Exception as e:
            output = str(e)

        sys.stdout = old_stdout

        return JsonResponse({
            "result": output
        })
