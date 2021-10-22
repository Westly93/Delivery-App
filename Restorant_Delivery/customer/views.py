import json
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View 
from django.db.models import Q
from .models import MenuItem, OrderModel


class IndexView(View):
    def get(self, request):
        context= {
            'title': 'Welcome'
        }
        return render(request, 'customer/index.html', context)
class AboutView(View):
    def get(self, request):
        context= {
            'title': 'About'
        }
        return render(request, 'customer/about.html', context)

class OrderView(View):
    def get(self, request):
        # Get all the categories
        appetizers= MenuItem.objects.filter(category__name__icontains= 'Appetizer')
        entres= MenuItem.objects.filter(category__name__icontains= 'Entre')
        drinks= MenuItem.objects.filter(category__name__icontains= 'Drink')
        desserts= MenuItem.objects.filter(category__name__icontains= 'Dessert')

        context= {
            'appetizers': appetizers,
            'entres': entres,
            'drinks': drinks,
            'desserts': desserts
        }

        return render(request, 'customer/order.html', context)
    
    def post(self, request):
        
        name= request.POST.get('name')
        email= request.POST.get('email')
        street= request.POST.get('street')
        city= request.POST.get('city')
        state= request.POST.get('state')
        zip_code= request.POST.get('zip_code')


        order_items= {
            'items': []
        }
        items= request.POST.getlist('items[]')
        for item in items:
            menu_item= MenuItem.objects.get(pk__contains= int(item))
            item_data= {
                'id': menu_item.pk,
                'price': menu_item.price,
                'name': menu_item.name
            }
            order_items['items'].append(item_data)
        price= 0
        item_ids= []
        for item in order_items['items']:
            price+= item['price']
            item_ids.append(item['id'])

        order= OrderModel.objects.create(
            price= price,
            name= name,
            email= email,
            street= street,
            city= city, 
            state= state,
            zip_code= zip_code
        )
        order.items.add(*item_ids)
        body= ('Thank you for your order your food is being cooked and will be delivered soon!\n'
            f'Your Total {price}\n'
            'Thank you again for your order'
        )
        send_mail(
            'Thank you for your order',
            body,
            'example@example.com',
            [email],
            fail_silently= False
        )

        return redirect('order-confirmation', pk= order.pk)

class OrderConfirmationView(View):
    def get(self, request, pk, *args, **kwargs):
        order= OrderModel.objects.get(pk= pk)
        context={
            'pk': order.pk,
            'items': order.items,
            'price': order.price
        }
        return render(request, 'customer/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        data= json.loads(request.body)
        print(data)
        if data['isPaid']:
            order= OrderModel.objects.get(pk= pk)
            order.is_paid= True
            order.save()
        return redirect('payment-confirmation')




class OrderPayConfirmationView(View):
    def get(self, request):
        return render(request, 'customer/order_pay_confirmation.html', {'title': 'Order Payment Confirmation'})


class MenuView(View):
    def get(self, request):
        menu_items= MenuItem.objects.all()
        context= {
            'menu_items': menu_items,
            'title': 'Menu Items'
        }
        return render(request, 'customer/menu.html', context)


class MenuSearchView(View):
    def get(self, request):
        query= self.request.GET.get('q')
        menu_items= MenuItem.objects.filter(
            Q(name__icontains= query)|
            Q(price__icontains= query)|
            Q(description__icontains= query)|
            Q(category__name__icontains= query)
        )
        context= {
            'menu_items': menu_items,
            'title': 'Menu Search'
        }
        return render(request, 'customer/menu.html', context)