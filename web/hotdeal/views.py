from django.shortcuts import render
from .models import Deal
# Create your views here.

def index(requets):
    deals = Deal.objects.all().order_by("-created_at")
    return render(requets, "index.html", {"deals": deals})