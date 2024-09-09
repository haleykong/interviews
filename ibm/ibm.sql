-- IBM 2023-2024 Backend Developer Assessment
-- Question 2)

SELECT MAXIMUM_HACKOS, COUNT(*) AS NUMBER_OF_HACKERS
FROM(
    SELECT MONTHS * HACKOS AS TOTAL_HACKOS, MONTHS, HACKOS
    FROM HACKER
) AS subquery
JOIN (
    SELECT MAX(MONTHS * HACKOS) AS MAXIMUM_HACKOS
    FROM HACKER
) AS max_query
ON subquery.TOTAL_HACKOS = max_query.MAXIMUM_HACKOS
GROUP BY MAXIMUM_HACKOS

-- 1. Subquery to calculate the total_hackos 
-- 2. Subquery to calculae the maximum_hackos
-- 3. Join the subqueries on the total_hackos and maximum_hackos
-- 4. Count the number of entries that match the maximum_hackos


-- Create sample table and insert sample data
CREATE TABLE "HACKER" (
    "ID" INT,
    "NAME" VARCHAR(100),
    "MONTHS" INT,
    "HACKOS" INT
);

INSERT INTO sample_table ("ID", "NAME", "MONTHS", "HACKOS") VALUES
(1, "A", 1, 2),
(2, "B", 3, 4),
(3, "C", 5, 6),
(4, "D", 7, 8);