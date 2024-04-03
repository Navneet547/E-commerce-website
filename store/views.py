from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models import *
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.hashers import  check_password,make_password
from django.shortcuts import render, redirect

class Dashboard(View):
    def get(self, request, category_id=None):
        categorylist = Category.objects.all()
        productlist = None
        
        if category_id:
            category_name=Category.objects.get(id=category_id)
            productlist = Products.objects.filter(category_id=category_id)
        elif categorylist:
            category_name=Category.objects.get(id=categorylist[0].id)
            productlist = Products.objects.filter(category_id=categorylist[0].id)

        context = {
            'category_name':category_name,
            'categorylist': categorylist,
            'productlist': productlist,
        }
        return render(request, 'dashboard.html', context)

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        # print('cart' , request.session['cart'])
        # print(quantity)
        return redirect('dashboard')
       
    
class View_Cart(View):
    def get(self, request):
        if 'customer_id' in request.session:
            cart = request.session.get('cart', {})
            # print('cart', cart)
            ids = list(cart.keys())
            if ids:
                products = Products.objects.filter(id__in=ids)
                return render(request, 'cart.html', {'products': products})
            else:
                return render(request, 'cart.html', {'empty_cart': True})
        else:
            return redirect("login")
        
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Products.objects.filter(id__in=list(cart.keys()))
        # print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('view-cart')
           

class OrderView(View):
    def get(self, request):
        Customer=request.session.get('customer_id')
        orders=Order.objects.filter(customer_id=Customer).order_by('-date')
        order={
            'orders':orders
        }
        return render(request,'order.html',order)
    

# Signup View

class Signup (View):
    def get(self, request):
        if 'customer_id' in request.session:
            return redirect('dashboard')
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            # print(first_name, last_name, phone, email, password)
            customer.password = make_password (customer.password)
            customer.save()
            return redirect ('login')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len (customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif Customer.objects.filter(email=customer.email):
            error_message = 'Email Address Already Registered..'

        return error_message
 
    
#login view

class Login(View):
    def get(self, request):
        if 'customer_id' in request.session:
            return redirect('dashboard')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.objects.filter(email=email).first()
        error_message = None

        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                # cart=request.session.get('cart')
                return redirect('dashboard')
            else:
                error_message = 'Invalid password'
        else:
            error_message = 'Customer not found'

        return render(request, 'login.html', {'error': error_message})


class Logout(View):
    def get(self,request):
        request.session.clear()
        return redirect('dashboard')

class webscrapper(View):
    def get(self,request):
        return render(request,"webscrap.html")
