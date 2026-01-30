from django.db import models


class Kategori(models.Model):
    """Model untuk kategori produk"""
    id_kategori = models.IntegerField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)

    class Meta:
        db_table = 'kategori'
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategori'

    def __str__(self):
        return self.nama_kategori


class Status(models.Model):
    """Model untuk status produk"""
    id_status = models.IntegerField(primary_key=True)
    nama_status = models.CharField(max_length=50)

    class Meta:
        db_table = 'status'
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.nama_status


class Produk(models.Model):
    """Model untuk produk"""
    id_produk = models.IntegerField(primary_key=True)
    nama_produk = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.PROTECT,
        db_column='kategori_id'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        db_column='status_id'
    )

    class Meta:
        db_table = 'produk'
        verbose_name = 'Produk'
        verbose_name_plural = 'Produk'
        ordering = ['id_produk']

    def __str__(self):
        return self.nama_produk

    def get_harga_formatted(self):
        """Format harga dengan thousand separator"""
        return f"Rp {self.harga:,.0f}".replace(',', '.')
