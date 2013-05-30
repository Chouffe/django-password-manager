from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import HttpResponse
from manager.models import Entry, CryptoEngine
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


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_search(request):

    engine = CryptoEngine(master_key=request.user.password)

    entries = None
    if 'title' in request.GET:
        search = str(request.GET['title'])
        entries = Entry.objects.filter(title__contains=search)
    else:
        entries = Entry.objects.all()

    # Decrypts the passwords
    for e in entries:
        e.password = engine.decrypt(e.password)

    response_data = [e.dict() for e in entries]
    # print response_data
    return HttpResponse(json.dumps(response_data), content_type="application/json")
