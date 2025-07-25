create table prefeitos (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cidade_id int UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY (cidade_id),
    FOREIGN KEY (cidade_id) references cidades (id)
);