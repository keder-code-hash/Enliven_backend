from rest_framework import serializers
from .models import Register

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model=Register
        fields=['user_name','first_name','last_name','bio','interests','email','ph_no','date_of_birth','password','is_admin','is_staff']

##write_only fiend are not shown for read purpose

class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model=Register
        fields=['user_name','first_name','last_name','bio','interests','email','ph_no','date_of_birth','password']  
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self,validated_data):
        customUser=Register.objects.create_user(validated_data['email'],validated_data['user_name']
            ,validated_data['last_name'],validated_data['first_name'],validated_data['password'])
        return customUser

class RegisterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Register
        fields=['user_name','first_name','last_name','bio','interests','ph_no','date_of_birth','profile_pic_name']
    def update(self, instance, validated_data):
        instance.user_name=validated_data.get('user_name',instance.user_name)
        instance.first_name=validated_data.get('first_name',instance.first_name)
        instance.last_name=validated_data.get('last_name',instance.last_name)
        instance.date_of_birth=validated_data.get('date_of_birth',instance.date_of_birth)
        instance.interests=validated_data.get('interests',instance.interests)
        instance.bio=validated_data.get('bio',instance.bio)
        instance.ph_no=validated_data.get('ph_no',instance.ph_no)
        instance.save()
        return instance