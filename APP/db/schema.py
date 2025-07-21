
instruccion = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS logs_actividad;',
    'DROP TABLE IF EXISTS mantenimientos;',
    'DROP TABLE IF EXISTS permisos;',
    'DROP TABLE IF EXISTS Equipos;',
    'DROP TABLE IF EXISTS categorias;',
    'DROP TABLE IF EXISTS ubicaciones;',
    'DROP TABLE IF EXISTS users;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
    CREATE TABLE users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL DEFAULT 'lector'
    );
    """,
    """
    CREATE TABLE categorias (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE ubicaciones (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL UNIQUE,
        descripcion TEXT
    );
    """,
    """
    CREATE TABLE Equipos (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        created_by INT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        usuario VARCHAR(50) NOT NULL,
        marca VARCHAR(255) NOT NULL,
        modelo VARCHAR(255) NOT NULL,
        numero_serie VARCHAR(50) NOT NULL,
        numero_parte VARCHAR(50) NOT NULL,
        estado VARCHAR(20) NOT NULL,
        sistema_operativo VARCHAR(50) NOT NULL,
        version_bios VARCHAR(50) NOT NULL,
        categoria_id INT,
        ubicacion_id INT,
        FOREIGN KEY (created_by) REFERENCES users(id),
        FOREIGN KEY (categoria_id) REFERENCES categorias(id),
        FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(id)
    );
    """,
    """
    CREATE TABLE mantenimientos (
        id INT PRIMARY KEY AUTO_INCREMENT,
        equipo_id INT NOT NULL,
        realizado_por INT NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        descripcion TEXT,
        FOREIGN KEY (equipo_id) REFERENCES Equipos(id),
        FOREIGN KEY (realizado_por) REFERENCES users(id)
    );
    """,
    """
    CREATE TABLE logs_actividad (
        id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        accion VARCHAR(255) NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """,
    """
    CREATE TABLE permisos (
        id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        modulo VARCHAR(100) NOT NULL,
        permiso VARCHAR(50) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """
]
