from manager.forms import EntryForm
from django.shortcuts import render

def entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            send = True
    else:
        form = EntryForm()
    return render(request, 'entry.html', locals())
