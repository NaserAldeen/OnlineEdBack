
from .serializers import UserCreateSerializer, UserLoginSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import CustomUser, Item, Branch, Order, TeacherClass, Lesson
from django.contrib.auth.models import User
from .serializers import ItemSerializer, WorkerSerializer, BranchSerializer, OrderSerializer, TeacherClassSerializer, LessonSerializer
from datetime import  datetime


class FetchClasses(APIView):
    def get(self, request):
        classes = TeacherClass.objects.filter(user__user=request.user)

        return Response({"classes": TeacherClassSerializer(classes, many=True).data})


class CreateClass(APIView):
    def post(self, request):
        name = request.data['name']
        description = request.data['description']
        teacher = CustomUser.objects.get(user=request.user)
        classe = TeacherClass.objects.create(user=teacher, name=name, description=description)

        classes = TeacherClass.objects.filter(user=teacher)

        return Response({"classes": TeacherClassSerializer(classes, many=True).data})



class SaveClassName(APIView):
    def post(self, request):
        classe = TeacherClass.objects.get(id=request.data['id'])
        classe.name = request.data['value']
        classe.save()
        classes = TeacherClass.objects.filter(user__user=request.user)

        return Response({"classes": TeacherClassSerializer(classes, many=True).data})




class SaveClassDescription(APIView):
    def post(self, request):
        classe = TeacherClass.objects.get(id=request.data['id'])
        classe.description = request.data['value']
        classe.save()
        classes = TeacherClass.objects.filter(user__user=request.user)

        return Response({"classes": TeacherClassSerializer(classes, many=True).data})


class DeleteClass(APIView):
    def post(self, request):
        classe = TeacherClass.objects.get(id=request.data['id'])
        classe.delete()
        classes = TeacherClass.objects.filter(user__user=request.user)

        return Response({"classes": TeacherClassSerializer(classes, many=True).data})


class FetchLessonsAndUsers(APIView):
    def post(self, request):
        class_id = request.data['class_id']
        classe = TeacherClass.objects.get(id=class_id)
        lessons = Lesson.objects.filter(teacher_class=classe).order_by("sort_order")
        users = classe.students.all()

        return Response({"lessons": LessonSerializer(lessons, many=True).data, "students": WorkerSerializer(users, many=True).data})

class CreateLesson(APIView):
    def post(self, request):
        classe = TeacherClass.objects.get(id=request.data['class_id'])
        lesson = Lesson.objects.create(teacher_class=classe, name=request.data['name'], description=request.data['description'], sort_order=int(request.data['sort_order']))

        return Response()
        
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        serializer.save()
        print(self.request.data)
        userType = self.request.data['type']
        user = User.objects.get(username=self.request.data['username'])


        custom_user = CustomUser.objects.create(user=user, type=userType, name=self.request.data['name'])


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        my_data = request.data
        serializer = UserLoginSerializer(data=my_data)
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            print(my_data)
            print(request.user)
            if request.data['type'] == "student":
                user =  CustomUser.objects.filter(user__username=request.data['username'], type="student")
                if user.exists():
                    valid_data = serializer.data
                    valid_data['type'] = "student"
                else:
                    return Response({"-": "You are not allowed to enter"}, HTTP_400_BAD_REQUEST)

            elif request.data['type'] == "teacher":
                user =  CustomUser.objects.filter(user__username=request.data['username'], type="teacher")
                if user.exists():
                    valid_data = serializer.data
                    valid_data['type'] = "teacher"
                else:
                    return Response({"-": "You are not allowed to enter"}, HTTP_400_BAD_REQUEST)


            else:
                valid_data['type'] = ""

            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)




class FetchItems(APIView):

    def get(self, request):
        items = Item.objects.all()
        return Response({"items":ItemSerializer(items, many=True).data})

class AddItem(APIView):

    def post(self, request):
        item = Item.objects.create(name=request.data['name'], inventory=int(request.data['inventory']))
        items = Item.objects.all()
        return Response({"items":ItemSerializer(items, many=True).data})


class DeleteItem(APIView):

    def post(self, request):
        item = Item.objects.get(id=request.data['id'])
        item.delete()
        items = Item.objects.all()
        return Response({"items":ItemSerializer(items, many=True).data})


class SaveInventory(APIView):
    def post(self, request):
        custom_user = CustomUser.objects.get(user=request.user)
        if custom_user.type == "admin":
            item = Item.objects.get(id=request.data['id'])
            item.inventory = int(request.data['value'])
            item.save()
        elif custom_user.type == "worker":
            item = Item.objects.get(id=request.data['id'])
            username = request.user.username

            date = datetime.now().date()
            time = datetime.now().time()

            item.log =  str(item.log) + "- "+ username + " changed inventory from "+ str(item.inventory) +" to "+ str(request.data['value'])+" at " + str(date) + str(time)+ "\n"

            item.inventory = int(request.data['value'])

            item.save()
        items = Item.objects.all()
        return Response({"items":ItemSerializer(items, many=True).data})


class SaveName(APIView):
    def post(self, request):
        item = Item.objects.get(id=request.data['id'])
        item.name = request.data['value']
        item.save()
        items = Item.objects.all()
        return Response({"items":ItemSerializer(items, many=True).data})


class FetchWorkers(APIView):
    def get(self, request):
        branch = CustomUser.objects.get(user=request.user).branch
        workers = CustomUser.objects.filter(branch=branch, type="worker")
        orders  = Order.objects.filter(branch=branch)
        return Response({"workers":WorkerSerializer(workers, many=True).data,
                        "orders": OrderSerializer(orders, many=True).data})

class FetchOrders(APIView):
    def get(self, request):
        branch = CustomUser.objects.get(user=request.user).branch
        orders  = Order.objects.filter(branch=branch).order_by("-created")
        return Response({"orders": OrderSerializer(orders, many=True).data})


class FetchHistory(APIView):
    def get(self, request):
        user = CustomUser.objects.get(user=request.user)
        orders  = Order.objects.filter(customer=user).order_by("-created")
        print(orders)
        return Response({"orders": OrderSerializer(orders, many=True).data})

class FetchCustomerHistory(APIView):
    def post(self, request):
        user = CustomUser.objects.get(id=request.data['customer'])
        orders  = Order.objects.filter(customer=user).order_by("-created")
        print(orders)
        return Response({"orders": OrderSerializer(orders, many=True).data})

class ChangeOrderStatus(APIView):
    def post(self, request):
        order  = Order.objects.get(id=request.data['id'])
        order.status = request.data['status']
        order.save()
        return Response()



class FetchBranches(APIView):
    def get(self, request):
        branches = Branch.objects.all()
        return Response({"branches":BranchSerializer(branches, many=True).data})



class PlaceOrder(APIView):
    def post(self, request):
        print(request.data)
        branch = Branch.objects.get(id=request.data['branch'])
        user = CustomUser.objects.get(user=request.user)
        cart = request.data['cart']
        address = request.data['address']
        total = request.data['total']
        is_delivery = request.data['is_delivery']
        expected = request.data['expected']

        if not is_delivery:
            address = ""
        order = Order.objects.create(customer=user, branch=branch, items=cart, address=address, total=total, is_delivery=is_delivery, expected=expected)

        return Response()
