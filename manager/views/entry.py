from django.contrib.auth.decorators import login_required
import datetime
from django.shortcuts import redirect
from manager.forms import EntryForm
from django.shortcuts import render
from manager.models import CryptoEngine, Entry
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.http import HttpResponse


# engine = None
#
# if engine is not None:
#     if request.user.is_superuser:
#         print 'SuperUser!!!'
#         engine = CryptoEngine(master_key=request.user.password)


class EntryDetailView(DetailView):
    """ Details about a given entry """

    model = Entry
    context_object_name = 'entry'
    template_name = 'entry_get.html'

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        decrypted = engine.decrypt(context['entry'].password)
        print decrypted
        context['decrypted_password'] = decrypted
        return context


class EntryListView(ListView):

    model = Entry
    context_object_name = 'entries'
    template_name = 'entry_list.html'
    paginate_by = 200


class EntryCreate(CreateView):
    """ Enables creation of new entries """

    model = Entry
    template_name = 'entry_create.html'
    form_class = EntryForm

    def post(self, request, *args, **kwargs):

        if request.user.is_superuser:
            engine = CryptoEngine(master_key=request.user.password)

            form = EntryForm(request.POST)
            if form.is_valid():
                entry = form.save(commit=False)
                entry.password = engine.encrypt(form.cleaned_data['password'])
                entry.save()
                return redirect('home')
            else:
                form = EntryForm()
        return render(request, self.template_name, locals())


class EntryUpdate(UpdateView):
    """ Enables update of a given entry """

    model = Entry
    template_name = 'entry_update.html'
    form_class = EntryForm

    def post(self, request, *args, **kwargs):

        if request.user.is_superuser:
            engine = CryptoEngine(master_key=request.user.password)

            form = EntryForm(request.POST)
            if form.is_valid():
                entry = form.save(commit=False)
                entry.id = kwargs['pk']
                entry.date = datetime.date.today()
                entry.password = engine.encrypt(form.cleaned_data['password'])
                entry.save()
                return redirect('home')
            else:
                form = EntryForm()
        return render(request, self.template_name, locals())


class EntryDelete(DeleteView):
    """ Enables deletion of a given entry """

    model = Entry
    context_object_name = 'entry'
    template_name = 'entry_delete.html'
    # FIXME
    success_url = '/'


def entry_search(request):

    if request.POST:
        if request.POST['search']:
            entries = Entry.objects.filter(title__contains=request.POST['search'])
        else:
            entries = Entry.objects.all()
    return render(request, 'entry_list.html', locals())
