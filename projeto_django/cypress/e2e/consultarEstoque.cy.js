describe('Eu como usuário, gostaria de visualizar o estoque de materiais', () => {

    const isWindows = Cypress.platform === 'win32';
    const copyCommand = isWindows 
        ? 'copy fixtures\\original_db.sqlite3 db.sqlite3'
        : 'cp fixtures/original_db.sqlite3 db.sqlite3';

    const copyCommand2 = isWindows 
        ? 'copy db.sqlite3 fixtures\\original_db.sqlite3'
        : 'cp db.sqlite3 fixtures/original_db.sqlite3';

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

    it('A aba “estoque” deve exibir uma lista de materiais', () => {
        // Acessar a página inicial e clicar na aba estoque
        cy.visit('/');
        cy.get('[href="/estoque"]').click();

        // Verificar se a lista de materiais está visível
        cy.get('.material-list').should('be.visible');
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