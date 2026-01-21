-- This model calculates the daily movement and Moving Average

WITH raw_data AS (
    SELECT * FROM `wallstreet-data-ops.wallstreet_warehouse.raw_stock_prices`
)

SELECT
    Date,
    Symbol,
    Close,
    -- Calculate daily return percentage
    (Close - Open) / Open * 100 AS daily_return_pct,
    -- Calculate 7-day Moving Average (Windows Function)
    AVG(Close) OVER (
        PARTITION BY Symbol
        ORDER BY Date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS ma_7_day
FROM raw_data