from django.shortcuts import render, redirect

from gallary.models import ItemImage, ReviewImage
from gallary.forms import ItemImageNewForm, ReviewImageNewForm
from .forms import NewItemForm
from .models import Item, Request, Notification


def index(request):
    context = {
        'items': Item.objects.all(),
    }
    return render(request, 'trade/index.html', context)


def new_item(request):
    if request.method == 'POST':
        item_form = NewItemForm(request.POST)
        image_form = ItemImageNewForm(request.POST, request.FILES)
        if item_form.is_valid() and image_form.is_valid():
            item = item_form.save(commit=False)
            item.user = request.user
            item.save()
            if request.FILES.get('image'):
                ItemImage.objects.create(
                    image=request.FILES['image'],
                    item=item,
                    user=request.user
                )
            return redirect('trade:trade_home')

    context = {
        'item_form': NewItemForm(),
        'image_item_form': ItemImageNewForm(),

    }
    return render(request, 'trade/new_item.html', context)


def request_item(request, pk):
    requested_item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        offered_item = Item.objects.get(pk=request.POST['offered_trade'])
        request_item_ob = Request.objects.create(
            user=request.user,
            requested_item=requested_item,
            offered_item=offered_item,
            note=request.POST['note'],
            status=None
        )
        Notification.objects.create(
            user=requested_item.user,
            user_req=request.user,
            request=request_item_ob
        )

    context = {
        'requested_item': requested_item,
    }
    return render(request, 'trade/request.html', context)


def request_status(request, pk):
    request_obj = Request.objects.get(pk=pk)
    if not request_obj.status:
        if request.method == 'POST':
            if request.POST['answer'] == '1':
                request_obj.status = 'Accepted'
            else:
                request_obj.status = 'Declined'
            request_obj.save()
            print(request.POST['answer'])

            Notification.objects.create(
                user=request_obj.user,
                user_req=request.user,
                request=request_obj
            )

        context = {
            'request_obj': request_obj
        }
        return render(request, 'trade/request_status.html', context)
    else:
        return redirect('user:home_page')


