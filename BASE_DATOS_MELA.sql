DROP DATABASE IF EXISTS MODULO_INNOVACION;
CREATE DATABASE MODULO_INNOVACION CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE MODULO_INNOVACION;

-- Tabla de roles
CREATE TABLE rol (
    id_rol SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(20) NOT NULL
)ENGINE=InnoDB;

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
)ENGINE=InnoDB;

-- Índice adicional (recomendado)
CREATE INDEX idx_usuario_rol ON usuario(id_rol);

-- Tabla de proyectos
CREATE TABLE tipo_proyecto (
    id INT UNSIGNED NOT NULL  AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
)ENGINE=InnoDB;

-- Tabla de archivos
CREATE TABLE archivos (
    id BIGINT UNSIGNED NOT NULL  AUTO_INCREMENT PRIMARY KEY ,
    id_proyecto UNSIGNED INT NOT NULL,
    nombre_proyecto VARCHAR(255) NOT NULL,
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
    FOREIGN KEY (id_proyecto) REFERENCES tipo_proyecto(id)
        ON UPDATE CASCADE ON DELETE CASCADE
)ENGINE=InnoDB;

-- Tabla de archivos modificados
CREATE TABLE archivos_modificados (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    id_archivo_original BIGINT UNSIGNED NOT NULL,
    id_proyecto INT UNSIGNED NOT NULL,
    nombre_proyecto VARCHAR(255) NOT NULL,
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
    FOREIGN KEY (id_proyecto) REFERENCES tipo_proyecto(id)
        ON UPDATE CASCADE ON DELETE CASCADE
)ENGINE=InnoDB;

-- Índices recomendados extra
CREATE INDEX idx_archivos_proyecto ON archivos(id_proyecto);
CREATE INDEX idx_archivos_modificados_proyecto ON archivos_modificados(id_proyecto);




INSERT INTO rol (id_rol, nombre_rol) VALUES 
(1,'Administrador'),
(2,'Editor'),
(3,'Usuario');
