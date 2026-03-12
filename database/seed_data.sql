-- Seed users (password for all is 'password123')
INSERT INTO users (id, email, password_hash, role, full_name) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'admin@upf.edu.my', '$2b$12$CDt6/cfN1/Z1irko9FZ8Vemnyk0c/dyJz0LAuqgvHSlbdXsVNw656', 'UPF Admin', 'UPF Administrator'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'staff@upf.edu.my', '$2b$12$CDt6/cfN1/Z1irko9FZ8Vemnyk0c/dyJz0LAuqgvHSlbdXsVNw656', 'UPF Staff', 'Ahmad Staff'),
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'driver1@upf.edu.my', '$2b$12$CDt6/cfN1/Z1irko9FZ8Vemnyk0c/dyJz0LAuqgvHSlbdXsVNw656', 'Driver', 'Babu Driver'),
('d0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'tech1@upf.edu.my', '$2b$12$CDt6/cfN1/Z1irko9FZ8Vemnyk0c/dyJz0LAuqgvHSlbdXsVNw656', 'Technician', 'Chandra Tech'),
('e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'security@upf.edu.my', '$2b$12$CDt6/cfN1/Z1irko9FZ8Vemnyk0c/dyJz0LAuqgvHSlbdXsVNw656', 'Security Officer', 'David Security');

-- Seed rooms
INSERT INTO rooms (id, name, capacity, location, resources) VALUES
('f0eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', 'Bilik Mesyuarat Utama', 20, 'Level 1, Block A', ARRAY['TV', 'Projector', 'Video Conference']),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'Bilik Perbincangan 1', 6, 'Level 2, Block B', ARRAY['Whiteboard']),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', 'Dewan Seminar', 100, 'Level 1, Block C', ARRAY['Projector', 'PA System']);

-- Seed vehicles
INSERT INTO vehicles (id, plate_number, model, type, capacity, status) VALUES
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'WAA 1234', 'Proton X70', 'SUV', 5, 'Available'),
('d0eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', 'WBB 5678', 'Toyota Hiace', 'Van', 12, 'Available'),
('e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a21', 'WCC 9012', 'Honda Accord', 'Sedan', 5, 'Available');

-- Seed logistic items
INSERT INTO logistic_items (id, name, category, quantity) VALUES
('f0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Plastic Chairs', 'Furniture', 200),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a23', 'Folding Tables', 'Furniture', 50),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a24', 'Microphone', 'ICT', 10),
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a25', 'Projector Screen', 'ICT', 5);

-- Seed stationery items
INSERT INTO stationery_items (id, item_name, category, unit, stock_quantity, minimum_stock_level, storage_location) VALUES
('d0eebc99-9c0b-4ef8-bb6d-6bb9bd380a26', 'A4 Paper', 'Paper', 'Ream', 100, 20, 'Store Room A'),
('e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a27', 'Black Pen', 'Writing', 'Box', 50, 10, 'Store Room A'),
('f0eebc99-9c0b-4ef8-bb6d-6bb9bd380a28', 'Notebook', 'Writing', 'Unit', 30, 5, 'Store Room B');

-- Seed equipment
INSERT INTO equipment (id, name, category, serial_number, status, condition) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a29', 'Laptop Dell Latitude', 'IT', 'SN123456', 'Available', 'New'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a30', 'Portable Projector', 'IT', 'SN789012', 'Available', 'Good'),
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a31', 'Public Address System', 'Event & Logistic', 'SN345678', 'Available', 'Good');
