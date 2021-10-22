from django.shortcuts import render
from django.views import View 
from django.utils.timezone import datetime
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from customer.models import OrderModel




class DashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        today= datetime.today()
        # find the orders for that particular day
        orders= OrderModel.objects.filter(
            created_on__year= today.year, 
            created_on__month= today.month, 
            created_on__day= today.day
        )
        # looping through the orders and add the prices to get the total revenue
        total_revenue= 0
        unfinished_orders= []
        for order in orders:
            total_revenue += order.price 
            # getting all the unfinished products and diplay them on the dasheboard
            if not order.is_paid or not order.is_shipped:
                unfinished_orders.append(order)
        
        context= {
            'total_revenue': total_revenue,
            'orders': unfinished_orders,
            'total_orders': len(orders), 
            'title': 'Dashboard'
        }
        return render(request, 'restorant/dashboard.html', context)
    def test_func(self):
        return self.request.user.groups.filter(name= 'staff').exists()

class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order= OrderModel.objects.get(pk=pk)
        context= {
            'order': order,
            'title': order.name
        }
        return render(request, 'restorant/order_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        order= OrderModel.objects.get(pk=pk)
        order.is_shipped= True
        order.save()
        context= {
            'order': order,
            'title': order.name
        }
        return render(request, 'restorant/order_detail.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name= 'staff').exists()
