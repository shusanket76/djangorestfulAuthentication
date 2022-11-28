from rest_framework import serializers
from .utils import Util
from .models import User
from .models import Susa
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ["email", "name","password", "password2", "tc"]
        extra_kwargs = {
            'password':{'write_only': True}
        }
    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password!=password2:
            raise serializers.ValidationError("PASSWORDS DOESNOT MATCHES")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model=User
        fields = ["email", 'password']
        
class SusaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Susa
        fields = ['title']
        
class UserResetPasswordEmailSerializers(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        fields = ['email']
        
    def validate(self, attrs):
        email = attrs.get("email")
        
        
        if  User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = "http://localhost:3000/api/user/reset/"+uid+"/"+token
            # print(link)
            data = {
                "subject":"RESET YOUR PASSWORD",
                "body":"CLICK ON THE LINK TO RESET YOUR PASSWORD. THE LINK IS VALID UNTIL 15 MINUTES." + link,
                "toemail":user.email
                
            }
            Util.send_email(data=data)
            return attrs
        else:
            raise serializers.ValidationError("THE EMAIL ADDRESS DOESNOT EXISTS PLEASE CREATE AN ACCOUNT")


class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input-type":"password"}, write_only=True)
    password2 = serializers.CharField(style={"input-type":"password"}, write_only=True)
    
    class Meta:
        fields = ["password", "password2"]
        
    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        uid = self.context.get("uid")
        token = self.context.get("token")
        if password!=password2:
            raise serializers.ValidationError("PASSWORD DOESNOT MATCHES TO EACH OTHER")
        userid = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id = userid)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("THE LINK EXPIRED")    
        user.set_password(password)
        user.save()
        return attrs   