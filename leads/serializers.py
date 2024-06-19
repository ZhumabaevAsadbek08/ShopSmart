from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import *
from .validators import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"