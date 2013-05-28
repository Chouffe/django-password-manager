from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from manager.models import Entry
from generator.models import Generator
import json


@login_required
def get_entries(request):

    entries = Entry.objects.all()
    response_data = [e.title for e in entries]
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def get_random_key(request):

    generator = Generator()
    if request.GET['length']:
        length = int(request.GET['length'])
        generator.length = length

    response_data = generator.generate()
    return HttpResponse(json.dumps(response_data), content_type="application/json")
