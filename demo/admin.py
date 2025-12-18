from django.contrib import admin
from .models import Masa, Categorie, Produs, ImagineProdus, Comanda, ProdusComanda, Cos

class ImagineProdusInline(admin.TabularInline):
    model = ImagineProdus
    extra = 1

@admin.register(Produs)
class ProdusAdmin(admin.ModelAdmin):
    list_display = ("nume", "categorie", "pret", "disponibil")
    list_filter = ("categorie", "disponibil")
    search_fields = ("nume",)
    inlines = [ImagineProdusInline]

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("iconita", "nume", "ordine")
    ordering = ("ordine",)

@admin.register(Masa)
class MasaAdmin(admin.ModelAdmin):
    list_display = ("numar",)
    ordering = ("numar",)

class ProdusComandaInline(admin.TabularInline):
    model = ProdusComanda
    extra = 1
    
@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ("id", "masa", "data_creare")
    search_fields = ("id",)
    inlines = [ProdusComandaInline]
    readonly_fields = ("data_creare",)

@admin.register(ProdusComanda)
class ProdusComandaAdmin(admin.ModelAdmin):
    list_display = ("comanda", "produs", "cantitate", "pret_unitar")
    
@admin.register(Cos)
class CosAdmin(admin.ModelAdmin):
    list_display = ("masa", "produs", "cantitate")


# Register your models here.
