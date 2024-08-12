WITH city_customer_counts AS (
    SELECT city_id, COUNT(*) AS customer_count
    FROM customer
    GROUP BY city_id
),
average_customers_overall AS (
    SELECT AVG(customer_count) as average_customers
    FROM city_customer_counts
)
SELECT country.country_name, city.city_name, ccc.customer_count
FROM city
JOIN country ON city.country_id = country.id
JOIN city_customer_counts ccc on city.id = ccc.city_id
JOIN average_customers_overall aco ON ccc.customer_count > aco.average_customers;