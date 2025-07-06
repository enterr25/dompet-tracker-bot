import datetime

def format_rp(jumlah):
    try:
        return f"Rp{int(jumlah):,}".replace(",", ".")
    except:
        return "Rp0"

def filter_transaksi_by_date(data, rentang="hari"):
    now = datetime.datetime.now()
    hasil = []
    for row in data:
        try:
            tgl = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        except:
            try:
                tgl = datetime.datetime.strptime(row[0], "%Y-%m-%d")
            except:
                continue
        if rentang == "hari" and tgl.date() == now.date():
            hasil.append(row)
        elif rentang == "minggu" and now - datetime.timedelta(days=7) <= tgl <= now:
            hasil.append(row)
        elif rentang == "bulan" and tgl.year == now.year and tgl.month == now.month:
            hasil.append(row)
    return hasil

def rekapkan(data):
    masuk = sum(int(row[1]) for row in data if row[2].lower() == "masuk")
    keluar = sum(int(row[1]) for row in data if row[2].lower() == "keluar")
    saldo = masuk - keluar
    return masuk, keluar, saldo
