import qrcode

base_url = "http://192.168.100.94:8000/"

for masa in range(1,11):
    url = f"{base_url}?masa={masa}"
    img = qrcode.make(url)
    img.save(f"qr_codes/masa_{masa}.png")