from django.shortcuts import render

# Create your views here.

def inbox(request):
    context = {}
    return render(request, 'chat/chat.html', context=context)