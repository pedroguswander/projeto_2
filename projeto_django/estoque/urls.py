from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('niveis/', niveis_view, name='niveis'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('', home_view, name='home'),
    path('brinquedos/', brinquedos_view, name='brinquedos'),
    path('brinquedos_cadastro/', brinquedos_cadastro_view, name='brinquedos_cadastro'),
    path('brinquedos/<brinquedo_id>/', brinquedo_view, name='brinquedo'),
    path('estoque/', estoque_view, name='estoque'),
    path('buscar_material/', buscar_material, name='buscar_material'),
    path('estoque_adicionar/', estoque_adicionar_view, name='estoque_adicionar'),
    path('pedidos/', pedidos_view, name='pedidos'),
    path('pedidos/<pedido_id>/', pedido_view, name='pedido'),
    path('pedidos_adicionar', pedido_adicionar_view, name='pedidos_adicionar'),
    path('feedbacks/<brinquedo_id>/', feedback_view, name='feedbacks'),
    path('feedback_adicionar/<pedido_id>/', feedback_adicionar_view, name='feedback_adicionar'),
    path('atualizar-estoque/<int:material_id>/', atualizar_estoque_view, name='atualizar_estoque'),
    path('registros-estoque/<int:material_id>/', registro_estoque_view, name='estoque_registro'),
    path('cliente_adicionar', cliente_adicionar_view, name='cliente_adicionar'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)