from django.urls import path
from .views import *

# Template-based URLs (for Django forms and templates)
urlpatterns = [
    # Home page
    path("", HomeView.as_view(), name="home"),
    
    # Core Requirement: Add Airport Route Form
    path("add-route/", AddRouteView.as_view(), name="add_route"),
    
    # Task 1: Search Route Form
    path("search-route/", SearchRouteView.as_view(), name="search_route"),
    
    # Task 2: Longest Duration
    path("longest-duration/", LongestDurationView.as_view(), name="longest_duration"),
    
    # Task 3: Shortest Duration
    path("shortest-duration/", ShortestDurationView.as_view(), name="shortest_duration"),
    
    # API endpoints (for REST API access)
    path("api/airport/", AirportCreate.as_view(), name="api_airport_create"),
    path("api/route/", AirportRouteCreate.as_view(), name="api_route_create"),
    path("api/traverse/", TraverseRoute.as_view(), name="api_traverse"),
    path("api/longest/", LongestDuration.as_view(), name="api_longest"),
    path("api/shortest/", ShortestDuration.as_view(), name="api_shortest"),
]
