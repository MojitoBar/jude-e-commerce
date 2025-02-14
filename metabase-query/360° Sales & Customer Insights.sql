-- 1.2 국가별 매출 비교
SELECT 
    country,
    SUM(total_amount) as total_revenue
FROM sales
GROUP BY country
ORDER BY total_revenue DESC;

-- 1.3 시간대별 주문 패턴
SELECT 
    CASE 
        WHEN EXTRACT(HOUR FROM date) BETWEEN 0 AND 3 THEN '00:00-03:59'
        WHEN EXTRACT(HOUR FROM date) BETWEEN 4 AND 7 THEN '04:00-07:59'
        WHEN EXTRACT(HOUR FROM date) BETWEEN 8 AND 11 THEN '08:00-11:59'
        WHEN EXTRACT(HOUR FROM date) BETWEEN 12 AND 15 THEN '12:00-15:59'
        WHEN EXTRACT(HOUR FROM date) BETWEEN 16 AND 19 THEN '16:00-19:59'
        ELSE '20:00-23:59'
    END as time_range,
    CASE EXTRACT(DOW FROM date)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END as day_of_week,
    COUNT(*) as order_count
FROM sales
GROUP BY 
    CASE 
        WHEN EXTRACT(HOUR FROM date) BETWEEN 0 AND 3 THEN '00:00-03:59'
        WHEN EXTRACT(HOUR FROM date) BETWEEN 4 AND 7 THEN '04:00-07:59'
        WHEN EXTRACT(HOUR FROM date) BETWEEN 8 AND 11 THEN '08:00-11:59'
        WHEN EXTRACT(HOUR FROM date) BETWEEN 12 AND 15 THEN '12:00-15:59'
        WHEN EXTRACT(HOUR FROM date) BETWEEN 16 AND 19 THEN '16:00-19:59'
        ELSE '20:00-23:59'
    END,
    EXTRACT(DOW FROM date)
ORDER BY 
    time_range,
    day_of_week;

-- 2.1 고객 구매액 분포
SELECT 
    CASE 
        WHEN total_purchase_amount >= 1000 THEN 'VIP (1000+)'
        WHEN total_purchase_amount >= 500 THEN 'High (500-999)'
        WHEN total_purchase_amount >= 100 THEN 'Medium (100-499)'
        ELSE 'Low (<100)'
    END as customer_segment,
    COUNT(*) as customer_count
FROM customer_summary
GROUP BY customer_segment;

-- 3.1 상위 판매 제품
SELECT 
    product_name,
    SUM(quantity) as total_quantity,
    SUM(total_amount) as total_revenue
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;

-- 1.1 일별 매출 추이
SELECT 
    date::date as sale_date,
    SUM(total_amount) as daily_revenue
FROM sales
GROUP BY date::date
ORDER BY date::date;

-- 5.1 월별 매출 및 성장률
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', date) as month,
        SUM(total_amount) as revenue
    FROM sales
    GROUP BY DATE_TRUNC('month', date)
)
SELECT 
    month,
    revenue,
    ((revenue - LAG(revenue) OVER (ORDER BY month)) / 
     LAG(revenue) OVER (ORDER BY month) * 100) as growth_rate
FROM monthly_sales
ORDER BY month;