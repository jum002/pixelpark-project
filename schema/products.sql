CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image_url VARCHAR(200),
    price DECIMAL(10,2) NOT NULL,
    template_url VARCHAR(200),
    x1 INT DEFAULT 0,
    y1 INT DEFAULT 0,
    x2 INT DEFAULT 0,
    y2 INT DEFAULT 0
);