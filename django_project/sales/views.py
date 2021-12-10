from decimal import Decimal
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django import forms
from .check import Checker
import logging
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Item

#logger = logging.getLogger(__name__)
#logger['handlers'] = ['console']


def updateView(request):
    # logger.info('Update')
    c = Checker()
    a = ""
    for item in Item.objects.all():
        resp = c.check(item.item_name, item.last_price,
                       item.author.first_name, item.author.email, item.getURLs())
        if resp:
            item.last_price = resp[0]
            item.on_sale = resp[1]
            item.last_site = resp[2]
            item.last_url = resp[3]
            a += item.item_name
            item.save()
    c.closeDriver()
    return HttpResponse("<p>" + a + "</p>")


def home(request):
    context = {}
    if request.user.is_authenticated:
        context = {
            'items': Item.objects.filter(author=request.user)
        }
    return render(request, 'sales/home.html', context)


class ItemListView(ListView):
    model = Item
    template_name = 'sales/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'items'
    ordering = ['-date_posted']
    paginate_by = 5


class UserItemListView(ListView):
    model = Item
    template_name = 'sales/user_items.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Item.objects.filter(author=user).order_by('-date_posted')


class ItemDetailView(DetailView):
    model = Item
    if Item.last_price == 0:
        Item.last_price = Item.regular_price
        Item.save()


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['item_name', 'urls', 'regular_price']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['item_name', 'urls', 'regular_price']

    def form_valid(self, form):
        print(form)
        form.instance.author = self.request.user
        #form.instance.regular_price = self.request.regular_price
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
