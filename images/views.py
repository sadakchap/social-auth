from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ImageCreatForm
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from common.decorators import ajax_required

from django.views.decorators.http import require_POST
from django.http import JsonResponse,HttpResponse

from actions.utils import create_action

from .models import Image

import redis
from django.conf import settings
r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

# Create your views here.

@login_required
def image_list(request):
    images = Image.objects.order_by('-created')
    paginator = Paginator(images,2)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return HttpResponse('')
    if request.is_ajax():
        return render(request,'images/image_ajax_list.html',{'section':'images','images':images})
    return render(request,'images/image_list.html',{'section':'images','images':images})




@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreatForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request,"Image has Been shared Here!")
            create_action(request.user,'bookmarked image',new_item)
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreatForm(data=request.GET)
    return render(request,'images/image_form.html',{'form':form})


def image_detail(req,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    total_views = r.incr('image:{}:views'.format(image.id))
    r.zincrby('image_ranking',1,image_id)
    # print(r.zincrby('image_ranking',1,image.id)) zincrby(key,amount,value)
    return render(req,"images/image_detail.html",{'image':image,'total_views':total_views})

@login_required
def image_ranking(request):
    image_ranking = r.zrange('image_ranking',0,-1,desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    #get most viewed images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request,'images/image_ranking.html',{'most_viewed':most_viewed})

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                # print("adding")
                image.users_like.add(request.user)
                create_action(request.user,'liked',image)
            else:
                # print("removing")
                image.users_like.remove(request.user)
                create_action(request.user,'unliked',image)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})
