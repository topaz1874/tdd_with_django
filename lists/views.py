from django.shortcuts import render, redirect
from .models import Item
# Create your views here.


def home_page(request):
    # return HttpResponse('<html><title>To-Do lists</title></html>')
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {
        'items': items
        })

