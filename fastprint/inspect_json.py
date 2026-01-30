"""
Script untuk melihat struktur JSON response dari API
Agar kita tahu field name yang benar

Usage: python inspect_json.py
"""

import requests
import hashlib
import json
from datetime import datetime, timedelta


def inspect_json():
    url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
    
    print("\n" + "="*70)
    print("🔍 INSPECT JSON STRUCTURE")
    print("="*70)
    
    session = requests.Session()
    
    # GET request
    print("\n[1] GET Request...")
    try:
        get_response = session.get(url, timeout=10)
        print(f"✅ Status: {get_response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Parse date
    server_date_str = get_response.headers["Date"]
    server_date_gmt = datetime.strptime(
        server_date_str,
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    
    # GMT+5
    server_date = server_date_gmt + timedelta(hours=5)
    
    day = server_date.day
    month = server_date.month
    year_2 = str(server_date.year)[2:]
    
    # Generate credentials
    username = f"tesprogrammer{day:02d}{month:02d}{year_2}C02"
    password_raw = f"bisacoding-{day:02d}-{month:02d}-{year_2}"
    password_md5 = hashlib.md5(password_raw.encode()).hexdigest()
    
    print(f"\n[2] Login dengan credentials...")
    print(f"    Username: {username}")
    print(f"    Password: {password_raw}")
    
    # POST request
    payload = {
        "username": username,
        "password": password_md5
    }
    
    try:
        post_response = session.post(
            url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        print(f"\n✅ Status: {post_response.status_code}")
        
        if post_response.status_code != 200:
            print(f"❌ Login gagal: {post_response.text}")
            return
        
        # Parse JSON
        json_data = post_response.json()
        
        print("\n" + "="*70)
        print("📋 STRUKTUR JSON RESPONSE")
        print("="*70)
        
        # Print full JSON (pretty)
        print("\n[A] Full JSON Response:")
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
        
        # Check data structure
        if "data" in json_data:
            print("\n" + "="*70)
            print("[B] Analisis Data Array")
            print("="*70)
            
            data_array = json_data["data"]
            print(f"\n📊 Total items: {len(data_array)}")
            
            if data_array:
                print("\n[C] Struktur Item Pertama:")
                print("-"*70)
                first_item = data_array[0]
                
                print("\nField names dan tipe data:")
                for key, value in first_item.items():
                    value_type = type(value).__name__
                    print(f"  {key:20} : {value_type:10} = {value}")
                
                print("\n" + "="*70)
                print("[D] Sample 3 Produk Pertama (Detail)")
                print("="*70)
                
                for i, item in enumerate(data_array[:3], 1):
                    print(f"\n[Produk {i}]")
                    for key, value in item.items():
                        print(f"  {key:20} : {value}")
                
                print("\n" + "="*70)
                print("[E] Summary - Field Names yang Tersedia:")
                print("="*70)
                
                field_names = list(first_item.keys())
                print("\nFields yang ada di response:")
                for field in field_names:
                    print(f"  ✓ {field}")
                
                print("\n" + "="*70)
                print("[F] Mapping untuk Django Models:")
                print("="*70)
                
                print("\nField mapping yang perlu digunakan:")
                print("Django Model Field    →  API Response Field")
                print("-"*70)
                
                # Cek berbagai kemungkinan field name
                possible_mappings = {
                    'id_produk': ['id', 'id_produk', 'produk_id', 'product_id'],
                    'nama_produk': ['nama', 'nama_produk', 'name', 'product_name'],
                    'harga': ['harga', 'price', 'harga_produk'],
                    'kategori_id': ['kategori_id', 'id_kategori', 'category_id'],
                    'kategori': ['kategori', 'nama_kategori', 'category', 'category_name'],
                    'status_id': ['status_id', 'id_status'],
                    'status': ['status', 'nama_status', 'status_name']
                }
                
                detected_mapping = {}
                
                for django_field, possible_fields in possible_mappings.items():
                    for api_field in possible_fields:
                        if api_field in first_item:
                            detected_mapping[django_field] = api_field
                            print(f"{django_field:20} →  {api_field}")
                            break
                
                print("\n" + "="*70)
                print("💾 SIMPAN INFORMASI INI UNTUK UPDATE DJANGO CODE!")
                print("="*70)
        
        else:
            print("\n❌ Tidak ada key 'data' di response!")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    inspect_json()