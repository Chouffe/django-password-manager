from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import datetime
from django.shortcuts import redirect
from manager.forms import EntryForm
from django.shortcuts import render
from manager.models import CryptoEngine, Entry, Category
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.http import HttpResponse


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

    # def get_context_data(self, **kwargs):
    #     context = super(EntryListView, self).get_context_data(**kwargs)
    #     categories = Category.objects.all()
    #     print categories
    #     context['cateories'] = categories
    #     return context


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
                messages.add_message(request, messages.INFO, u'New entry added: {}'.format(entry.title))
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
                messages.add_message(request, messages.INFO, u'Entry updated: {}'.format(entry.title))
                return redirect('home')
            else:
                form = EntryForm()
        return render(request, self.template_name, locals())


class EntryDelete(DeleteView):
    """ Enables deletion of a given entry """

    model = Entry
    context_object_name = 'entry'
    template_name = 'entry_delete.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.WARNING, "Entry deleted")
        return super(DeleteView, self).post(request, *args, **kwargs)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def entry_search(request):

    # Loads the categories
    categories = Category.objects.all()

    # Loads the entries
    if request.POST:
        if request.POST['search']:
            entries = Entry.objects.filter(title__contains=request.POST['search'])
            search = request.POST['search']
        else:
            entries = Entry.objects.all()

        if len(entries) == 0:
            messages.add_message(request, messages.WARNING, u'No entries related to {}'.format(request.POST['search']))
    else:
        entries = Entry.objects.all()

    return render(request, 'entry_list.html', locals())
