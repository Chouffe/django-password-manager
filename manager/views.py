from manager.forms import EntryForm
from django.shortcuts import render
from generator.models import Generator
from manager.models import CryptoEngine, Entry
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


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


class EntryCreate(CreateView):
    model = Entry
    # fields = ['title', 'url', 'username', 'comment', 'expires']
    template_name = 'manager/entry_create.html'
    form_class = EntryForm
    # success_url = todo

    def post(self, request, *args, **kwargs):

        form = EntryForm(request.POST)
        if form.is_valid():
            message = 'Hello World!!!!'
            # send = True
            entry = form.save(commit=False)
            # entry.password = engine.encrypt(Generator(length=25).generate())
            print form.cleaned_data
            entry.password = engine.encrypt(form.cleaned_data['password'])
            entry.save()
            # return render(request, self.success_url, locals())
        else:
            form = EntryForm()
        return render(request, self.template_name, locals())


class EntryUpdate(UpdateView):

    model = Entry
    # fields = ['title', 'url', 'username', 'comment', 'expires']
    template_name = 'manager/entry_update.html'
    form_class = EntryForm
    # FIXME
    success_url = '../../home'


class EntryDelete(DeleteView):
    model = Entry
    context_object_name = 'entry'
    template_name = 'manager/entry_delete.html'
    # FIXME
    success_url = '../../home'
