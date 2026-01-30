from django.urls import path
from . import views

urlpatterns = [
    # List produk (halaman utama)
    path('', views.produk_list, name='produk_list'),
    
    # CRUD operations
    path('tambah/', views.produk_create, name='produk_create'),
    path('edit/<int:pk>/', views.produk_update, name='produk_update'),
    path('hapus/<int:pk>/', views.produk_delete, name='produk_delete'),
    path('detail/<int:pk>/', views.produk_detail, name='produk_detail'),
]
