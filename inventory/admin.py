from django.contrib import admin
from .models import Produk, Kategori, Status


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    """Admin untuk model Kategori"""
    list_display = ['id_kategori', 'nama_kategori']
    search_fields = ['nama_kategori']
    ordering = ['id_kategori']


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Admin untuk model Status"""
    list_display = ['id_status', 'nama_status']
    search_fields = ['nama_status']
    ordering = ['id_status']


@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    """Admin untuk model Produk"""
    list_display = [
        'id_produk', 
        'nama_produk', 
        'harga', 
        'get_kategori_nama', 
        'get_status_nama'
    ]
    list_filter = ['kategori', 'status']
    search_fields = ['nama_produk', 'kategori__nama_kategori']
    ordering = ['id_produk']
    
    def get_kategori_nama(self, obj):
        return obj.kategori.nama_kategori
    get_kategori_nama.short_description = 'Kategori'
    
    def get_status_nama(self, obj):
        return obj.status.nama_status
    get_status_nama.short_description = 'Status'
