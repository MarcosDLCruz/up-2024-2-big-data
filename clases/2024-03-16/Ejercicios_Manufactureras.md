1. Display the most expensive products of each brand and their average.

My strategy was to:

- Use a JOIN to combine the manufacturers and articles tables on the matching id and manufacturer_id fields.
- Select the title from the manufacturers table. 
- Use aggregate functions MAX() and AVG() to get the highest and average prices from the articles table.
- Group the results by title to ensure the aggregation applies to each manufacturer.

- SELECT m.title, MAX(a.price), AVG(a.price)
FROM manufacturers AS m
JOIN articles AS a ON m.id = a.manufacturer_id
group by m.title

2. How many products exist in each category

My strategy was to:

- Use LEFT JOIN to combine the categories table with the articles_categories junction table, and then with the articles table.
- Select the title from the categories table, renaming it as category_title.
- Use the COUNT() function to count the number of articles for each category.
- Group the results by category_title to ensure the count applies to each category.

SELECT c.title AS category_title, COUNT(a.id) AS product_count
FROM categories c
LEFT JOIN articles_categories ac ON c.id = ac.category_id
LEFT JOIN articles a ON ac.article_id = a.id
GROUP BY c.title

3. IDEM brand.

My strategy was to:

- Use LEFT JOIN to combine the manufacturers table with the articles table on the manufacturer_id.
- Select the title from the manufacturers table, renaming it as manufacturer_title.
- Use the COUNT() function to count the number of articles associated with each manufacturer.
- Group the results by manufacturer_title to ensure the count applies to each manufacturer.

SELECT m.title AS manufacturer_title, COUNT(a.id) AS product_count
FROM manufacturers m
LEFT JOIN articles a ON m.id = a.manufacturer_id
GROUP BY m.title

4. The 5 most relevant products of each brand.

My strategy was to:

- Use a subquery to rank articles for each manufacturer by their relevance using ROW_NUMBER() with PARTITION BY manufacturer_id ORDER BY relevance DESC.
- Filter the subquery to select only the top 5 articles per manufacturer by checking row_num <= 5.
- Use the filtered results to select articles from the main articles table, ensuring we only get the top 5 relevant articles per manufacturer.
- Join the manufacturers table with the articles table on manufacturer_id.
- Select the title from both manufacturers and articles tables, along with the article's relevance, to display the desired information.

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