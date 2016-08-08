import json

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from .models import Url

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

@require_POST
@csrf_exempt
def shorten(request):
    orig_url = request.POST['url']
    
    if 'shortened_url' in request.POST:
        shortened_url = request.POST['shortened_url']
        try:
            url = Url.objects.get(shortened_url=shortened_url)
            
            messages.error(request, 'ERROR: The provided custom URL already exists.')

            if 'response_type' in request.POST:
                if request.POST['response_type'] == 'json':
                    return JsonResponse({'msg' : 'The provided custom URL already exists.'})

            return render(request, 'index.html', {
                'url': orig_url,
#                'shortened_url': shortened_url
            })
        except Url.DoesNotExist:
            pass
    
    try:
        url = Url.objects.get(original_url=orig_url)
        shortened_url = request.POST['shortened_url']
        
        if shortened_url != '':
            url.shortened_url = shortened_url
        else:
            # Return existing url
            shortened_url = url.shortened_url
        
        # Increment shorten_count
        url.shorten_count = url.shorten_count + 1
        url.save()
    except Url.DoesNotExist:
        # Create new object
        url = Url.objects.create(original_url=orig_url, visit_count=1, shorten_count=1)
        shortened_url = request.POST['shortened_url']
        if shortened_url == '':
            # Shorten the url
            shortened_url = base62encode(url.pk)
        url.shortened_url = shortened_url
        url.save()
        
    messages.success(request, 'SUCCESS: Shortened URL generated.')
    
    if 'response_type' in request.POST:
        if request.POST['response_type'] == 'json':
            return JsonResponse({'shortened_url' : shortened_url, 'shorten_count': url.shorten_count})
        
    return render(request, 'index.html', {
        'url': orig_url,
        'shortened_url': shortened_url
    })

#    return JsonResponse({'shortened_url' : shortened_url, 'shorten_count': url.shorten_count})

@require_GET
def list_all(request): 
    urls = Url.objects.all()
#    urls_dict = dict(urls)
    if 'response_type' in request.POST:
        if request.POST['response_type'] == 'json':
            return JsonResponse(serializers.serialize('json', urls), safe=False)
    return render(request, 'view_all.html', {
        "urls" : urls,
    })

@require_GET
def original_url(request, hash_val):
    try:
        url = Url.objects.get(shortened_url=hash_val)
        original_url = url.original_url
        url.visit_count = url.visit_count + 1
        url.save()
        return redirect(original_url)
    except Url.DoesNotExist:
        raise Http404("Page does not exist")

def base62encode(number):
    BASE10 = "0123456789"
    BASE62 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
 
    if str(number)[0] == '-':
        number = str(number)[1:]
        neg = 1
    else:
        neg = 0
 
    # make an integer out of the number
    x=0
    for digit in str(number):
       x = x*len(BASE10) + BASE10.index(digit)
   
    if x == 0:
        res = BASE62[0]
    else:
        res = ""
        while x>0:
            digit = x % len(BASE62)
            res = BASE62[digit] + res
            x = int(x / len(BASE62))
        if neg:
            res = "-" + res
 
    return res