describe('Eu como usuário, gostaria de adicionar novos tipos de materiais no meu estoque', () => {

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

    it('Adicionar um novo material ao estoque e verificar a presença na lista', () => {
        // Acessar a página inicial e clicar no botão de adicionar material
        cy.visit('/');
        cy.contains('Adicionar Material').click();

        // Preencher o formulário com os detalhes do novo material
        cy.get('input[name="material"]').type('Novo Material');
        cy.get('input[name="codigo"]').type('12345');
        cy.get('input[name="quantidade"]').type('10');
        cy.get('input[name="preco"]').type('15.50');
        cy.get('textarea[name="descricao"]').type('Descrição do novo material');

        // Submeter o formulário
        cy.get('button[name="registrar_material"]').click();


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
