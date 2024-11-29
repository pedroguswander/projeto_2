describe('eu como usuário, gostaria de registrar o feedback dos clientes após o envio do produto', () => {

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

        it('Deve registrar e exibir o feedback corretamente na lista de feedbacks do brinquedo', () => {
          // Passo 1: Acessar a página de pedidos
          cy.visit('/pedidos'); 
      
          // Passo 2: Localizar o pedido 03 e clicar para adicionar um feedback
          cy.get(':nth-child(4) > .pedido-item-center > :nth-child(2) > .button-class').click()

          cy.get('.button-class').click()


      
          // Passo 3: Preencher o formulário de feedback
          cy.get('input[name="titulo"]').type('Excelente produto!');
          cy.get('textarea[name="descricao"]').type('O produto atendeu todas as minhas expectativas.');
          cy.get('button[type="submit"]').click(); // Envia o feedback
      
          // Passo 4: Ir para a página de brinquedos
          cy.visit('/brinquedos'); 
      
          // Passo 5: Localizar o brinquedo relacionado ao pedido 03
          cy.get('[href="/feedbacks/7/"]').click()
      
          // Passo 6: Verificar se o feedback que foi registrado aparece na lista de feedbacks do brinquedo
          cy.get('.feedback-container').within(() => {
            // Verifica se o feedback registrado aparece corretamente
            cy.contains('Excelente produto!').should('be.visible');
            cy.contains('O produto atendeu todas as minhas expectativas.').should('be.visible');
          });
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