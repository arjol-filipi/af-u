from rest_framework import serializers
from ..models import Artikull

class ArticleSerializer(serializers.ModelSerializer):
    class Meta():
        model = Artikull
        fields = '__all__'
