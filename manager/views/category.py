from manager.models import CryptoEngine, Entry, Category
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


class CategoryDetailView(DetailView):
    """ Details about a given entry """

    model = Category
    context_object_name = 'category'
    template_name = 'manager/category_get.html'
