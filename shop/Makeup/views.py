from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import *
from django.contrib import messages 

# ===================== Pages =====================

def main(request):
    return render(request, "main.html")

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to access this page")
    return render(request, "dashboard.html")

# ===================== Auth =====================

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('products')
        else:
            return render(request, 'login.html', {
                'error': 'Username or password is incorrect'
            })
        

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def is_admin(user):
    return user.is_staff

@login_required(login_url='login')
@user_passes_test(is_admin)
def dashboard(request):
    return render(request, "dashboard.html")
























    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ===================== Products =====================

def products(request):
    # جلب كل المنتجات من قاعدة البيانات
    products_list = Products.objects.all() 
    # إرسالها للصفحة باسم "products" لكي تتعرف عليها حلقة الـ for
    return render(request, "products.html", {"products": products_list})

@login_required(login_url='login')
def list_products(request):
    products = Products.objects.all()
    return render(request, "list.html", {'products': products})

@login_required(login_url='login')
def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        Products.objects.create(name=name, price=price, image=image)
        return redirect('list')
    return render(request, 'add_product.html')

@login_required(login_url='login')
def edit_product(request, id):
    product = get_object_or_404(Products, id=id)
    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        return redirect('list')
    return render(request, 'edit_product.html', {'product': product})

@login_required(login_url='login')
def delete_product(request, id):
    product = get_object_or_404(Products, id=id)
    if request.method == "POST":
        product.delete()
        cart = request.session.get('cart', {})
        if str(id) in cart:
            del cart[str(id)]
            request.session['cart'] = cart
        return redirect('list')
    return render(request, 'delete_product.html', {'product': product})

# ===================== Cart =====================

@login_required(login_url='login')
def cart(request):
    # 1. التأكد من إنشاء السلة في الجلسة إذا لم تكن موجودة
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    # جلب السلة الحالية
    cart_session = request.session['cart']

    # 2. معالجة ضغطة الزر (إضافة المنتج)
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        
        if product_id:
            # تحويل الـ ID لنص لأن مفاتيح الـ Session يجب أن تكون نصوصاً
            p_id_str = str(product_id)
            
            # إذا المنتج موجود زود الكمية، وإذا مش موجود أضفه بقيمة 1
            if p_id_str in cart_session:
                cart_session[p_id_str] += 1
            else:
                cart_session[p_id_str] = 1
            
            # إخبار Django أن الجلسة تعدلت ليتم حفظها في قاعدة البيانات
            request.session.modified = True
            
            # بعد الإضافة، يفضل البقاء في نفس الصفحة أو التوجه للسلة
            return redirect('cart')

    # 3. عرض المنتجات في السلة
    display_items = []
    grand_total = 0
    
    for p_id, qty in cart_session.items():
        # البحث عن المنتج في قاعدة البيانات باستخدام الـ ID
        product = Products.objects.filter(id=p_id).first()
        if product:
            subtotal = product.price * qty
            grand_total += subtotal
            display_items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal
            })
            
    return render(request, 'cart.html', {
        'cart_items': display_items,
        'total': grand_total
    })
@login_required(login_url='login')
def remove_from_cart(request, product_id):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        p_id_str = str(product_id)
        if p_id_str in cart:
            del cart[p_id_str]
            request.session.modified = True
    return redirect('cart')
def add_to_cart(request, product_id):
    # 1. التأكد من وجود سلة
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    # 2. جلب السلة وتعديلها
    cart = request.session['cart']
    p_id_str = str(product_id)
    cart[p_id_str] = cart.get(p_id_str, 0) + 1
    
    # 3. إجبار السيشين على الحفظ
    request.session.modified = True
    request.session.save() # إضافة سطر حفظ إضافي للتأكيد
    
    # 4. إضافة رسالة نجاح تظهر للمستخدم
    messages.success(request, "تم إضافة المنتج بنجاح!")
    
    return redirect('cart')