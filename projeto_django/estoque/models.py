from django.db import models

class Brinquedo(models.Model) :
    brinquedo = models.CharField(max_length=50, blank=True)
    quantidade = models.IntegerField(blank=True, null=True)
    codigo = models.CharField(max_length=10)
    descricao = models.TextField()
    passo_a_passo = models.TextField()
    imagem = models.ImageField(blank= True, default='boneca.png')

    def __str__(self) :
        return self.brinquedo

class material_de_um_brinquedo(models.Model) :
    brinquedo = models.ForeignKey(Brinquedo, on_delete=models.CASCADE, related_name='Brinquedo', null=True)
    material = models.CharField(max_length=20)
    quantidade = models.IntegerField()

    def __str__(self) :
        return self.material

class Material(models.Model) :
    material = models.CharField(max_length=20)
    codigo = models.CharField(max_length = 12, blank= True)
    descricao = models.TextField(max_length= 100, blank= True)
    quantidade = models.IntegerField()
    preco = models.FloatField()
    date_added = models.DateTimeField(null=True, auto_now_add= True)
    date_exit = models.DateTimeField(null=True, blank= True)
    imagem = models.ImageField(blank= True, default='logo_do_instoky.png')

    def __str__(self):
        return self.material
    
class Cliente(models.Model) :
    nome = models.CharField(max_length=20, null= True, blank= True)
    cpf = models.CharField(max_length = 14, blank= True)
    contato = models.EmailField()
    endereco = models.CharField(max_length=60, null= True, blank= True)
    feedback = models.TextField(null= True, blank= True)

    def __str__(self):
        return self.nome

class Pedido(models.Model) :
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em andamento', 'Em andamento'),
        ('concluido', 'Concluído'),
    ]

    codigo = models.CharField(max_length = 12, blank= True)
    brinquedo = models.ForeignKey(Brinquedo, on_delete=models.CASCADE, related_name='brinquedo_de_um_pedido', null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name = 'cliente', null= True)
    descricao = models.TextField(max_length= 200, blank= True)
    status = models.CharField(max_length=20,  choices= STATUS_CHOICES , default= 'pendente')
    data_de_solicitacao = models.DateField(null= True, blank= True)
    data_de_entrega = models.DateField(null= True, blank= True)

    def __str__(self):
        return self.codigo
    
class Feedback(models.Model) :
    titulo = models.CharField(max_length=20)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='feedback', null=True)
    #brinquedo = models.ForeignKey(Brinquedo, on_delete=models.CASCADE, related_name='brinquedo_de_um_feedback', null=True)
    descricao = models.TextField(max_length=500, blank=True, null= True)
    data_de_escrita = models.DateField(auto_now_add=True)
    estrelas = models.IntegerField(blank= True, null= True)
    
    def __str__(self):
        return self.titulo
    
class Registro_de_Transacoes(models.Model):
    registro =  models.CharField(max_length = 12, blank= True, null= True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material_saida_chegada', null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='pedido_saida_chegada', null=True)
    brinquedo = models.ForeignKey(Brinquedo, on_delete=models.CASCADE, related_name='brinquedo_saida_chegada', null=True, blank= True)
    quantidade = models.IntegerField()
    data_de_saida = models.DateField(auto_now_add=True)
    razao = models.TextField(max_length= 200, null= True, blank= True)

    def __str__(self):
        return self.registro