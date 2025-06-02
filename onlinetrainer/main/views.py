import json
import os
import threading

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from .serializers import CustomRegisterSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
import numpy as np
import cv2


#------- add Sam

BASE_DIR = "pythonProject16"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
RAW_DATA_DIR = os.path.join(MEDIA_ROOT, 'row_data')
# Дозволити великі файли
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024
#------- end Sam



def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def profile_p(request):
    return render(request, 'main/profile.html')


def contacts(request):
    return render(request, 'main/contacts.html')


def registration_form(request):
    return render(request, 'main/registration_form.html')


def login(request):
    return render(request, 'main/login.html')


def downloads(request):
    return render(request, 'main/downloads.html')


def exit(request):
    return render(request, 'main/exit.html')


def exercises(request):
    return render(request, 'main/exercises.html')


def ex1(request):
    return render(request, 'main/ex1.html')


def ex2(request):
    return render(request, 'main/ex2.html')


def ex3(request):
    return render(request, 'main/ex3.html')

def chose1(request):
    return render(request, 'main/chose1.html')

def chose2(request):
    return render(request, 'main/chose2.html')

def chose3(request):
    return render(request, 'main/chose3.html')

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = [AllowAny]


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
        })



from .utils import send_confirmation_email

class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_email(user, request)
            return Response({"message": "Реєстрація успішна! Перевірте пошту(Подивітья у розділі спаму)."}, status=201)
        else:
            print(serializer.errors)  # <-- додай це
            return Response({"errors": serializer.errors}, status=400)


from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.urls import reverse

class ActivateUserView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            # Перенаправлення на сторінку успіху
            return HttpResponseRedirect(reverse('activation_success'))
        else:
            return Response({"message": "Недійсне або прострочене посилання."}, status=status.HTTP_400_BAD_REQUEST)


def activation_success(request):
    return render(request, 'main/activation_success.html')

@login_required
def profile(request):
    user = request.user  # поточний залогінений користувач
    return render(request, 'profile.html', {
        'username': user.username,
        'email': user.email,

    })


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@csrf_exempt
def try_mobile_login(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST allowed')

    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
    except Exception as e:
        return HttpResponseBadRequest('Invalid JSON')

    # Проста перевірка (заміни на свою авторизацію!)
    if len(username) > 0 and len(password) > 0:
        # Наприклад, повертаємо token або OK
        # TODO CREATE DIR TO USER
        return JsonResponse({'status': 'ok', 'token': 'test-token'})
    else:
        return JsonResponse({'status': 'error', 'error': 'Invalid credentials'}, status=401)

@csrf_exempt
def get_username_from_token(request):
    token = request.headers.get("token")
    if token and token == 'test-token':  # in SESSIONS:
        username = request.headers.get("mobile-user-name")
        return username  # SESSIONS[token]
    return None


def process_save_yuv_frames(data, yuv_format, username):
    idx = 0
    num_frames = int.from_bytes(data[idx:idx+4], 'big')
    idx += 4

    frames_info = []
    for _ in range(num_frames):
        timestamp = int.from_bytes(data[idx:idx+8], 'big')
        idx += 8
        width = int.from_bytes(data[idx:idx+4], 'big')
        idx += 4
        height = int.from_bytes(data[idx:idx+4], 'big')
        idx += 4
        yuv_len = int.from_bytes(data[idx:idx+4], 'big')
        idx += 4
        yuv_data = data[idx:idx+yuv_len]
        idx += yuv_len

        expected_len = width * height * 3 // 2
        if len(yuv_data) != expected_len:
            frames_info.append({
                "timestamp": timestamp,
                "status": f"YUV size mismatch {len(yuv_data)} != {expected_len}",
            })
            continue

        try:
            yuv = np.frombuffer(yuv_data, dtype=np.uint8)
            yuv = yuv.reshape((height * 3 // 2, width))
            if yuv_format == "NV21":
                rgb_img = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB_NV21)
            elif yuv_format == "YUV420P":
                rgb_img = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB_I420)
            else:
                frames_info.append({
                    "timestamp": timestamp,
                    "status": f"Unknown format: {yuv_format}",
                })
                continue
            user_dir = os.path.join(MEDIA_ROOT, 'frames', username)
            os.makedirs(user_dir, exist_ok=True)
            filename = os.path.join(user_dir, f"{timestamp}.jpg")
            cv2.imwrite(filename, cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR))
            frames_info.append({
                "timestamp": timestamp,
                "status": "saved",
                "path": filename,
            })
        except Exception as e:
            frames_info.append({
                "timestamp": timestamp,
                "status": f"Failed to decode: {e}",
            })
    # Можете зберігати frames_info десь або логувати тут при потребі
def proctssing_raw_frames(frames):
    points_tabel = []
    if len(frames) > 0:
        for i, frame in enumerate(frames):
            pass# points_tabel.append(find_sceleton_point(frame))
        return points_tabel

@csrf_exempt
def upload_raw_data_YUV_frames(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST allowed")

    username = get_username_from_token(request)
    if not username:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    yuv_format = request.headers.get("X-YUV-Format", "NV21").upper()

    try:
        data = request.body
        # запуск обробки у фоні, повертаємо accepted
        threading.Thread(target=process_save_yuv_frames, args=(data, yuv_format, username), daemon=True).start()
        return JsonResponse({"status": "accepted"}, status=202)
    except Exception as e:
        return HttpResponseBadRequest(f"Parsing error: {e}")
