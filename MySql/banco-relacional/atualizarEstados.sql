update estados
set nome = 'Errejota', 
    populacao = 20.2 
where sigla = 'RJ';

select nome, populacao from estados est where sigla = 'RJ'; 
