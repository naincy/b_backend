from rest_framework import serializers

"""
Serializer for Course Class Object
"""
class CourseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
