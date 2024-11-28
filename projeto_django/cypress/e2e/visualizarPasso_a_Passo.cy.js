describe('Eu como usuário, gostaria de visualizar o passo a passo para produzir um brinquedo', () => {

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

    it('Exibe a descrição do passo a passo ao clicar no botão', () => {
        // Acessar a página inicial e navegar até o processo de criação de um brinquedo
        cy.visit('/');
        cy.get('[href="/brinquedos"]').click();
    
        // Selecionar um brinquedo e acessar o processo de criação
        cy.get(':nth-child(1) > .button-class').contains('Processo de criação').click();
    
        // Verificar se a string de descrição está visível ao clicar no botão de "Descrição do Passo a Passo"
        cy.get('summary').contains('Descrição do Passo a Passo').click(); // Clicar para expandir
        cy.get('.receita-card > p').should('be.visible'); // Verificar se a string está visível
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
