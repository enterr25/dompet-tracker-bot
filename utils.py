
# utils.py - Fungsi tambahan untuk CatatUangBot Pro
# Termasuk: Format Rupiah, Filter Laporan, dll

import datetime

def format_rp(x):
    try:
        return f"Rp{x:,.0f}".replace(",", ".")
    except:
        return "Rp0"

def filter_transaksi_by_date(data, rentang):
    now = datetime.datetime.now()

    if rentang == "hari":
        batas = now.date()
        hasil = [r for r in data if datetime.datetime.strptime(r[0], '%Y-%m-%d').date() == batas]
    elif rentang == "minggu":
        batas = now - datetime.timedelta(days=now.weekday())
        hasil = [r for r in data if datetime.datetime.strptime(r[0], '%Y-%m-%d').date() >= batas.date()]
    elif rentang == "bulan":
        hasil = [r for r in data if datetime.datetime.strptime(r[0], '%Y-%m-%d').month == now.month]
    else:
        hasil = data

    return hasil

def rekapkan(data):
    try:
        masuk = sum(int(r[1]) for r in data if r[2] == "Masuk")
        keluar = sum(int(r[1]) for r in data if r[2] == "Keluar")
        return masuk, keluar, masuk - keluar
    except:
        return 0, 0, 0
