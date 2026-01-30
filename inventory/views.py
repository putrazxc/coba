from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Produk, Kategori, Status
from .forms import ProdukForm
from .serializers import ProdukSerializer


def produk_list(request):
    """
    View untuk menampilkan daftar produk yang bisa dijual
    """
    # Filter produk dengan status "bisa dijual"
    produks = Produk.objects.filter(
        status__nama_status__icontains='bisa dijual'
    ).select_related('kategori', 'status')
    
    # Search functionality (optional)
    search = request.GET.get('search', '')
    if search:
        produks = produks.filter(
            Q(nama_produk__icontains=search) |
            Q(kategori__nama_kategori__icontains=search)
        )
    
    context = {
        'produks': produks,
        'search': search,
        'total_produk': produks.count()
    }
    
    return render(request, 'inventory/produk_list.html', context)


def produk_create(request):
    """
    View untuk menambah produk baru dengan validasi
    """
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Produk berhasil ditambahkan!')
            return redirect('produk_list')
        else:
            messages.error(request, '❌ Gagal menambahkan produk. Periksa form kembali.')
    else:
        form = ProdukForm()
    
    context = {
        'form': form,
        'title': 'Tambah Produk Baru',
        'button_text': 'Simpan'
    }
    
    return render(request, 'inventory/produk_form.html', context)


def produk_update(request, pk):
    """
    View untuk edit produk dengan validasi
    """
    produk = get_object_or_404(Produk, id_produk=pk)
    
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Produk berhasil diupdate!')
            return redirect('produk_list')
        else:
            messages.error(request, '❌ Gagal mengupdate produk. Periksa form kembali.')
    else:
        form = ProdukForm(instance=produk)
    
    context = {
        'form': form,
        'title': f'Edit Produk: {produk.nama_produk}',
        'button_text': 'Update',
        'produk': produk
    }
    
    return render(request, 'inventory/produk_form.html', context)


def produk_delete(request, pk):
    """
    View untuk hapus produk dengan konfirmasi
    """
    produk = get_object_or_404(Produk, id_produk=pk)
    
    if request.method == 'POST':
        nama_produk = produk.nama_produk
        produk.delete()
        messages.success(request, f'✅ Produk "{nama_produk}" berhasil dihapus!')
        return redirect('produk_list')
    
    context = {
        'produk': produk
    }
    
    return render(request, 'inventory/produk_confirm_delete.html', context)


def produk_detail(request, pk):
    """
    View untuk melihat detail produk
    """
    produk = get_object_or_404(Produk, id_produk=pk)
    
    context = {
        'produk': produk
    }
    
    return render(request, 'inventory/produk_detail.html', context)
