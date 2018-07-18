from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import time

# Create your views here.
def index(request):
    context = None
    return render(request, 'bus/index.html', context)


def printAjax(request):
    print 'printAjax', request.GET
    data = {
        'success': time.time(),
    }
    return JsonResponse(data)