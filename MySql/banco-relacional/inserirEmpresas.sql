INSERT INTO empresas (nome, cnpj)

VALUES
    ('Bradesco', 9238246238642432),
    ('Itau', 9238246212313123),
    ('Nubank', 9238246238642324);

ALTER TABLE empresas MODIFY cnpj VARCHAR(20);

insert into empresas_unidades 
    (empresa_id, cidade_id, sede)

values 
    (1, 7, 0),
    (1, 2, 1),
    (2, 3, 1),
    (2, 4, 0),
    (3, 2, 1),
    (3, 3, 0);

    