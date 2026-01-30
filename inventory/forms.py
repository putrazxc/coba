from django import forms
from .models import Produk, Kategori, Status


class ProdukForm(forms.ModelForm):
    """Form untuk tambah dan edit produk dengan validasi"""
    
    class Meta:
        model = Produk
        fields = ['id_produk', 'nama_produk', 'harga', 'kategori', 'status']
        widgets = {
            'id_produk': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID Produk'
            }),
            'nama_produk': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Produk',
                'required': True
            }),
            'harga': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Harga',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
            'kategori': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            })
        }
        labels = {
            'id_produk': 'ID Produk',
            'nama_produk': 'Nama Produk',
            'harga': 'Harga (Rp)',
            'kategori': 'Kategori',
            'status': 'Status'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Jika edit (ada instance), disable id_produk
        if self.instance and self.instance.pk:
            self.fields['id_produk'].widget.attrs['readonly'] = True
    
    def clean_nama_produk(self):
        """Validasi nama produk wajib diisi"""
        nama = self.cleaned_data.get('nama_produk')
        if not nama or nama.strip() == '':
            raise forms.ValidationError('Nama produk wajib diisi')
        return nama.strip()
    
    def clean_harga(self):
        """Validasi harga harus berupa angka positif"""
        harga = self.cleaned_data.get('harga')
        if harga is None:
            raise forms.ValidationError('Harga wajib diisi')
        if harga <= 0:
            raise forms.ValidationError('Harga harus lebih dari 0')
        return harga
    
    def clean_id_produk(self):
        """Validasi ID produk untuk insert baru"""
        id_produk = self.cleaned_data.get('id_produk')
        
        # Jika ini bukan edit (tidak ada instance.pk)
        if not self.instance.pk:
            # Cek apakah ID sudah ada
            if Produk.objects.filter(id_produk=id_produk).exists():
                raise forms.ValidationError('ID Produk sudah digunakan')
        
        return id_produk
