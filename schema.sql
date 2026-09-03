CREATE DATABASE IF NOT EXISTS tomario CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tomario;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hotels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    area VARCHAR(50) NOT NULL,
    address VARCHAR(255),
    description TEXT,
    image_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT NOT NULL,
    room_number VARCHAR(10) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    price_per_night DECIMAL(10,2) NOT NULL,
    capacity INT NOT NULL,
    description TEXT,
    image_url VARCHAR(255),
    FOREIGN KEY (hotel_id) REFERENCES hotels(id),
    UNIQUE KEY uq_hotel_room_number (hotel_id, room_number)
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

INSERT INTO hotels (name, area, address, description) VALUES
('Tomario Hotel 東京', '東京', '東京都千代田区丸の内1-1-1', '都心の主要駅から徒歩圏内、ビジネスにも観光にも便利なホテルです。'),
('Tomario Hotel 京都', '京都', '京都府京都市東山区清水1-1-1', '古都の風情を感じられる、落ち着いた雰囲気のホテルです。'),
('Tomario Hotel 大阪', '大阪', '大阪府大阪市中央区難波1-1-1', '繁華街に近く、食とショッピングを楽しむのに最適なホテルです。');

INSERT INTO rooms (hotel_id, room_number, room_type, price_per_night, capacity, description) VALUES
(1, '101', 'シングル', 8000, 1, '落ち着いた雰囲気のシングルルームです。'),
(1, '102', 'シングル', 8000, 1, '落ち着いた雰囲気のシングルルームです。'),
(1, '201', 'ダブル', 12000, 2, 'ゆったりとしたダブルルームです。'),
(2, '101', 'シングル', 7500, 1, '和の趣を感じるシングルルームです。'),
(2, '202', 'ダブル', 13000, 2, '庭園を望むダブルルームです。'),
(3, '101', 'シングル', 7000, 1, 'アクセス抜群のシングルルームです。'),
(3, '301', 'スイート', 22000, 3, '豪華なスイートルームです。特別なひとときをお過ごしください。');
