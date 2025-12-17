from django.urls import path
from . import views
urlpatterns = [
	path("", views.meniu, name="meniu"),
    path("masa/<int:masa_id>/", views.meniu, name="meniu_masa"),
    path("adauga/<int:produs_id>/", views.adauga_in_cos, name="adauga_in_cos"),
    path("cos/", views.cos, name="cos"),
    path("adauga2/<int:produs_id>/", views.adauga_din_cos, name="adauga_din_cos"),
    path("scade/<int:produs_id>/", views.scade_din_cos, name="scade_din_cos"),
    path("get_cos_curent/", views.get_cos_curent, name="get_cos_curent"),
    path("trimite/", views.trimite_comanda, name="trimite_comanda"),
    path("produs/<int:produs_id>/", views.detalii_produs, name="detalii_produs"),
    

]
