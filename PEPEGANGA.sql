DROP DATABASE IF EXISTS MODULO_INNOVACION;
CREATE DATABASE MODULO_INNOVACION CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE MODULO_INNOVACION;

-- Tabla de roles
CREATE TABLE rol (
    id_rol SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(20) NOT NULL
);

-- Tabla de usuarios
CREATE TABLE usuario (
    id_usuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(80) NOT NULL,
    num_documento CHAR(12) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contra_encript VARCHAR(140) NOT NULL,
    id_rol SMALLINT UNSIGNED NOT NULL,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

-- Índice adicional (recomendado)
CREATE INDEX idx_usuario_rol ON usuario(id_rol);

-- Tabla de proyectos
CREATE TABLE proyectos (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

-- Tabla de archivos
CREATE TABLE archivos (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_proyecto INT NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_almacenamiento VARCHAR(255) NOT NULL,
    fecha_carga DATE NOT NULL,
    fecha_informe DATE NOT NULL,
    responsable VARCHAR(255) NOT NULL,
    progreso INT NOT NULL,
    observacion TEXT,
    tamano_archivo VARCHAR(50) NOT NULL,
    version VARCHAR(50) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    codigo_sgps VARCHAR(100),
    nombre_centro VARCHAR(255),
    regional VARCHAR(100),
    responsables_proyecto TEXT,
    es_modificado BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Tabla de archivos modificados
CREATE TABLE archivos_modificados (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_archivo_original BIGINT NOT NULL,
    id_proyecto INT NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_almacenamiento VARCHAR(255) NOT NULL,
    fecha_subido DATE NOT NULL,
    fecha_informe DATE NOT NULL,
    responsable VARCHAR(255) NOT NULL,
    progreso INT NOT NULL,
    observacion TEXT,
    tamano_archivo VARCHAR(50) NOT NULL,
    version VARCHAR(50) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    codigo_sgps VARCHAR(100),
    nombre_centro VARCHAR(255),
    regional VARCHAR(100),
    responsables_proyecto TEXT,
    razon_modificado TEXT NOT NULL,
    FOREIGN KEY (id_archivo_original) REFERENCES archivos(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Índices recomendados extra
CREATE INDEX idx_archivos_proyecto ON archivos(id_proyecto);
CREATE INDEX idx_archivos_modificados_proyecto ON archivos_modificados(id_proyecto);
CREATE INDEX idx_archivos_modificados_original ON archivos_modificados(id_archivo_original);
