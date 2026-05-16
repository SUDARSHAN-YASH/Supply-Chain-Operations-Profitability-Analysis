import duckdb

con = duckdb.connect("supply_chain.duckdb")

print(con.execute("""
SELECT
    "Delivery Status",
    COUNT(*) AS total_orders
FROM clean_supply_chain
GROUP BY "Delivery Status"
ORDER BY total_orders DESC
""").fetchdf())


print(con.execute("""
SELECT
    "Delivery Status",
    COUNT(*) AS total_orders,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM clean_supply_chain
GROUP BY "Delivery Status"
ORDER BY total_orders DESC
""").fetchdf())


print(con.execute("""
SELECT
    "Shipping Mode",
    "Delivery Status",
    COUNT(*) AS total_orders
FROM clean_supply_chain
GROUP BY
    "Shipping Mode",
    "Delivery Status"
ORDER BY total_orders DESC
""").fetchdf())


print(con.execute("""
SELECT
    ROUND(MIN("Benefit per order"),2) AS min_profit,
    ROUND(MAX("Benefit per order"),2) AS max_profit,
    ROUND(AVG("Benefit per order"),2) AS avg_profit
FROM clean_supply_chain
""").fetchdf())


print(con.execute("""
SELECT
    "Shipping Mode",
    "Delivery Status",
    COUNT(*) AS total_orders,
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER(PARTITION BY "Shipping Mode"),
        2
    ) AS percentage_within_mode
FROM clean_supply_chain
GROUP BY
    "Shipping Mode",
    "Delivery Status"
ORDER BY
    "Shipping Mode",
    percentage_within_mode DESC
""").fetchdf())


print(con.execute("""
SELECT
    "Category Name",
    ROUND(AVG("Benefit per order"),2) AS avg_profit,
    ROUND(MIN("Benefit per order"),2) AS worst_loss,
    COUNT(*) AS total_orders
FROM clean_supply_chain
GROUP BY "Category Name"
ORDER BY avg_profit ASC
""").fetchdf())


print(con.execute("""
SELECT
    "Category Name",
    ROUND(SUM("Benefit per order"),2) AS total_profit,
    ROUND(AVG("Benefit per order"),2) AS avg_profit,
    COUNT(*) AS total_orders
FROM clean_supply_chain
GROUP BY "Category Name"
ORDER BY total_profit ASC
""").fetchdf())


print(con.execute("""
SELECT
    "Order Region",
    COUNT(*) AS total_orders,
    SUM(
        CASE
            WHEN "Delivery Status" = 'Late delivery'
            THEN 1 ELSE 0
        END
    ) AS late_orders,
    ROUND(
        SUM(
            CASE
                WHEN "Delivery Status" = 'Late delivery'
                THEN 1 ELSE 0
            END
        ) * 100.0 / COUNT(*),
    2) AS late_delivery_percentage
FROM clean_supply_chain
GROUP BY "Order Region"
ORDER BY late_delivery_percentage DESC
""").fetchdf())


print(con.execute("""
SELECT
    ROUND("Order Item Discount",2) AS discount_amount,
    ROUND(AVG("Benefit per order"),2) AS avg_profit,
    COUNT(*) AS total_orders
FROM clean_supply_chain
GROUP BY discount_amount
ORDER BY discount_amount DESC
LIMIT 20
""").fetchdf())


print(con.execute("""
SELECT
    "Shipping Mode",
    ROUND(AVG("Benefit per order"),2) AS avg_profit,
    ROUND(SUM("Benefit per order"),2) AS total_profit,
    COUNT(*) AS total_orders
FROM clean_supply_chain
GROUP BY "Shipping Mode"
ORDER BY avg_profit DESC
""").fetchdf())


print(con.execute("""
SELECT
    "Category Name",
    COUNT(*) AS total_orders,
    ROUND(
        AVG(
            CASE
                WHEN "Delivery Status" = 'Late delivery'
                THEN 1 ELSE 0
            END
        ) * 100,
    2) AS late_delivery_percentage
FROM clean_supply_chain
GROUP BY "Category Name"
ORDER BY late_delivery_percentage DESC
""").fetchdf())


print(con.execute("""
SELECT
    "Order Region",
    ROUND(SUM("Benefit per order"),2) AS total_profit,
    ROUND(AVG("Benefit per order"),2) AS avg_profit,
    COUNT(*) AS total_orders
FROM clean_supply_chain
GROUP BY "Order Region"
ORDER BY total_profit DESC
""").fetchdf())


print(con.execute("""
SELECT
    "Delivery Status",
    ROUND(AVG("Benefit per order"),2) AS avg_profit,
    ROUND(SUM("Benefit per order"),2) AS total_profit,
    COUNT(*) AS total_orders
FROM clean_supply_chain
GROUP BY "Delivery Status"
ORDER BY avg_profit ASC
""").fetchdf())


print(con.execute("""
SELECT
    STRFTIME(
        COALESCE(
            TRY_STRPTIME(
                "order date (DateOrders)",
                '%m/%d/%Y %H:%M'
            ),
            TRY_STRPTIME(
                "order date (DateOrders)",
                '%m-%d-%Y %H:%M'
            )
        ),
        '%Y-%m'
    ) AS order_month,

    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN "Delivery Status" = 'Late delivery'
            THEN 1 ELSE 0
        END
    ) AS late_orders,

    ROUND(
        SUM(
            CASE
                WHEN "Delivery Status" = 'Late delivery'
                THEN 1 ELSE 0
            END
        ) * 100.0 / COUNT(*),
    2) AS late_delivery_percentage

FROM clean_supply_chain

GROUP BY order_month

ORDER BY order_month
""").fetchdf())

print(con.execute("""
SELECT
    ROUND(AVG("Days for shipment (scheduled)"),2)
        AS avg_scheduled_days,

    ROUND(AVG("Days for shipping (real)"),2)
        AS avg_actual_days,

    ROUND(
        AVG("Days for shipping (real)")
        -
        AVG("Days for shipment (scheduled)"),
    2) AS avg_delay_gap

FROM clean_supply_chain
""").fetchdf())


print(con.execute("""
SELECT
    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN "Days for shipping (real)"
                 >
                 "Days for shipment (scheduled)"
            THEN 1 ELSE 0
        END
    ) AS delayed_orders,

    ROUND(
        SUM(
            CASE
                WHEN "Days for shipping (real)"
                     >
                     "Days for shipment (scheduled)"
                THEN 1 ELSE 0
            END
        ) * 100.0 / COUNT(*),
    2) AS delayed_order_percentage

FROM clean_supply_chain
""").fetchdf())
