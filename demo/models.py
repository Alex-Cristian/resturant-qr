from django.db import models


class Masa(models.Model):
    numar = models.IntegerField(unique=True)

    def __str__(self):
        return f"Masa {self.numar}"


class Categorie(models.Model):
    nume = models.CharField(max_length=50)
    iconita = models.CharField(
        max_length=10,
        blank=True,
        help_text="Ex: 🍕 🍝 🥤 🍰"
    )
    ordine = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.iconita} {self.nume}"



class Produs(models.Model):
    categorie = models.ForeignKey(
        Categorie,
        related_name="produse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    nume = models.CharField(max_length=100)
    pret = models.DecimalField(max_digits=6, decimal_places=2)
    disponibil = models.BooleanField(default=True)
    ingrediente = models.CharField(max_length=1000, blank=True)
    valori_nutritionale = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.nume


class ImagineProdus(models.Model):
    produs = models.ForeignKey(
        Produs,
        related_name="imagini",
        on_delete=models.CASCADE
    )
    imagine = models.ImageField(upload_to="produse/")

    def __str__(self):
        return f"Imagine pentru {self.produs.nume}"


class Comanda(models.Model):
    masa = models.ForeignKey(Masa, on_delete=models.CASCADE)
    data_creare = models.DateTimeField(auto_now_add=True)
    finalizata = models.BooleanField(default=False)
    observatii = models.TextField(blank=True)

    def __str__(self):
        return f"Comanda #{self.id} - Masa {self.masa.numar}"


class ProdusComanda(models.Model):
    comanda = models.ForeignKey(
        Comanda,
        related_name="pozitii",
        on_delete=models.CASCADE
    )
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    cantitate = models.IntegerField()
    pret_unitar = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.produs.nume} x{self.cantitate}"
