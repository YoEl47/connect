from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from.forms import *
from .models import *
from django.contrib import messages,auth
from .import *
# Create your views here.

def dashboard(req):
    return render(req, "dashboard/index.html")


def reg(req):
    if req.method== "POST":
       
            form = RegisterStudentForm(req.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
    else:
        form = RegisterStudentForm()
    context={
        'form':form
    }
    return render(req,'dashboard/register.html',context)


def login(request):
    print("in the method")
    if request.method=='POST':
        print("in the post")

        email = request.POST['email']
        p = request.POST['password']
       # user= auth.authenticate(email= email, password = p)
        user=email
        print(user)

        if user is not None:
            print("user found")
          
            u=''
            
          
            if str(u) == 'Instructor':
                print(user.instructor_course)
                return redirect('instructorHome')
            elif u == '':
                return redirect('home')
            elif str(u) == 'Student':
                return redirect('getMessage')
            elif str(u)=="college Registrar":
                return redirect('register_course')
        else:
            messages.error(request, 'wrong username or password')
    context={
        "form": LoginiForm()
    }
    return render(request,'dashboard/index.html',context)

@login_required()
def logout(request):
    auth.logout(request)
    return redirect('login')

from rest_framework.views import *
from .serializzers import *

class GetSavedAnnouncements(APIView):

    def post(self, request, format=None):
        serializer = UserAnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.generics import RetrieveAPIView

class GetUserInfo(RetrieveAPIView):
    queryset = users.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


from collageRegistrar.serializers import *
from collageRegistrar.models import Announcement 
class SavedAnnouncementApi(APIView):
    def get(self, request,pk):
        my_objects = savedAnnouncements.objects.filter(user=pk).order_by("-id")

        
        serializer = UserAnnouncementSerializer(my_objects, many=True)

        # Return the serialized data
        return Response(serializer.data)
class DeleteUserSavedMessages(APIView):
    def get(self, req,pk,pk2,*args,**kwargs):
        mes= savedAnnouncements.objects.filter(user= pk, announcement = pk2).first()
        mes.delete()
        
        return Response({"message":"deleted successfully"})


class ChangePassword(APIView):
    pass
    def post(self, req,*args,**kwargs):
        pass

from rest_framework.parsers import MultiPartParser, FormParser

class UserProfileUpdateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.userprofile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserProfileUpdateSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user_serializer = UserProfileSerializer(instance.user)
            return Response(user_serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)