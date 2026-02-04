from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AirportRoute(models.Model):
    """
    Represents a route between two airports with a direction (Left/Right) and duration.
    Each parent airport can have at most one left child and one right child.
    """
    LEFT = "L"
    RIGHT = "R"

    POSITION_CHOICES = (
        (LEFT, "Left"),
        (RIGHT, "Right"),
    )
    parent = models.ForeignKey(
        Airport,
        related_name="children",
        on_delete=models.CASCADE,
        help_text="The starting airport node"
    )
    child = models.ForeignKey(
        Airport,
        related_name="parent_routes",
        on_delete=models.CASCADE,
        help_text="The destination airport node"
    )
    position = models.CharField(
        max_length=1,
        choices=POSITION_CHOICES,
        help_text="Direction: Left or Right"
    )
    duration = models.PositiveIntegerField(
        help_text="Time taken to reach this airport (in minutes)"
    )

    class Meta:
        unique_together = ("parent", "position")
        verbose_name = "Airport Route"
        verbose_name_plural = "Airport Routes"
        ordering = ["parent", "position"]

    def __str__(self):
        return f"{self.parent} → {self.child} ({self.get_position_display()})"
