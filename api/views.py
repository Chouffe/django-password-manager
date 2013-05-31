from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import HttpResponse
from manager.models import Entry, CryptoEngine, Category
from generator.models import Generator
import json
import datetime


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

    elif 'category' in request.GET:
        search = str(request.GET['category'])
        categories = Category.objects.filter(title__contains=search)
        entries = [e for c in categories for e in c.entry_set.all()]

    else:
        entries = Entry.objects.all()

    # Decrypts the passwords
    for e in entries:
        e.password = engine.decrypt(e.password)

    response_data = [e.dict() for e in entries]
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def post_entry_add(request):

    engine = CryptoEngine(master_key=request.user.password)

    e = None
    attributes = set(['title', 'password', 'category'])
    if attributes <= set(request.POST.keys()):

        e = Entry(title=request.POST['title'],
                  password=request.POST['password'])

        for k, v in request.POST.items():
            if k == 'username':
                e.username = v
            elif k == 'url':
                e.url = v
            elif k == 'comment':
                e.comment = v
            elif k == 'expires':
                # date formated: m/d/Y
                e.expires = datetime.datetime.strptime(v, "%m/%d/%Y").date()
            elif k == 'category':
                c = Category.objects.filter(id=int(v))
                if len(c) == 0:
                    return HttpResponse(0)
                else:
                    e.category_id = int(v)
        try:
            e.save()
            return HttpResponse(1)
        except:
            return HttpResponse(0)
    else:
        return HttpResponse(0)
