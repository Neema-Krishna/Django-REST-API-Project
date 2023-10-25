from rest_framework import serializers
from watchlist_app.models import Watchlist,StreamPlatform,Review,User


 

class ReviewSerializer(serializers.ModelSerializer):
    user_name=serializers.StringRelatedField(read_only=True)
    watchlist=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        fields='__all__'
        # exclude=['watchlist']

class WatchListSerializer (serializers.ModelSerializer):
    # len_name=serializers.SerializerMethodField()
    # reviews=ReviewSerializer(many=True,read_only=True)
    platform=serializers.CharField(source='platform.name')
    
    class Meta:
        model=Watchlist
        fields="__all__"
        # exclude=['active']
        # fileds=['id','name']
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist1=WatchListSerializer(many=True,read_only=True)
    # watchlist1=serializers.StringRelatedField(many=True)
    # watchlist1=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # watchlist1=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='movie_detail')
    class Meta:
        model=StreamPlatform
        fields='__all__'
    
    # def get_len_name(self,object):
    #     return len(object.name)
        
    # def validate(self,data):
    #     if data['name']==data['description']:
    #         raise serializers.ValidationError('NOT possible')
    #     return data
        
    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is too short")
    #     else:
    #         return value



# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError('Name is too short')

# class MovieSerailizer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField(validators=[name_length])
#     description=serializers.CharField()
#     active=serializers.BooleanField()
    
    
#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)
#     def update(self,instance,validated_data):
#          instance.name=validated_data.get('name',instance.name)
#          instance.description=validated_data.get('description',instance.description)
#          instance.active=validated_data.get('active',instance.active)
#          instance.save()
#          return instance
     
#     #object validation
     
#     def validate(self,data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError('NOT possible')
#         return data
        
    # field validation 
    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is too short")
    #     else:
    #         return value
    
    
    
