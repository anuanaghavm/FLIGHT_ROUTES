from rest_framework import serializers
from .models import Airport, AirportRoute


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class AirportRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirportRoute
        fields = "__all__"

    def validate(self, data):
        parent = data.get("parent")
        position = data.get("position")

        if parent and position:
            # Check if this position already exists for the parent
            existing_route = AirportRoute.objects.filter(
                parent=parent,
                position=position
            )
            # Exclude current instance if updating
            if self.instance:
                existing_route = existing_route.exclude(pk=self.instance.pk)
            
            if existing_route.exists():
                raise serializers.ValidationError(
                    f"This position ({position}) already exists for parent airport '{parent.name}'"
                )

        return data
