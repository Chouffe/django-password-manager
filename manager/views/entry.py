from manager.forms import EntryForm
from django.shortcuts import render
from manager.models import CryptoEngine, Entry
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


engine = CryptoEngine(master_key='testofanewawesomekey')


class EntryDetailView(DetailView):
    """ Details about a given entry """

    model = Entry
    context_object_name = 'entry'
    template_name = 'manager/entry_get.html'

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        context['decrypted_password'] = engine.decrypt(
            context['entry'].password)
        return context


class EntryCreate(CreateView):
    """ Enables creation of new entries """

    model = Entry
    template_name = 'manager/entry_create.html'
    form_class = EntryForm
    # success_url = todo

    def post(self, request, *args, **kwargs):

        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.password = engine.encrypt(form.cleaned_data['password'])
            entry.save()
            # return render(request, self.success_url, locals())
        else:
            form = EntryForm()
        return render(request, self.template_name, locals())


class EntryUpdate(UpdateView):
    """ Enables update of a given entry """

    model = Entry
    template_name = 'manager/entry_update.html'
    form_class = EntryForm
    # FIXME
    success_url = '../../home'


class EntryDelete(DeleteView):
    """ Enables deletion of a given entry """

    model = Entry
    context_object_name = 'entry'
    template_name = 'manager/entry_delete.html'
    # FIXME
    success_url = '../../home'
