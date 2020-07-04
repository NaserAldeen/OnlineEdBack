from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Item, CustomUser, Branch, Order, TeacherClass, Lesson

class TeacherClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherClass
        fields = "__all__"

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class BranchSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Branch
        fields="__all__"

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    class  Meta:
        model = Order
        fields="__all__"

    def get_customer(self, obj):
        return WorkerSerializer(obj.customer).data


class ItemSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Item
        fields="__all__"

class WorkerSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class  Meta:
        model = CustomUser
        fields= "__all__"

    def get_username(self, obj):
        return obj.user.username


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(allow_blank=True, read_only=True)
    def validate(self, data):
        my_username = data.get('username')
        my_password = data.get('password')
        user_obj = None
        try:
            user_obj = User.objects.get(username=my_username)
        except:
            raise serializers.ValidationError("This email does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError("Incorrect email/password combination")
        payload = RefreshToken.for_user(user_obj)
        token = str(payload.access_token)

        data["access"] = token
        data['username'] = my_username
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data
