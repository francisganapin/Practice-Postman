from django.shortcuts import render
from .models import Cat

def cat_list(request):
    cats = Cat.objects.select_related('category').all()
    return render(request,'cats/cat_list.html',{'cats':cats})