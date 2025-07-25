select 
    e.nome as Estado,
    c.nome as Cidades,
    regiao as Região
from estados e
    inner join cidades c
on e.id = c.estado_id;
