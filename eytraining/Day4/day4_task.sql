CREATE TABLE shopey.customers(
    customer_id SERIAL PRIMARY KEY,
    f_name VARCHAR(50),
    l_name VARCHAR(50),
    email VARCHAR(100)
);

-- Orders
CREATE TABLE shopey.orders (
    order_id    SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES shopey.customers(customer_id),
    order_date  TIMESTAMP DEFAULT NOW(),
    status      VARCHAR(20) CHECK (status IN ('Pending','Confirmed','Shipped','Delivered','Cancelled')) DEFAULT 'Pending'
);

-- Order Lines
CREATE TABLE shopey.order_lines (
    line_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES shopey.orders(order_id),
    product_id INT NOT NULL REFERENCES shopey.products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL
);

-- Payments
CREATE TABLE shopey.payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INT UNIQUE NOT NULL REFERENCES shopey.orders(order_id),
    payment_date TIMESTAMP,
    method VARCHAR(50) CHECK (method IN ('Card','PayPal','Bank Transfer','Wallet')),
    amount NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Pending','Paid','Failed','Refunded')) DEFAULT 'Pending'
);

INSERT INTO shopey.customers (f_name, l_name, email)
VALUES
('Alice', 'Smith', 'alice@gmail.com'),
('Bob', 'Johnson', 'bob@gmail.com'),
('Carol', 'White', 'carol@gmail.com');

INSERT INTO shopey.orders (customer_id, status)
VALUES
(1, 'Delivered'),
(1, 'Delivered'),
(2, 'Delivered'),
(2, 'Shipped'),
(3, 'Delivered');

INSERT INTO shopey.order_lines
(order_id, product_id, quantity, unit_price)
VALUES
(1, 1, 2, 100.00),
(1, 2, 1, 50.00),

(2, 1, 3, 200.00),

(3, 2, 1, 300.00),

(4, 3, 2, 150.00),

(5, 1, 1, 500.00);


SELECT
    c.f_name || ' ' || c.l_name AS customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(ol.quantity * ol.unit_price) AS total_spent,
    RANK() OVER (
        ORDER BY SUM(ol.quantity * ol.unit_price) DESC
    ) AS customer_rank
FROM shopey.customers c

INNER JOIN shopey.orders o
    ON c.customer_id = o.customer_id

INNER JOIN shopey.order_lines ol
    ON o.order_id = ol.order_id

GROUP BY
    c.customer_id,
    c.f_name,
    c.l_name

ORDER BY customer_rank ASC;