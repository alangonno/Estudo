-- INSERT INTO cidades (nome, area, estado_id)
-- VALUE ('Campinas', 795, 33);

-- INSERT INTO cidades (nome, area, estado_id)
-- VALUES ('Niteroi', 133.9, 25);

-- INSERT INTO cidades 
--     (nome, area, estado_id)
-- VALUES(
--     'Caruaru', 
--     965.2, 
--     (select id from estados where sigla = 'PE')
--     )

INSERT INTO cidades
    (nome, area, estado_id)
VALUES (
    'Volta Redonda', 
    200.3, 
    (select id from estados where sigla = 'RJ')
    )