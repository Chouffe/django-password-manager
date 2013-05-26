from manager.forms import EntryForm
from django.shortcuts import render
from generator.models import Generator
from manager.models import CryptoEngine, Entry
from django.views.generic import DetailView


engine = CryptoEngine(master_key='testofanewawesomekey')


def entry(request):

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            message = 'Success'
            send = True
            entry = form.save(commit=False)
            entry.password = engine.encrypt(Generator(length=25).generate())
            entry.save()
    else:
        form = EntryForm()

    return render(request, 'entry.html', locals())


class EntryDetailView(DetailView):
    model = Entry
    context_object_name = 'entry'
    template_name = 'manager/entry_get.html'

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        # print context
        # print context['entry'].__dict__
        context['decrypted_password'] = engine.decrypt(
            context['entry'].password)
        return context
