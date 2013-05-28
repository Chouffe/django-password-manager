from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from manager.models import Entry
import json


# @login_required
def get_entries(request):

    entries = Entry.objects.all()
    response_data = [e.title for e in entries]
    return HttpResponse(json.dumps(response_data), content_type="application/json")
