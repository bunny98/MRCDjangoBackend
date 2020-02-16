from .models import FileTable
from rest_framework import serializers

class FileNamesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileTable
        fields = ['file']

