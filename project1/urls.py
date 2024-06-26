"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import settings
from store.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('store',Dashboard.as_view(),name="store"),
    path('', Dashboard.as_view(), name='dashboard'),
    path('dashboard/<int:category_id>/', Dashboard.as_view(), name='dashboard_with_category'),
    # path('add_to_cart/',Add_to_cart.as_view(),name="add_to_cart_empty"),
    # path('add_to_cart/<int:product_id>/',Add_to_cart.as_view(),name="add_to_cart"),
    path('view-cart/',View_Cart.as_view(),name="view-cart"),
    path('order/',OrderView.as_view(),name='order'),
    path('signup/',Signup.as_view(),name="signup"),
    path('login/',Login.as_view(),name="login"),
    path('logout/',Logout.as_view(),name="logout"),
    path("webscrap/",webscrapper.as_view(),name="webscrap"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
