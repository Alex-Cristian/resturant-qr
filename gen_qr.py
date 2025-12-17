import qrcode

base_url = "https://resturant-qr.onrender.com/meniu/masa"

for masa in range(1,11):
    url = f"{base_url}/{masa}"
    img = qrcode.make(url)
    img.save(f"qr_codes/masa_{masa}.png")