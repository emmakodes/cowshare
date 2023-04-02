from django.shortcuts import render

# Create your views here.
def index(request):
    
    context = {
        
    }
    return render(request, 'cowshare/index.html',context)

def products(request):
    context = {
        
    }
    return render(request, 'cowshare/products.html',context)
