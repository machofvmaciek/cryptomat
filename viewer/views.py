"""Module gathering views for viewer app."""

# from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    """Index page of viewer."""
    return HttpResponse("Welcome to cryptomat's viewer!")
