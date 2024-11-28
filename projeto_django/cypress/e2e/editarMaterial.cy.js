describe('Eu como usuário, gostaria de atualizar o nível de estoque dos meus materiais', () => {

    const isWindows = Cypress.platform === 'win32'; // Detecta o sistema operacional
    const copyCommand = isWindows 
        ? 'copy fixtures\\original_db.sqlite3 db.sqlite3' // Para Windows
        : 'cp fixtures/original_db.sqlite3 db.sqlite3';   // Para Linux/Mac

    before(() => {
        // Copia o banco de dados original para db.sqlite3
        cy.exec(copyCommand, { failOnNonZeroExit: false })
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

        // Atualizar o estoque e verificar mensagem de confirmação
        cy.get(':nth-child(1) > .material-right > .add-button').click();
        cy.get('[type="number"]').type(5); // Adiciona 5 unidades
        cy.get('button').click(); // Confirma
        cy.contains('Estoque atualizado com sucesso!').should('be.visible'); // Verifica a mensagem
    });

    it('Impede que a quantidade no estoque fique negativa', () => {
        // Acessar a página inicial e navegar até o estoque
        cy.visit('/');
        cy.get('[href="/estoque"]').click();

        // Seleciona o primeiro material da lista e obtém a quantidade atual
        cy.get(':nth-child(1) > .material-right > ul > :nth-child(1)').then(($el) => {
            const textoQuantidade = $el.text(); // Exemplo: "Quantidade no estoque: 3"
            const quantidadeAtual = parseInt(textoQuantidade.match(/\d+/)[0]); // Extrai o número

            // Atualizar o estoque com um valor que faz o total ficar negativo
            cy.get(':nth-child(1) > .material-right > .add-button').click();
            const quantidadeNegativa = -(quantidadeAtual + 1); // Garante que o saldo final será negativo
            cy.get('[type="number"]').type(quantidadeNegativa); // Insere o valor
            cy.get('button').click(); // Tenta confirmar

            // Verifica se a mensagem de erro é exibida
            cy.contains('Erro: A quantidade no estoque não pode ser negativa.').should('be.visible');
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
