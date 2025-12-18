from django.shortcuts import render, redirect, get_object_or_404
from .models import Categorie, Comanda, Masa, Produs, ProdusComanda, Cos

def get_cos_curent(request):
    masa_id = request.session.get("masa_id")
    if not masa_id:
        return None, None

    cosuri = request.session.get("cosuri", {})
    cos = cosuri.get(str(masa_id), {})

    return masa_id, cos


def meniu(request):
    masa = None
    masa_id = request.GET.get("masa")

    if masa_id:
        try:
            masa = Masa.objects.get(numar=masa_id)
            request.session["masa_id"] = masa.id
        except Masa.DoesNotExist:
            masa = None
            request.session.pop("masa_id", None)

    else:
        masa_param = request.session.get("masa_id")
        if masa_param:
            try:
                masa = Masa.objects.get(id=masa_param)
            except Masa.DoesNotExist:
                masa = None
                request.session.pop("masa_id", None)

    categorii = Categorie.objects.prefetch_related(
        "produse__imagini"
    ).order_by("ordine")

    ctx = {
        "categorii": categorii,
        "masa": masa,
    }

    return render(request, "demo/meniu.html", ctx)

def adauga_in_cos(request, produs_id):
    masa_id = request.session.get("masa_id")
    masa = Masa.objects.get(id=masa_id)
    produs = Produs.objects.get(id=produs_id)

    item, created = Cos.objects.get_or_create(
        masa=masa,
        produs=produs,
    )

    if not created:
        item.cantitate += 1
        item.save()

    return redirect("cos")

def cos(request):
    masa = None
    masa_id = request.session.get("masa_id")

    if not masa_id:
        return redirect("meniu")
    if masa_id:
        masa = Masa.objects.get(id=masa_id)
        items = Cos.objects.filter(masa=masa)
    else:
        items = []

    return render(request, "demo/cos.html", {"masa": masa, "items": items})

    
def adauga_din_cos(request, produs_id):
    masa_id = request.session.get("masa_id")
    if not masa_id:
        return redirect("meniu")

    masa = Masa.objects.get(id=masa_id)
    produs = Produs.objects.get(id=produs_id)

    item = Cos.objects.get(masa=masa, produs=produs)
    item.cantitate += 1
    item.save()

    return redirect("cos")


def scade_din_cos(request, produs_id):
    masa_id = request.session.get("masa_id")
    if not masa_id:
        return redirect("meniu")

    masa = Masa.objects.get(id=masa_id)
    produs = Produs.objects.get(id=produs_id)

    item = Cos.objects.get(masa=masa, produs=produs)
    item.cantitate -= 1

    if item.cantitate <= 0:
        item.delete()
    else:
        item.save()

    return redirect("cos")


def trimite_comanda(request):
    masa_id = request.session.get("masa_id")
    if not masa_id:
        return redirect("meniu")

    masa = Masa.objects.get(id=masa_id)
    items = Cos.objects.filter(masa=masa)

    if not items.exists():
        return redirect("cos")

    comanda = Comanda.objects.create(masa=masa)

    for item in items:
        ProdusComanda.objects.create(
            comanda=comanda,
            produs=item.produs,
            cantitate=item.cantitate,
            pret_unitar=item.produs.pret,
        )

    # șterge coșul după trimitere
    items.delete()

    return redirect("meniu")


def detalii_produs(request, produs_id):
    produs = get_object_or_404(Produs, id=produs_id)

    return render(request, "demo/produs.html", {
        "produs": produs
    })

    


# Create your views here.
