
describe('Eu como usuário, gostaria de marcar pedidos como "em produção"', () => {

    const isWindows = Cypress.platform === 'win32'; // Detecta o sistema operacional
    const copyCommand = isWindows 
        ? 'copy fixtures\\original_db.sqlite3 db.sqlite3' // Para Windows
        : 'cp fixtures/original_db.sqlite3 db.sqlite3';   // Para Linux/Mac

    const copyCommand2 = isWindows 
        ? 'copy db.sqlite3 fixtures\\original_db.sqlite3' // Para Windows
        : 'cp db.sqlite3 fixtures/original_db.sqlite3';   // Para Linux/Mac

    before(() => {
        // Copia o banco de dados original para db.sqlite3
        cy.exec(copyCommand2, { failOnNonZeroExit: false })
            .then(result => {
                cy.log('Banco de dados restaurado a partir do fixture:', result.stdout || result.stderr);
                expect(result.code).to.eq(0, 'Falha ao restaurar o banco de dados do fixture');
            });
        
        // Executa as migrações para garantir consistência
        cy.exec('python3 manage.py makemigrations', { failOnNonZeroExit: false })
            .then(result => cy.log('Execução do comando makemigrations:', result.stdout || result.stderr));
        
        cy.exec('python3 manage.py migrate', { failOnNonZeroExit: false })
            .then(result => cy.log('Execução do comando migrate:', result.stdout || result.stderr));
    });

    it('Exibe mensagem de aviso quando não é possível produzir o pedido requisitado', () => {
            // Acessar a página inicial
            cy.visit('/');
            cy.get('[href="/pedidos"]').click()
        
            // Procurar pelo pedido com o nome "PEDIDO-02" e clicar no card de detalhes da entrega
            cy.get(':nth-child(3) > .pedido-item-center > :nth-child(2) > .button-class').click()
        
            // Verificar se a mensagem "Não é possível produzir o pedido." está visível
            cy.contains('Não é possível produzir o pedido.').should('be.visible');
        });

    it('Se for possível produzir o produto requisitado no pedido, ao clicar no botão de “Iniciar produção”, o status do pedido deve ser modificado para “em andamento”', () => {
            // Acessar a página inicial
            cy.visit('/');
            cy.get('[href="/pedidos"]').click();
        
            // Clicar no último botão de detalhes da entrega
            cy.get('.pedido-item:last-child .button-class').click();
        
            // Verificar se está na página do pedido e o botão "Iniciar produção" está visível
            cy.contains('Iniciar produção').should('be.visible');
        
            // Clicar no botão "Iniciar produção"
            cy.contains('Iniciar produção').click();
        
            // Verificar se o status foi atualizado para "em andamento"
            cy.contains('Status: em andamento').should('be.visible');
    });

    it('Ao clicar em cancelar um pedido que está marcado como “em andamento”,  o status do pedido deve mudar para “pendente”', () => {
        // Acessar a página inicial
        cy.visit('/');
        cy.get('[href="/pedidos"]').click();
    
        // Clicar no último botão de detalhes da entrega
        cy.get(':nth-child(2) > .pedido-item-center > :nth-child(2) > .button-class').click();
        cy.get('#button-cancel').click()
        cy.get(':nth-child(2) > .pedido-item-left > p').invoke('text').should('have.string', 'pendente')
    
});

it('Ao clicar em concluir um pedido que está marcado como “em andamento”,  o status do pedido deve mudar para “concluído”', () => {
    // Acessar a página inicial
    cy.visit('/');
    cy.get('[href="/pedidos"]').click();

    // Clicar no último botão de detalhes da entrega
    cy.get(':nth-child(2) > .pedido-item-center > :nth-child(2) > .button-class').click();
    cy.get(':nth-child(1) > .btn').click()
    cy.get(':nth-child(2) > .pedido-item-left > p').invoke('text').should('have.string', 'concluido')

});
        

    afterEach(() => {
        cy.exec(copyCommand, { failOnNonZeroExit: false });
    })
        
    after(() => {
        // Restaura o banco de dados original para garantir limpeza
        cy.exec(copyCommand, { failOnNonZeroExit: false })
            .then(result => {
                cy.log('Banco de dados restaurado para o estado original:', result.stdout || result.stderr);
                expect(result.code).to.eq(0, 'Falha ao restaurar o banco de dados original');
            });

        // Verifica se o arquivo foi restaurado corretamente
    });

});
