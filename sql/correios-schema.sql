-- Database: correios

DROP DATABASE IF EXISTS correios;

CREATE DATABASE IF NOT EXISTS correios
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TABLE IF NOT EXISTS log_bairro
(
    bai_nu bigint NOT NULL,
    ufe_sg character(2) COLLATE pg_catalog."default" NOT NULL,
    loc_nu bigint NOT NULL,
    bai_no character varying(72) COLLATE pg_catalog."default" NOT NULL,
    bai_no_abrev character varying(36) COLLATE pg_catalog."default",
    CONSTRAINT bairro_pkey PRIMARY KEY (bai_nu)
);

CREATE TABLE IF NOT EXISTS log_cpc
(
    cpc_nu bigint NOT NULL,
    ufe_sg character(2) COLLATE pg_catalog."default" NOT NULL,
    loc_nu bigint NOT NULL,
    cpc_no character varying(72) COLLATE pg_catalog."default" NOT NULL,
    cpc_endereco character varying(100) COLLATE pg_catalog."default" NOT NULL,
    cep character(8) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT cpc_pkey PRIMARY KEY (cpc_nu)
);

CREATE TABLE IF NOT EXISTS log_faixa_bairro
(
    bai_nu bigint NOT NULL,
    fcb_cep_ini character(8) COLLATE pg_catalog."default" NOT NULL,
    fcb_cep_fim character(8) COLLATE pg_catalog."default",
    CONSTRAINT faixa_bairro_pkey PRIMARY KEY (bai_nu, fcb_cep_ini)
);

CREATE TABLE IF NOT EXISTS log_faixa_cpc
(
    cpc_nu bigint NOT NULL,
    cpc_inicial character varying(6) COLLATE pg_catalog."default" NOT NULL,
    cpc_final character varying(6) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT faixa_cpc_pkey PRIMARY KEY (cpc_nu, cpc_inicial)
);

CREATE TABLE IF NOT EXISTS log_faixa_localidade
(
    loc_nu bigint NOT NULL,
    loc_cep_ini character(8) COLLATE pg_catalog."default" NOT NULL,
    loc_cep_fim character(8) COLLATE pg_catalog."default" NOT NULL,
    loc_tipo_faixa character(1) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT faixa_localidade_pkey PRIMARY KEY (loc_nu, loc_cep_ini, loc_tipo_faixa)
);

CREATE TABLE IF NOT EXISTS log_faixa_uf
(
    ufe_sg character(2) COLLATE pg_catalog."default" NOT NULL,
    ufe_cep_ini character(8) COLLATE pg_catalog."default" NOT NULL,
    ufe_cep_fim character(8) COLLATE pg_catalog."default",
    CONSTRAINT faixa_uf_pkey PRIMARY KEY (ufe_sg, ufe_cep_ini)
);

CREATE TABLE IF NOT EXISTS log_faixa_uop
(
    uop_nu bigint NOT NULL,
    fnc_inicial bigint NOT NULL,
    fnc_final bigint NOT NULL,
    CONSTRAINT faixa_uop_pkey PRIMARY KEY (uop_nu, fnc_inicial)
);

CREATE TABLE IF NOT EXISTS log_grande_usuario
(
    gru_nu bigint NOT NULL,
    ufe_sg character(2) COLLATE pg_catalog."default" NOT NULL,
    loc_nu bigint NOT NULL,
    bai_nu bigint NOT NULL,
    log_nu bigint,
    gru_no character varying(72) COLLATE pg_catalog."default" NOT NULL,
    gru_endereco character varying(100) COLLATE pg_catalog."default" NOT NULL,
    cep character(8) COLLATE pg_catalog."default" NOT NULL,
    gru_no_abrev character varying(36) COLLATE pg_catalog."default",
    CONSTRAINT grande_usuario_pkey PRIMARY KEY (gru_nu)
);

CREATE TABLE IF NOT EXISTS log_localidade
(
    loc_nu bigint NOT NULL,
    ufe_sg character(2) COLLATE pg_catalog."default" NOT NULL,
    loc_no character varying(72) COLLATE pg_catalog."default" NOT NULL,
    cep character(8) COLLATE pg_catalog."default",
    loc_in_sit character(1) COLLATE pg_catalog."default" NOT NULL,
    loc_in_tipo_loc character(1) COLLATE pg_catalog."default" NOT NULL,
    loc_nu_sub bigint,
    loc_no_abrev character varying(36) COLLATE pg_catalog."default",
    mun_nu character(7) COLLATE pg_catalog."default",
    CONSTRAINT localidade_pkey PRIMARY KEY (loc_nu)
);

CREATE TABLE IF NOT EXISTS log_logradouro
(
    log_nu bigint NOT NULL,
    ufe_sg character(2) COLLATE pg_catalog."default" NOT NULL,
    loc_nu bigint NOT NULL,
    bai_nu_ini bigint NOT NULL,
    bai_nu_fim bigint,
    log_no character varying(100) COLLATE pg_catalog."default" NOT NULL,
    log_complemento character varying(100) COLLATE pg_catalog."default",
    cep character(8) COLLATE pg_catalog."default" NOT NULL,
    tlo_tx character varying(36) COLLATE pg_catalog."default" NOT NULL,
    log_sta_tlo character(1) COLLATE pg_catalog."default",
    log_no_abrev character varying(36) COLLATE pg_catalog."default",
    CONSTRAINT logradouro_pkey PRIMARY KEY (log_nu)
);

CREATE TABLE IF NOT EXISTS log_num_sec
(
    log_nu bigint NOT NULL,
    sec_nu_ini character varying(10) COLLATE pg_catalog."default" NOT NULL,
    sec_nu_fim character varying(10) COLLATE pg_catalog."default" NOT NULL,
    sec_in_lado character(1) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT num_sec_pkey PRIMARY KEY (log_nu)
);

CREATE TABLE IF NOT EXISTS ect_pais
(
    pai_sg character(2) COLLATE pg_catalog."default" NOT NULL,
    pai_sg_alternativa character(3) COLLATE pg_catalog."default" NOT NULL,
    pai_no_portugues character varying(72) COLLATE pg_catalog."default" NOT NULL,
    pai_no_ingles character varying(72) COLLATE pg_catalog."default",
    pai_no_frances character varying(72) COLLATE pg_catalog."default",
    pai_abreviatura character varying(36) COLLATE pg_catalog."default",
    CONSTRAINT pais_pkey PRIMARY KEY (pai_sg_alternativa)
);

CREATE TABLE IF NOT EXISTS log_unid_oper
(
    uop_nu bigint NOT NULL,
    ufe_sg character(2) COLLATE pg_catalog."default" NOT NULL,
    loc_nu bigint NOT NULL,
    bai_nu bigint NOT NULL,
    log_nu bigint,
    uop_no character varying(100) COLLATE pg_catalog."default" NOT NULL,
    uop_endereco character varying(100) COLLATE pg_catalog."default" NOT NULL,
    cep character(8) COLLATE pg_catalog."default" NOT NULL,
    uop_in_cp character(1) COLLATE pg_catalog."default" NOT NULL,
    uop_no_abrev character varying(36) COLLATE pg_catalog."default",
    CONSTRAINT unid_oper_pkey PRIMARY KEY (uop_nu)
);

CREATE TABLE IF NOT EXISTS log_var_bai
(
    bai_nu bigint NOT NULL,
    vdb_nu bigint NOT NULL,
    vdb_tx character varying(72) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT var_bai_pkey PRIMARY KEY (bai_nu, vdb_nu)
);

CREATE TABLE IF NOT EXISTS log_var_loc
(
    loc_nu bigint NOT NULL,
    val_nu bigint NOT NULL,
    val_tx character varying(72) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT var_loc_pkey PRIMARY KEY (loc_nu, val_nu)
);

CREATE TABLE IF NOT EXISTS log_var_log
(
    log_nu bigint NOT NULL,
    vlo_nu bigint NOT NULL,
    tlo_tx character varying(36) COLLATE pg_catalog."default" NOT NULL,
    vlo_tx character varying(150) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT var_log_pkey PRIMARY KEY (log_nu, vlo_nu)
);

ALTER TABLE log_faixa_localidade
ADD CONSTRAINT fk_faixa_localidade_loc_nu
FOREIGN KEY (loc_nu)
REFERENCES log_localidade(loc_nu);

ALTER TABLE log_var_loc
ADD CONSTRAINT fk_var_loc_loc_nu
FOREIGN KEY (loc_nu)
REFERENCES log_localidade(loc_nu);

ALTER TABLE log_grande_usuario
ADD CONSTRAINT fk_grande_usuario_log_nu
FOREIGN KEY (log_nu)
REFERENCES log_logradouro(log_nu);

ALTER TABLE log_num_sec
ADD CONSTRAINT fk_num_sec_log_nu
FOREIGN KEY (log_nu)
REFERENCES log_logradouro(log_nu);

ALTER TABLE log_var_log
ADD CONSTRAINT fk_var_log_log_nu
FOREIGN KEY (log_nu)
REFERENCES log_logradouro(log_nu);

ALTER TABLE log_faixa_uop
ADD CONSTRAINT fk_faixa_uop_uop_nu
FOREIGN KEY (uop_nu)
REFERENCES log_unid_oper(uop_nu);

ALTER TABLE log_unid_oper
ADD CONSTRAINT fk_unid_oper_log_nu
FOREIGN KEY (log_nu)
REFERENCES log_logradouro(log_nu);

ALTER TABLE log_unid_oper
ADD CONSTRAINT fk_unid_oper_bai_nu
FOREIGN KEY (bai_nu)
REFERENCES log_bairro(bai_nu);

ALTER TABLE log_unid_oper
ADD CONSTRAINT fk_unid_oper_loc_nu
FOREIGN KEY (loc_nu)
REFERENCES log_localidade(loc_nu);

ALTER TABLE log_faixa_bairro
ADD CONSTRAINT fk_faixa_bairro_bai_nu
FOREIGN KEY (bai_nu)
REFERENCES log_bairro(bai_nu);

ALTER TABLE log_var_bai
ADD CONSTRAINT fk_var_bai_bai_nu
FOREIGN KEY (bai_nu)
REFERENCES log_bairro(bai_nu);

ALTER TABLE log_bairro
ADD CONSTRAINT fk_bairro_loc_nu
FOREIGN KEY (loc_nu)
REFERENCES log_localidade(loc_nu);

ALTER TABLE log_faixa_cpc
ADD CONSTRAINT fk_faixa_cpc_cpc_nu
FOREIGN KEY (cpc_nu)
REFERENCES log_cpc(cpc_nu);

ALTER TABLE log_cpc
ADD CONSTRAINT fk_cpc_loc_nu
FOREIGN KEY (loc_nu)
REFERENCES log_localidade(loc_nu);

ALTER TABLE log_logradouro
ADD CONSTRAINT fk_logradouro_bai_nu_ini
FOREIGN KEY (bai_nu_ini)
REFERENCES log_bairro(bai_nu);

ALTER TABLE log_logradouro
ADD CONSTRAINT fk_logradouro_bai_nu_fim
FOREIGN KEY (bai_nu_fim)
REFERENCES log_bairro(bai_nu);

ALTER TABLE log_logradouro
ADD CONSTRAINT fk_logradouro_loc_nu
FOREIGN KEY (loc_nu)
REFERENCES log_localidade(loc_nu);

CREATE INDEX idx_log_faixa_bairro_cep_range
ON log_faixa_bairro (CAST(fcb_cep_ini AS bigint), CAST(fcb_cep_fim AS bigint));

CREATE INDEX idx_log_localidade_cep ON log_localidade(cep);

CREATE INDEX idx_log_localidade_loc_nu ON log_localidade(loc_nu);

CREATE INDEX idx_log_logradouro_loc_nu_cep ON log_logradouro(loc_nu, cep);

CREATE INDEX idx_log_logradouro_loc_nu ON log_logradouro(loc_nu);

CREATE INDEX idx_log_logradouro_log_nu ON log_logradouro(log_nu);

CREATE INDEX idx_log_num_sec_log_nu ON log_num_sec(log_nu);

CREATE INDEX idx_log_bairro_bai_nu ON log_bairro(bai_nu);
