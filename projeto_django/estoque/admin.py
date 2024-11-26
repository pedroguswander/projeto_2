from django.contrib import admin
from .models import Material, Brinquedo, material_de_um_brinquedo, Cliente, Pedido, Feedback

admin.site.register(Material)
admin.site.register(Brinquedo)
admin.site.register(material_de_um_brinquedo)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Feedback)
