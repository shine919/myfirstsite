from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import *
from django.views.generic import TemplateView


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'MainApp/homePage.html',
                  {
                      'pr': products,
                      'category': category,
                      'categories': categories,
                  })


def product_details(request, product_id):
    product = get_object_or_404(Product,id=product_id)


    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    print(request.session.session_key)



    return render(request, 'MainApp/product.html', locals())

def about(request):
    return render(request,'MainApp/about.html',locals())
def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, defaults={"nmb": nmb})
        if not created:
            print ("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)


    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in  products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["title"] = item.product.title
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)
def checkout(request):
    data = request.POST
    form = CheckoutContactForm(request.POST or None)
    context = {'form': CheckoutContactForm()}
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    print (products_in_basket)
    for item in products_in_basket:
        print(item.order)
    is_delete = data.get("is_delete")
    product_id = data.get("product_id")
    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
        print(is_delete)
    if request.POST:
            user = request.user
            name = data.get("name", "3423453")
            phone = data.get("phone")
            payment = data.get("payment")
            address = data.get("address")
            order = Order.objects.create(user=user, status_id=1,customer_name=name, customer_phone=phone,customer_payment = payment,customer_address = address)
            if form.is_valid():
                for title, value in data.items():
                    if title.startswith("product_in_basket_"):
                        product_in_basket_id = title.split("product_in_basket_")[1]
                        product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                        print(type(value))
                        product_in_basket.nmb = value
                        product_in_basket.order = order
                        product_in_basket.save(force_update=True)

                        ProductInOrder.objects.create(product=product_in_basket.product, nmb = product_in_basket.nmb,
                                                      price_per_item=product_in_basket.price_per_item,
                                                      total_price = product_in_basket.total_price,
                                                      order=order)

            if is_delete == 'true':
                ProductInBasket.objects.filter(session_key=session_key).update(is_active=False)
                print(is_delete)
                print(product_id)
                print(session_key)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    ProductInBasket.objects.filter(is_active=False,session_key=session_key).update(order=None)
    return render(request, 'MainApp/checkout.html', locals())

def login_user(request):
    context={'login_form': LoginForm()}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('/')
            else:
                context={
                    'login_form':login_form,
                    'attention':f'Пользователь или пароль неверны'
                }
        else:
            context = {
                'login_form': login_form,
            }
    return render(request, 'MainApp/login.html', context)

class RegisterView(TemplateView):
    template_name = 'MainApp/register.html'

    def get(self,request):
        user_form = RegisterForm()
        context = {
            'user_form':user_form
        }
        return render(request,'MainApp/register.html',context)
    def post(self,request):
        user_form=RegisterForm(request.POST)
        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            login(request,user)
            return redirect('/')
        context = {
            'user_form': user_form
        }
        return render(request, 'MainApp/register.html', context)
def logout_user(request):
    logout(request)
    return redirect('/')
