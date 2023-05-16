from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name='MainApp'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'
         ),
    path('product/<int:product_id>/', views.product_details, name='product'),
    path('basket_adding', views.basket_adding, name='basket_adding'),
    path('checkout', views.checkout, name='checkout'),
    path('login',views.login_user,name='login'),
    path('register',views.RegisterView.as_view(),name='register'),
    path('logout',views.logout_user,name='logout'),
    path('about',views.about,name='about'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
