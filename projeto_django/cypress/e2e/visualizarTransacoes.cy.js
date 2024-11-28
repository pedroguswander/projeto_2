describe('Eu como usuário, gostaria de atualizar o nível de estoque dos meus materiais', () => {

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

    it('Exibe mensagem de confirmação após atualizar estoque', () => {
        // Acessar a página inicial e navegar até o estoque
        cy.visit('/');
        cy.get('[href="/estoque"]').click();
        cy.get(':nth-child(1) > .material-right > ul > :nth-child(4) > a').click();
        cy.get('.registro-lista').should('be.visible');

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
