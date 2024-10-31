from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Room
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        # Build the absolute URL for the image field
        if instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation
