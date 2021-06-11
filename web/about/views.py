from django.views import generic
from .models import About


class AboutListView(generic.ListView):
    model = About
    context_object_name = 'about_list'
