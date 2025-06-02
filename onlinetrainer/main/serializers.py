from django.contrib.auth.models import User
from rest_framework import serializers
import re
from rest_framework.validators import UniqueValidator


class CustomRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Користувач з таким email вже існує.")
        ]
    )

    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Користувач з таким ім’ям вже існує.")
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Тільки @gmail.com дозволено.")
        return value

    def validate_password(self, value):
        # Перевірка на мінімальну довжину
        if len(value) < 8:
            raise serializers.ValidationError("Пароль має містити не менше 8 символів.")

        # Перевірка на наявність цифр
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Пароль має містити хоча б одну цифру.")

        # Перевірка на наявність великих літер
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Пароль має містити хоча б одну велику літеру.")

        # Перевірка на наявність спеціальних символів
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Пароль має містити хоча б один спеціальний символ.")

        return value

    def create(self, validated_data):
        # Створення користувача
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .utils import send_confirmation_email  # Місце для функції відправки листа


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password)

        # Відправка листа з підтвердженням
        send_confirmation_email(user, request)

        return redirect('registration_success')  # Страница після успішної реєстрації

    return render(request, 'register.html')


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Додай email до відповіді
        data['email'] = self.user.email

        return data
