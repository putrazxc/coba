from rest_framework import serializers
from .models import Produk, Kategori, Status


class KategoriSerializer(serializers.ModelSerializer):
    """Serializer untuk model Kategori"""
    
    class Meta:
        model = Kategori
        fields = ['id_kategori', 'nama_kategori']


class StatusSerializer(serializers.ModelSerializer):
    """Serializer untuk model Status"""
    
    class Meta:
        model = Status
        fields = ['id_status', 'nama_status']


class ProdukSerializer(serializers.ModelSerializer):
    """Serializer untuk model Produk dengan nested kategori dan status"""
    kategori_nama = serializers.CharField(source='kategori.nama_kategori', read_only=True)
    status_nama = serializers.CharField(source='status.nama_status', read_only=True)
    harga_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Produk
        fields = [
            'id_produk',
            'nama_produk',
            'harga',
            'harga_formatted',
            'kategori',
            'kategori_nama',
            'status',
            'status_nama'
        ]
    
    def get_harga_formatted(self, obj):
        """Format harga dengan Rupiah"""
        return obj.get_harga_formatted()


class ProdukCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer untuk create dan update produk dengan validasi"""
    
    class Meta:
        model = Produk
        fields = ['id_produk', 'nama_produk', 'harga', 'kategori', 'status']
    
    def validate_nama_produk(self, value):
        """Validasi nama produk tidak boleh kosong"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("Nama produk wajib diisi")
        return value.strip()
    
    def validate_harga(self, value):
        """Validasi harga harus positif"""
        if value <= 0:
            raise serializers.ValidationError("Harga harus lebih dari 0")
        return value
