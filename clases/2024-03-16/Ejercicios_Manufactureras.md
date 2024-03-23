1. Mostrar los productos más caros de cada marca y su promedio


SELECT m.title, MAX(a.price), AVG(a.price)
FROM manufacturers AS m
JOIN articles AS a ON m.id = a.manufacturer_id
group by m.title

2. Cuántos productos existen en cada categoría

SELECT c.title AS category_title, COUNT(a.id) AS product_count
FROM categories c
LEFT JOIN articles_categories ac ON c.id = ac.category_id
LEFT JOIN articles a ON ac.article_id = a.id
GROUP BY c.title

3. IDEM marca.

SELECT m.title AS manufacturer_title, COUNT(a.id) AS product_count
FROM manufacturers m
LEFT JOIN articles a ON m.id = a.manufacturer_id
GROUP BY m.title

4. Los 5 productos más relevantes de cada marca.

SELECT m.title AS manufacturer_title, a.title AS product_title, a.relevance
FROM manufacturers m
JOIN articles a ON m.id = a.manufacturer_id
WHERE a.id IN (
    SELECT id
    FROM (
        SELECT id, ROW_NUMBER() OVER (PARTITION BY manufacturer_id ORDER BY relevance DESC) AS row_num
        FROM articles
    ) AS ranked
    WHERE row_num <= 5
)