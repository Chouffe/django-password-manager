from manager.models import Category
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from manager.forms import CategoryForm


# engine = None
#
# if engine is not None:
#     if request.user.is_superuser:
#         print 'SuperUser!!!'
#         engine = CryptoEngine(master_key=request.user.password)


class CategoryDetailView(DetailView):
    """ Details about a given entry """

    model = Category
    context_object_name = 'category'
    template_name = 'category_get.html'



class CategoryListView(ListView):

    model = Category
    context_object_name = 'categories'
    template_name = 'category_list.html'
    paginate_by = 100


class CategoryCreate(CreateView):
    """ Enables creation of new entries """

    model = Category
    template_name = 'category_create.html'
    form_class = CategoryForm
    # success_url = todo


class CategoryUpdate(UpdateView):
    """ Enables update of a given entry """

    model = Category
    template_name = 'category_update.html'
    form_class = CategoryForm
    # FIXME
    success_url = '../../home'


class CategoryDelete(DeleteView):
    """ Enables deletion of a given entry """

    model = Category
    context_object_name = 'category'
    template_name = 'category_delete.html'
    # FIXME
    success_url = '../../home'
