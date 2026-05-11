-- ============================================================
-- BASE DE DATOS: hotel
-- Usuario: root  |  Contraseña: hugo$
-- Sistema de microservicios de reservas de hotel
-- ============================================================

CREATE DATABASE IF NOT EXISTS hotel
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE hotel;

-- ============================================================
-- auth_service: tabla de usuarios del sistema
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id               INT          NOT NULL AUTO_INCREMENT,
    username         VARCHAR(100) NOT NULL,
    hashed_password  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username),
    INDEX idx_users_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- rooms_service: habitaciones del hotel
-- ============================================================
CREATE TABLE IF NOT EXISTS rooms (
    id              INT         NOT NULL AUTO_INCREMENT,
    number          VARCHAR(20) NOT NULL,
    type            VARCHAR(50) NOT NULL,
    price_per_night FLOAT       NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_rooms_number (number),
    INDEX idx_rooms_number (number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- guests_service: huespedes registrados
-- ============================================================
CREATE TABLE IF NOT EXISTS guests (
    id         INT          NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,
    email      VARCHAR(255) NOT NULL,
    phone      VARCHAR(20)  DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_guests_email (email),
    INDEX idx_guests_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- reservations_service: reservaciones
-- ============================================================
CREATE TABLE IF NOT EXISTS reservations (
    id          INT         NOT NULL AUTO_INCREMENT,
    guest_id    INT         NOT NULL,
    room_id     INT         NOT NULL,
    check_in    DATE        NOT NULL,
    check_out   DATE        NOT NULL,
    total_price FLOAT       NOT NULL,
    status      VARCHAR(50) NOT NULL DEFAULT 'confirmed',
    PRIMARY KEY (id),
    INDEX idx_reservations_guest_id (guest_id),
    INDEX idx_reservations_room_id (room_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- payments_service: pagos
-- ============================================================
CREATE TABLE IF NOT EXISTS payments (
    id             INT          NOT NULL AUTO_INCREMENT,
    reservation_id INT          NOT NULL,
    amount         FLOAT        NOT NULL,
    currency       VARCHAR(10)  NOT NULL DEFAULT 'USD',
    status         VARCHAR(50)  NOT NULL DEFAULT 'pending',
    transaction_id VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_payments_transaction_id (transaction_id),
    INDEX idx_payments_reservation_id (reservation_id),
    INDEX idx_payments_transaction_id (transaction_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- availability_service: control de disponibilidad (anti-doble reserva)
-- ============================================================
CREATE TABLE IF NOT EXISTS availability_records (
    id        INT  NOT NULL AUTO_INCREMENT,
    room_id   INT  NOT NULL,
    check_in  DATE NOT NULL,
    check_out DATE NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_availability_room_id (room_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- billing_service: facturas
-- ============================================================
CREATE TABLE IF NOT EXISTS invoices (
    id             INT          NOT NULL AUTO_INCREMENT,
    reservation_id INT          NOT NULL,
    amount         FLOAT        NOT NULL,
    status         VARCHAR(50)  NOT NULL DEFAULT 'generated',
    created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_invoices_reservation_id (reservation_id),
    INDEX idx_invoices_reservation_id (reservation_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Datos iniciales de ejemplo (opcional)
-- ============================================================

-- Habitaciones de ejemplo
INSERT IGNORE INTO rooms (number, type, price_per_night) VALUES
    ('101', 'simple',   80.00),
    ('102', 'simple',   80.00),
    ('201', 'doble',   120.00),
    ('202', 'doble',   120.00),
    ('301', 'suite',   250.00),
    ('302', 'suite',   250.00);
