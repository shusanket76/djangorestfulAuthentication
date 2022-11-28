from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, SusaSerializer, UserResetPasswordEmailSerializers, UserPasswordResetSerializer
from .serializers import UserLoginSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from .models import Susa

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            tokens = get_tokens_for_user(user=user)
            return Response({"tokens":tokens, 'msg':"REGISTRATION SUCCESFULL"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
    
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                tokens = get_tokens_for_user(user=user)
                return Response({"token":tokens, "msg":"LOGIN SUCCESSFULL"}, status=status.HTTP_200_OK)          
        return Response({"errors":{'non_field_errors':["EMAIL OR PASSWORD IS NOT VALID"]}}, status=status.HTTP_406_NOT_ACCEPTABLE)
    

class Blog(APIView):
    def get(self,request,format=None):
        susan = Susa.objects.all()
        serializer = SusaSerializer(susan, many=True)
        
        return Response(serializer.data)
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):

        susan = Susa(user=request.user, title=request.data.get("title"))
        susan.save()
        
        return Response("SAVED")
 

class UserResetPasswordEmail(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = UserResetPasswordEmailSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response("PASSWORD RESET EMAIL SENT TO YOUR EMAIL. PLEASE CHECK YOUR EMAIL")
        
class UserPasswordReset(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self,request,uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={"uid":uid, "token":token})
        if serializer.is_valid():
            return Response("PASSWORD RESET SUCCESFULLY")
        else:
            return Response("ERROR OCCURED")
        