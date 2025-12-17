from django.shortcuts import render, redirect, get_object_or_404
from .models import Categorie, Comanda, Masa, Produs, ProdusComanda

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

    
    categorii = Categorie.objects.prefetch_related("produse__imagini").order_by("ordine")
    ctx = {
        "categorii": categorii,
        "masa": masa
    }
    return render(request, "demo/meniu.html", ctx)

def adauga_in_cos(request, produs_id):
    masa_id = request.session.get("masa_id")
    if not masa_id:
        return redirect("meniu")

    cosuri = request.session.get("cosuri", {})
    cos = cosuri.get(str(masa_id), {})
    
    produs_id = str(produs_id)
    cos[produs_id] = cos.get(produs_id, 0) + 1
    
    cosuri[str(masa_id)] = cos
    request.session["cosuri"] = cosuri

    return redirect("meniu")

def cos(request):
    masa_id = request.session.get("masa_id")
    if not masa_id:
        return redirect("meniu")

    cosuri = request.session.get("cosuri", {})
    cos = cosuri.get(str(masa_id), {})

    produse = Produs.objects.filter(id__in=cos.keys())

    total = 0
    items = []

    for produs in produse:
        cantitate = cos[str(produs.id)]
        subtotal = cantitate * produs.pret
        total += subtotal

        items.append({
            "produs": produs,
            "cantitate": cantitate,
            "subtotal": subtotal
        })

    return render(request, "demo/cos.html", {
        "items": items,
        "total": total
    })
    
def adauga_din_cos(request, produs_id):
    masa_id = request.session.get("masa_id")
    if not masa_id:
        return redirect("meniu")

    cosuri = request.session.get("cosuri", {})
    cos = cosuri.get(str(masa_id), {})

    produs_id = str(produs_id)

    if produs_id in cos:
        cos[produs_id] += 1
    request.session["cosuri"]=cosuri
    return redirect("cos")

def scade_din_cos(request, produs_id):
    masa_id = request.session.get("masa_id")
    if not masa_id:
        return redirect("meniu")

    cosuri = request.session.get("cosuri", {})
    cos = cosuri.get(str(masa_id), {})

    produs_id = str(produs_id)

    if produs_id in cos:
        cos[produs_id] -= 1
        if cos[produs_id] <= 0:
            del cos[produs_id]
            
    request.session["cosuri"]=cosuri
    return redirect("cos")

def trimite_comanda(request):
    masa_id = request.session.get("masa_id")
    if not masa_id:
        return redirect("meniu")
    
    cosuri = request.session.get("cosuri",{})
    cos = cosuri.get(str(masa_id), {})
    
    if not cos:
        return redirect("cos")
    
    masa = Masa.objects.get(id=masa_id)
    
    comanda = Comanda.objects.create(masa=masa)
    
    produse = Produs.objects.filter(id__in=cos.keys())
    
    for produs in produse:
        ProdusComanda.objects.create(
            comanda=comanda,
            produs=produs,
            cantitate=cos[str(produs.id)],
            pret_unitar=produs.pret,
        )
        
    del cosuri[str(masa_id)]
    request.session["cosuri"]=cosuri
    
    return redirect ("meniu")

def detalii_produs(request, produs_id):
    produs = get_object_or_404(Produs, id=produs_id)

    return render(request, "demo/produs.html", {
        "produs": produs
    })

    


# Create your views here.
