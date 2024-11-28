from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from .models import Material, Brinquedo, material_de_um_brinquedo, Cliente, Pedido, Feedback, Registro_de_Transacoes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


def login_view(request) :
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('home')
        

    context = {}
    
    return render(request, 'estoque/login.html', context)

def cadastro_view(request) :
    pass

def home_view(request) :
    try:
        User.objects.get(username = 'danielle') and User.objects.get(username = 'artesa1')
    
    except:
        usuario1 = User.objects.create_user(username= 'danielle', password= "123")
        usuario2 = User.objects.create_user(username= 'artesa1', password= "123")
        usuario1.save()
        usuario2.save()

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

def brinquedo_view(request, brinquedo_id) :
    brinquedo = Brinquedo.objects.get(id = brinquedo_id)
    materiais = material_de_um_brinquedo.objects.filter(brinquedo = brinquedo.id)
    context = {'brinquedo': brinquedo, 'materiais': materiais}
    return render(request, 'estoque/brinquedo.html', context)

from django.db.models import Q

def estoque_view(request):
    error_message = ''
    query = request.GET.get('q')
    if query:
        materiais = Material.objects.filter(
            Q(material__icontains=query) | Q(descricao__icontains=query)
        )
        if not materiais.exists():
            error_message = 'Nenhum material encontrado para a busca.'
    else:
        materiais = Material.objects.all()

    for material in materiais:
        material.valor = material.quantidade * material.preco

    context = {
        'materiais': materiais,
        'error_message': error_message,
    }
    return render(request, 'estoque/estoque.html', context)


def estoque_pesquisa_view(request, material_id) :
    context = {'material_filtrado': material_id,}
    return render(request, 'estoque/estoque_pesquisa.html', context)


def buscar_material(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX Request
        query = request.GET.get('term', '')
        materiais = Material.objects.filter(material__icontains=query)
        resultados = [{'id': mat.id, 'label': mat.material} for mat in materiais]
        return JsonResponse(resultados, safe=False)

    return JsonResponse({'error': 'Método inválido'}, status=400)

def estoque_adicionar_view(request) :
    if request.method == 'POST':
        if request.POST.get("registrar_material") == "registrar_material":
                material = request.POST.get('material')
                codigo = request.POST.get('codigo')
                descricao = request.POST.get('descricao')
                quantidade = request.POST.get('quantidade')
                preco = request.POST.get('preco')

                m = Material(
                    material = material,
                    codigo = codigo,
                    descricao = descricao,
                    quantidade = quantidade,
                    preco = preco,
                )

                m.save()
        
        return redirect('estoque')
            
    context = {}
    return render(request, 'estoque/estoque_adicionar.html', context)

def atualizar_estoque_view(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    mensagem = ''
    erro = False

    if request.method == 'POST':
        quantidade_atualizada = request.POST.get('quantidade')
        try:
            quantidade_atualizada = int(quantidade_atualizada)
            nova_quantidade = material.quantidade + quantidade_atualizada
            
            if nova_quantidade < 0:
                mensagem = "Erro: A quantidade no estoque não pode ser negativa."
                erro = True
            else:
                material.quantidade = nova_quantidade
                material.save()
                mensagem = "Estoque atualizado com sucesso!"
        except ValueError:
            mensagem = "Por favor, insira uma quantidade válida."
            erro = True

    context = {
        'material': material,
        'mensagem': mensagem,
        'erro': erro,
    }
    return render(request, 'estoque/estoque_atualizar.html', context)


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
            for material in materiais:
                material_do_estoque = Material.objects.get(material = material)
                if material_do_estoque.quantidade >= material.quantidade:
                    material_do_estoque.quantidade -= material.quantidade
                    material_do_estoque.save()

                    material_registrado = Material.objects.get(material = material_do_estoque)

                    registro = Registro_de_Transacoes(
                        registro = 'REGISTRO' + str(material_registrado.id),
                        pedido = pedido,
                        brinquedo = brinquedo,
                        material = material_registrado,
                        quantidade = material.quantidade,
                    )

                    registro.save()

            pedido.status = 'em andamento'
            pedido.save()
            return redirect('pedidos')
        
        if action == 'done':
            pedido.status = 'concluido'
            pedido.save()
            return redirect('pedidos')
        
        if action == 'cancel':
            for material in materiais:
                material_do_estoque = Material.objects.get(material = material)
                material_do_estoque.quantidade += material.quantidade
                material_do_estoque.save()

            pedido.status = 'pendente'
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

def feedback_view(request, brinquedo_id):
    feedbacks = Feedback.objects.all()
    brinquedo = Brinquedo.objects.get(id = brinquedo_id)
    pedidos = Pedido.objects.filter(brinquedo = brinquedo)

    context = {'feedbacks': feedbacks ,'pedidos': pedidos, 'brinquedo': brinquedo,}
    return render(request, 'estoque/feedbacks.html', context)

def feedback_adicionar_view(request, pedido_id):
    pedido = Pedido.objects.get(id = pedido_id)
    cliente = Cliente.objects.get(nome = pedido.cliente)

    if request.method == 'POST':
        data = request.POST
        action = data.get("feedback")

        if action == "enviar":
            titulo = data.get('titulo')
            descricao = data.get('descricao')
            #obj_pedido = Feedback.objects.get(pedido = pedido)
            feedback = Feedback(
                titulo = titulo,
                descricao = descricao,
                pedido = pedido,
            )

            feedback.save()

    context = {'pedido': pedido, 'cliente': cliente}

    return render(request, 'estoque/feedback_adicionar.html', context)

def registro_estoque_view(request, material_id):
    registros = Registro_de_Transacoes.objects.filter(material = material_id)
    material = Material.objects.get(id = material_id)
    context = {'registros': registros, 'material': material}
    return render(request, 'estoque/estoque_registro.html', context)

def niveis_view(request):
    if request.method == 'POST':
        data = request.POST
        action = data.get("nivel")

        if action == 'adm': #assign roles
            return redirect('login')

        #if action == 'artesa':
            return redirect('login')

    return render(request, 'estoque/niveis.html')
