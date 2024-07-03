CREATE TABLE warehouses(warehouse_id INT NOT NULL AUTO_INCREMENT, name TEXT NOT NULL, latitude DECIMAL NOT NULL, longitude DECIMAL NOT NULL, PRIMARY KEY(warehouse_id));
CREATE TABLE items(item_id INT NOT NULL AUTO_INCREMENT, name TEXT NOT NULL, PRIMARY KEY(item_id));
CREATE TABLE stock(stock_id INT NOT NULL AUTOINCREMENT, warehouse_id INT NOT NULL, item_id INT NOT NULL, quantity INT NOT NULL,
PRIMARY KEY(stock_id), FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id), FOREIGN KEY (item_id) REFERENCES items(item_id));

