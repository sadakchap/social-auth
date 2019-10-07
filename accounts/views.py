from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,ProfileEditForm,UserEditForm
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact,Profile

from actions.utils import create_action
from actions.models import Action

@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user','user__profile').prefetch_related('target')[:10]
    return render(request,'accounts/dashboard.html',{'section':'dashboard','actions':actions})

def register(req):
    form = UserRegisterForm(req.POST or None)
    if form.is_valid():
        pwrd2 = form.cleaned_data.get('pwrd2')
        new_user = form.save(commit=False)
        new_user.set_password(pwrd2)
        new_user.save()
        Profile.objects.create(user=new_user)
        messages.success(req,'Your Account has Been successfully CREATED.You can login now!')
        create_action(new_user,'has created an account')
        return redirect('login')
    return render(req,'accounts/register.html',{'form':form})

@login_required
def edit(req):
    u_form = UserEditForm(req.POST or None,instance=req.user)
    p_form = ProfileEditForm(req.POST or None,req.FILES or None,instance=req.user.profile)
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(req,"Your Profile has been successfully Updated!")
        return redirect('edit')
    return render(req,'accounts/edit.html',{'u_form':u_form,'p_form':p_form})


@login_required
def users_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,'accounts/users_list.html',{'section':'people','users':users})

@login_required
def user_detail(request,username):
    user = get_object_or_404(User,username=username,is_active=True)
    return render(request,'accounts/user_detail.html',{'section':'people','user':user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    u_id = request.POST.get('id')
    action = request.POST.get('action')
    print(u_id,action)
    if u_id and action:
        try:
            user = User.objects.get(id=u_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
                create_action(request.user,'following',user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})





















#
# def login_page(req):
#     next = req.GET.get('next')
#     form = UserLoginForm(req.POST or None)
#     if form.is_valid():
#         usrnm = form.cleaned_data.get('usrnm')
#         pswrd = form.cleaned_data.get('pswrd')
#         user = authenticate(username=usrnm,password=pswrd)
#         if user:
#             login(req,user)
#             messages.success(req,"You are successfully Logged in!!")
#             if next:
#                 return redirect(next)
#             return redirect('/')
#
#     return render(req,'accounts/login.html',{'form':form})
