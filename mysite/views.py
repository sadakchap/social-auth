from django.shortcuts import render

def index(req):
    return render(req,'index.html')

def about(req):
    return render(req,'about.html')
