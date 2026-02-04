from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.db.models import Max, Min
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Airport, AirportRoute
from .serializers import AirportSerializer, AirportRouteSerializer
from .forms import AirportRouteForm, SearchForm


class AirportCreate(APIView):

    def post(self, request):
        serializer = AirportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class AirportRouteCreate(APIView):

    def post(self, request):
        serializer = AirportRouteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class TraverseRoute(APIView):
    """
    API endpoint for Task 1: Find the Last Reachable Airport Node
    """
    def get(self, request):
        start = request.GET.get("airport")
        direction = request.GET.get("direction")
        
        if not start or not direction:
            return Response(
                {"error": "airport and direction parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            airport = Airport.objects.get(id=start)
        except Airport.DoesNotExist:
            return Response(
                {"error": "Airport not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if direction not in [AirportRoute.LEFT, AirportRoute.RIGHT]:
            return Response(
                {"error": "Direction must be 'L' (Left) or 'R' (Right)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Traverse continuously in the selected direction
        while True:
            route = AirportRoute.objects.filter(
                parent=airport,
                position=direction
            ).first()

            if not route:
                break

            airport = route.child

        return Response({
            "last_reachable_airport": airport.name,
            "airport_id": airport.id
        })


class LongestDuration(APIView):
    """
    API endpoint for Task 2: Find the Airport with the Longest Duration
    """
    def get(self, request):
        route = AirportRoute.objects.order_by("-duration").first()
        
        if not route:
            return Response(
                {"error": "No routes found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "airport": route.child.name,
            "airport_id": route.child.id,
            "duration": route.duration,
            "route": f"{route.parent.name} → {route.child.name}"
        })



class ShortestDuration(APIView):
    """
    API endpoint for Task 3: Find the Airport with the Shortest Duration Across the Entire Route
    """
    def get(self, request):
        route = AirportRoute.objects.order_by("duration").first()
        
        if not route:
            return Response(
                {"error": "No routes found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "airport": route.child.name,
            "airport_id": route.child.id,
            "duration": route.duration,
            "route": f"{route.parent.name} → {route.child.name}"
        })


# Template-based views for Django forms

class AddRouteView(FormView):
    """
    Template view for adding an Airport Route (Core Requirement)
    """
    template_name = 'airport/add_route.html'
    form_class = AirportRouteForm
    success_url = '/airport/add-route/'

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            f"Route added successfully: {form.instance.parent.name} → "
            f"{form.instance.child.name} ({form.instance.get_position_display()})"
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = AirportRoute.objects.select_related(
            'parent', 'child'
        ).all()[:10]  # Show recent routes
        return context


class SearchRouteView(FormView):
    """
    Template view for Task 1: Find the Last Reachable Airport Node
    """
    template_name = 'airport/search_route.html'
    form_class = SearchForm

    def form_valid(self, form):
        airport = form.cleaned_data['airport']
        direction = form.cleaned_data['direction']
        
        # Traverse continuously in the selected direction
        current_airport = airport
        path = [current_airport.name]
        
        while True:
            route = AirportRoute.objects.filter(
                parent=current_airport,
                position=direction
            ).select_related('child').first()

            if not route:
                break

            current_airport = route.child
            path.append(current_airport.name)

        return render(self.request, self.template_name, {
            'form': self.form_class(),
            'last_airport': current_airport,
            'path': path,
            'direction': direction,
            'direction_display': dict(AirportRoute.POSITION_CHOICES)[direction]
        })


class LongestDurationView(TemplateView):
    """
    Template view for Task 2: Find the Airport with the Longest Duration
    """
    template_name = 'airport/longest_duration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        route = AirportRoute.objects.select_related(
            'parent', 'child'
        ).order_by("-duration").first()
        
        if route:
            context['route'] = route
            context['airport'] = route.child
            context['duration'] = route.duration
        else:
            context['error'] = "No routes found"
        
        return context


class ShortestDurationView(TemplateView):
    """
    Template view for Task 3: Find the Airport with the Shortest Duration Across the Entire Route
    """
    template_name = 'airport/shortest_duration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        route = AirportRoute.objects.select_related(
            'parent', 'child'
        ).order_by("duration").first()
        
        if route:
            context['route'] = route
            context['airport'] = route.child
            context['duration'] = route.duration
        else:
            context['error'] = "No routes found"
        
        return context


class HomeView(TemplateView):
    """
    Home page with navigation to all features
    """
    template_name = 'airport/home.html'
