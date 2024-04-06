from django.http import HttpResponse
from django.template.loader import render_to_string

def home_view(request, *args, **kwargs):
    context={}
    HTML_STRING = render_to_string("hacnitewelcome.html",context=context)

    return HttpResponse(HTML_STRING)