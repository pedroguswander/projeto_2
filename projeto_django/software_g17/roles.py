from rolepermissions.roles import AbstractUserRole

class Danielle(AbstractUserRole) :
    avaible_permissions = {' '}

class Funcionaria(AbstractUserRole):
    avaible_permissions = {' '}

class Administrador(AbstractUserRole):
    avaible_permissions = {'registrar_brinquedos': True, 'registrar_materiais': True, 'editar_materiais': True, 'registrar_clientes': True}