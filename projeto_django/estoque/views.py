from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from .models import Material, Brinquedo, material_de_um_brinquedo, Cliente, Pedido

def login_view(request) :
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('home')
    return render(request, 'estoque/login.html')

def cadastro_view(request) :
    pass

def home_view(request) :
    context = {}
    return render(request, 'estoque/home.html', context)

def brinquedos_view(request) :
    brinquedos = Brinquedo.objects.all()
    context = {'brinquedos' : brinquedos}
    return render(request, 'estoque/brinquedos.html', context)


def brinquedos_cadastro_view(request) :
    materiais = Material.objects.all()

    if request.method == 'POST':
        brinquedo = request.POST.get('brinquedo')
        descricao = request.POST.get('descricao')
        passo_a_passo = request.POST.get('passo a passo')
        imagem = request.POST.get('imagem')

        b = Brinquedo(
            brinquedo = brinquedo,
            descricao = descricao,
            passo_a_passo = passo_a_passo,
            imagem = imagem,
        )
        b.save()

        for material in materiais:
            if request.POST.get(f'material_{material.id}') == 'on':
                quantidade = request.POST.get(f'quantidade_{material.id}')
                if quantidade:
                    m = material_de_um_brinquedo(
                        brinquedo=b,
                        material=material.material,
                        quantidade=int(quantidade),
                    )
                    m.save()

        return redirect('brinquedos')
    
    context = {'materiais': materiais}
    return render(request, 'estoque/brinquedos_cadastro.html', context)

'''def brinquedo_view(request, brinquedo_id) :
    pode_produzir = True

    if request.method == 'POST':

        if request.POST.get('registro_brinquedo') == 'brinquedo' and pode_produzir:
            brinquedo = Brinquedo.objects.get(id = brinquedo_id)
            materiais = material_de_um_brinquedo.objects.filter(brinquedo = brinquedo)
            for material in materiais :
                material_do_estoque = Material.objects.get(material = material)
                material_do_estoque.quantidade -= material.quantidade
                material_do_estoque.save()

    preco_total = 0

    faltando = []

    brinquedo = Brinquedo.objects.get(id = brinquedo_id)
    materiais = material_de_um_brinquedo.objects.filter(brinquedo = brinquedo)
    for material in materiais :
        material_do_estoque = Material.objects.get(material = material)
        preco_total += material.quantidade * material_do_estoque.preco

        if material.quantidade > material_do_estoque.quantidade:
            pode_produzir = False
            faltando.append(f'{material}: faltam {material.quantidade - material_do_estoque.quantidade} itens, você possui {material_do_estoque.quantidade} item no estoque')

    
    context = {'brinquedo' : brinquedo, 'materiais' : materiais, 'preco_total' : preco_total,
            'pode_produzir' : pode_produzir, 'faltando' : faltando,}
    
    return render(request, 'estoque/brinquedo.html', context)'''

def brinquedo_view(request, brinquedo_id) :
    brinquedo = Brinquedo.objects.get(id = brinquedo_id)
    context = {'brinquedo': brinquedo}
    return render(request, 'estoque/brinquedo.html', context)

def estoque_view(request) :
    error_message = ''

    if request.method == 'POST' :
        if request.POST.get('pesquisa_material') == 'pesquisa_material':
            material = request.POST.get("pesquise por materiais")
            try:
                material_filtrado = Material.objects.get(material__iexact = material)
                return redirect('estoque_pesquisa', material_filtrado)
            
            except Material.DoesNotExist:
                error_message = 'Material não encontrado!'
            
    materiais = Material.objects.all()

    for material in materiais :
        material.valor = material.quantidade * material.preco

    context = {'materiais' : materiais, 'error_message': error_message}

    return render(request, 'estoque/estoque.html', context)

def estoque_pesquisa_view(request, material_id) :
    context = {'material_filtrado': material_id,}
    return render(request, 'estoque/estoque_pesquisa.html', context)

def estoque_adicionar_view(request) :
    if request.method == 'POST':
        if request.POST.get("registrar_material") == "registrar_material":
                material = request.POST.get('material')
                quantidade = request.POST.get('quantidade')
                preco = request.POST.get('preco')
                date_added = request.POST.get('date_added')

                m = Material(
                    material = material,
                    quantidade = quantidade,
                    preco = preco,
                    date_added = date_added,
                )

                m.save()
        
        return redirect('estoque')
            
    context = {}
    return render(request, 'estoque/estoque_adicionar.html', context)

def pedidos_view(request):
    pedidos = Pedido.objects.all()
    brinquedos = Brinquedo.objects.all()
    clientes = Cliente.objects.all()
    context = {'pedidos': pedidos, 'brinquedos': brinquedos, 'clientes': clientes}
    return render(request, 'estoque/pedidos.html', context)

def pedido_view(request, pedido_id):
    pode_produzir = True

    pedido = Pedido.objects.get(id = pedido_id)
    brinquedo = Brinquedo.objects.get(brinquedo = pedido.brinquedo)
    cliente = Cliente.objects.get(nome = pedido.cliente)
    materiais = material_de_um_brinquedo.objects.filter(brinquedo = pedido.brinquedo)
    
    if request.method == 'POST':
        data = request.POST
        action = data.get("producao")

        if action == 'ok':
            pedido.status = 'em andamento'
            pedido.save()
            return redirect('pedidos')
        
        if action == 'done':
            pedido.status = 'concluido'
            pedido.save()
            return redirect('pedidos')
   
    for material in materiais:
        material_do_estoque = Material.objects.get(material = material)
        if material.quantidade > material_do_estoque.quantidade:
            material.faltando = True
            pode_produzir = False

        else :
            material.faltando = False

    context = {'pedido': pedido, 'brinquedo': brinquedo, 'cliente': cliente, 'materiais': materiais, 'pode_produzir': pode_produzir}
    return render(request, 'estoque/pedido.html', context) 