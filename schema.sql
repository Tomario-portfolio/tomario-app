CREATE DATABASE IF NOT EXISTS tomario CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tomario;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(10) NOT NULL UNIQUE,
    room_type VARCHAR(50) NOT NULL,
    price_per_night DECIMAL(10,2) NOT NULL,
    capacity INT NOT NULL,
    description TEXT,
    image_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    room_id INT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);

INSERT INTO rooms (room_number, room_type, price_per_night, capacity, description) VALUES
('101', 'シングル', 8000, 1, '落ち着いた雰囲気のシングルルームです。'),
('102', 'シングル', 8000, 1, '落ち着いた雰囲気のシングルルームです。'),
('201', 'ダブル', 12000, 2, 'ゆったりとしたダブルルームです。'),
('202', 'ダブル', 12000, 2, 'ゆったりとしたダブルルームです。'),
('301', 'スイート', 25000, 3, '豪華なスイートルームです。特別なひとときをお過ごしください。');
