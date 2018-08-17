from django.shortcuts import render

# Create your views here.
def products(request):
    return render(request, 'products/products.html')

def productsold(request):
    return render(request, 'products/productsold.html')
