CREATE DATABASE projeto_integrador;
USE projeto_integrador;

CREATE TABLE ELEITORES(
	id int auto_increment PRIMARY KEY,
	nome_completo varchar(50) not null,
	titulo_eleitor varchar(12) not null unique, 
	cpf varchar(50) not null unique,
	mesário boolean not null,
	chave_acesso varchar(50) not null,
	votou boolean default false
);

CREATE TABLE CANDIDATOS(
	id int auto_increment primary key,
	nome varchar(50) not null,
	numerodevotacao varchar(50) not null unique, 
	partido varchar(30) not null,
	sigla_partido varchar(10) not null
);

CREATE TABLE VOTOS(
	id INT AUTO_INCREMENT PRIMARY KEY,
	candidato_id INT, 
	data_hora DATETIME NOT NULL,
	protocolo VARCHAR(50) NOT NULL,
	FOREIGN KEY (candidato_id) REFERENCES Candidatos(id)
);

INSERT INTO CANDIDATOS (nome, numerodevotacao, partido, sigla_partido) VALUES 
('Ana Silva', '12345', 'SIX SEVEN', 'SS'),
('Bruno Souza', '54321', 'RESENHAXX', 'RX'),
('Carla Dias', '99888', 'COMIDA MINEIRA', 'CM');

INSERT INTO Eleitores (nome_completo, titulo_eleitor, cpf, mesário, chave_acesso) VALUES 
('Joyce Cardoso', '111222333444', '12345678901', false, 'XYZ123'),
('Arthur Gomes', '555666777888', '98765432100', true, 'ABC789'),
('João Firmino', '999000111222', '11122233344', false, 'KEY456');

INSERT INTO Votos (candidato_id, data_hora, protocolo) VALUES 
(1, NOW(), 'PROT-2026-001'),
(2, NOW(), 'PROT-2026-002'),
(1, NOW(), 'PROT-2026-003'); 

SELECT * FROM votos;
SELECT * FROM candidatos;
SELECT * FROM eleitores;

ALTER TABLE ELEITORES MODIFY COLUMN cpf VARCHAR(50);
ALTER TABLE ELEITORES MODIFY COLUMN chave_acesso VARCHAR(50);
ALTER TABLE VOTOS DROP FOREIGN KEY votos_ibfk_2;
ALTER TABLE VOTOS DROP COLUMN eleitor_id;
