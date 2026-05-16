import duckdb

con = duckdb.connect("supply_chain.duckdb")

con.execute("""
CREATE OR REPLACE TABLE clean_supply_chain AS
SELECT
    Type,
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Benefit per order",
    "Sales per customer",
    "Delivery Status",
    Late_delivery_risk,
    "Category Name",
    "Customer City",
    "Customer Country",
    "Customer Segment",
    "Customer State",
    "Department Name",
    Market,
    "Order City",
    "Order Country",
    "order date (DateOrders)",
    "Order Id",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Product Price",
    "Order Item Profit Ratio",
    "Order Item Quantity",
    Sales,
    "Order Item Total",
    "Order Profit Per Order",
    "Order Region",
    "Order State",
    "Order Status",
    "shipping date (DateOrders)",
    "Shipping Mode",
    "Product Name",
    "Product Price"
FROM supply_chain
""")

print("Clean table created successfully!")

print(con.execute("""
SELECT COUNT(*) 
FROM clean_supply_chain
""").fetchall())
print(con.execute("""
DESCRIBE clean_supply_chain
""").fetchdf())

print(con.execute("""
SELECT *
FROM clean_supply_chain
LIMIT 5
""").fetchdf())

