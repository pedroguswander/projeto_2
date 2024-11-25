from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('login', login_view, name='login'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('', home_view, name='home'),
    path('brinquedos/', brinquedos_view, name='brinquedos'),
    path('brinquedos_cadastro/', brinquedos_cadastro_view, name='brinquedos_cadastro'),
    path('brinquedos/<brinquedo_id>/', brinquedo_view, name='brinquedo'),
    path('estoque/', estoque_view, name='estoque'),
    path('estoque_pesquisa/<material_id>/', estoque_pesquisa_view, name='estoque_pesquisa'),
    path('estoque_adicionar/', estoque_adicionar_view, name='estoque_adicionar'),
    path('pedidos/', pedidos_view, name='pedidos'),
    path('pedidos/<pedido_id>/', pedido_view, name='pedido'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)