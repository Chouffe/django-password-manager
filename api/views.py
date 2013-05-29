from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import HttpResponse
from manager.models import Entry
from generator.models import Generator
import json


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_entries(request):

    entries = Entry.objects.all()
    response_data = [e.title.capitalize() for e in entries]
    response_data.sort()
    response_data = list(set(response_data))
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_random_key(request):

    generator = Generator()
    if 'length' in request.GET:
        length = int(request.GET['length'])
        generator.length = length

    response_data = generator.generate()
    return HttpResponse(json.dumps(response_data), content_type="application/json")
