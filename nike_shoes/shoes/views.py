from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View
from .models import Shoe, Cart, CartItem
from .forms import ShoeForm


def home(request):

    shoes = Shoe.objects.all()
    
    category = request.GET.get('category')
    size = request.GET.get('size')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if category:
        shoes = shoes.filter(category__icontains=category)
    if size:
        shoes = shoes.filter(size=size)
    if min_price:
        shoes = shoes.filter(price__gte=min_price)
    if max_price:
        shoes = shoes.filter(price__lte=max_price)
    
    context = {
        "shoes": shoes,
    }
    return render(request, 'home.html', context)

class HomeView(ListView):
    model = Shoe
    template_name = 'home.html'
    context_object_name = 'shoes'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        size = self.request.GET.get('size')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if category:
            queryset = queryset.filter(category__icontains=category)
        if size:
            queryset = queryset.filter(size=size)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


def shoe_detail(request, shoe_id):
    shoe = get_object_or_404(Shoe, id=shoe_id)
    context = {
        "shoe": shoe
    }
    return render(request, 'shoe_detail.html', context)

class ShoeDetailView(DetailView):
    model = Shoe
    template_name = 'shoe_detail.html'
    pk_url_kwarg = 'shoe_id'
    context_object_name = 'shoe'


def view_cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.shoe.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

class ViewCart(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = CartItem.objects.all()
        total_price = sum(item.shoe.price * item.quantity for item in cart_items)
        
        context['cart_items'] = cart_items
        context['total_price'] = total_price
        return context
    

def add_to_cart(request, shoe_id):
    cart, created = Cart.objects.get_or_create(user=request.user)

    shoe = get_object_or_404(Shoe, id=shoe_id)
    cart_item, created = CartItem.objects.get_or_create(
        shoe=shoe,
        cart=cart,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

    
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def add_shoe(request):
    if request.method == 'POST':
        form = ShoeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the new shoe to the database
            return redirect('home')  # Redirect to home page after adding shoe
    else:
        form = ShoeForm()
    return render(request, 'add_shoe.html', {'form': form})
