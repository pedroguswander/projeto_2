describe('eu como usuário, gostaria de visualizar solicitações de produtos dadas pelos meus clientes', () => {

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

    it('Deve exibir uma lista com todos os pedidos ao acessar a aba de pedidos', () => {
        // Acessar a página inicial e navegar até a aba de pedidos
        cy.visit('/');
        cy.get('[href="/pedidos"]').click();

        // Verificar se a lista de pedidos está visível
        cy.contains('Código do Pedido: PEDIDO-01').should('be.visible');
        cy.contains('Código do Pedido: PEDIDO-02').should('be.visible');
    });


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
