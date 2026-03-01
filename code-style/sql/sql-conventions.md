# SQL Conventions

Consistent SQL formatting rules for data pipelines, analytics, and application queries. Designed for readability by both humans and AI agents.

---

## Core Rules

### 1. Keywords: UPPERCASE

All SQL keywords in uppercase. All identifiers (tables, columns, aliases) in lowercase.

```sql
SELECT
    user_id,
    first_name,
    created_at
FROM dim_customer
WHERE is_active = TRUE
ORDER BY created_at DESC
```

### 2. CTEs Over Subqueries

Use Common Table Expressions (CTEs) instead of nested subqueries. CTEs are easier to read, debug, and reuse.

```sql
-- CORRECT: CTEs
WITH active_users AS (
    SELECT
        user_id,
        email,
        created_at
    FROM dim_user
    WHERE is_active = TRUE
),

recent_orders AS (
    SELECT
        user_id,
        order_id,
        order_total,
        ordered_at
    FROM fct_order
    WHERE ordered_at >= CURRENT_DATE - INTERVAL '30 days'
)

SELECT
    au.user_id,
    au.email,
    COUNT(ro.order_id) AS order_count,
    SUM(ro.order_total) AS total_spent
FROM active_users AS au
LEFT JOIN recent_orders AS ro
    ON au.user_id = ro.user_id
GROUP BY
    au.user_id,
    au.email
```

```sql
-- WRONG: Nested subqueries
SELECT
    u.user_id,
    u.email,
    sub.order_count,
    sub.total_spent
FROM (
    SELECT user_id, email FROM dim_user WHERE is_active = TRUE
) u
LEFT JOIN (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(order_total) AS total_spent
    FROM fct_order
    WHERE ordered_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
) sub ON u.user_id = sub.user_id
```

### 3. Explicit Column Lists — No `SELECT *`

Always list columns explicitly. `SELECT *` breaks when schemas change and hides what data you actually need.

```sql
-- CORRECT
SELECT
    user_id,
    email,
    first_name,
    last_name,
    created_at
FROM dim_user

-- WRONG
SELECT * FROM dim_user
```

**Exception:** `SELECT *` is acceptable inside a CTE that immediately feeds into a specific column list, or in exploratory/ad-hoc queries (never in production code).

### 4. Trailing Commas

Place commas at the end of the line (trailing). This makes diffs cleaner when adding or removing columns.

```sql
-- CORRECT: Trailing commas
SELECT
    user_id,
    first_name,
    last_name,
    email,
    created_at
FROM dim_user
```

```sql
-- WRONG: Leading commas
SELECT
    user_id
    , first_name
    , last_name
    , email
    , created_at
FROM dim_user
```

### 5. One Column Per Line for 3+ Columns

If a SELECT, GROUP BY, or ORDER BY has more than 3 columns, put each on its own line.

```sql
-- CORRECT: 4+ columns, one per line
SELECT
    user_id,
    email,
    first_name,
    last_name
FROM dim_user

-- ACCEPTABLE: 3 or fewer columns can stay on one line
SELECT user_id, email, created_at
FROM dim_user
WHERE is_active = TRUE
```

### 6. JOIN Formatting

- Explicit join type (never omit INNER/LEFT/etc.)
- ON clause indented on the next line
- Table aliases: short but meaningful (not single letters unless obvious)

```sql
-- CORRECT
SELECT
    o.order_id,
    o.order_total,
    c.email,
    p.product_name
FROM fct_order AS o
INNER JOIN dim_customer AS c
    ON o.customer_id = c.customer_id
LEFT JOIN dim_product AS p
    ON o.product_id = p.product_id
WHERE o.ordered_at >= '2025-01-01'
```

```sql
-- WRONG
SELECT o.order_id, o.order_total, c.email, p.product_name
FROM fct_order o
JOIN dim_customer c ON o.customer_id = c.customer_id   -- implicit INNER, ON not indented
LEFT JOIN dim_product p ON o.product_id = p.product_id  -- ON not indented
WHERE o.ordered_at >= '2025-01-01'
```

### 7. WHERE Clause Formatting

Each condition on its own line. AND/OR at the start of the line.

```sql
-- CORRECT
WHERE
    o.ordered_at >= '2025-01-01'
    AND o.status = 'completed'
    AND o.order_total > 0
    AND c.is_active = TRUE
```

```sql
-- WRONG
WHERE o.ordered_at >= '2025-01-01' AND o.status = 'completed' AND o.order_total > 0
```

### 8. Indentation

Use 4 spaces. No tabs. Indent consistently within CTEs, subqueries, and CASE statements.

```sql
SELECT
    user_id,
    CASE
        WHEN total_orders >= 100 THEN 'platinum'
        WHEN total_orders >= 50 THEN 'gold'
        WHEN total_orders >= 10 THEN 'silver'
        ELSE 'bronze'
    END AS customer_tier,
    total_orders
FROM int_customer_summary
```

---

## Before/After Example

### Before (bad style)

```sql
select u.*, count(o.id) as cnt, sum(o.total) as rev from users u
left join orders o on u.id=o.user_id where u.active=1
and o.created_at > '2025-01-01' group by u.id having count(o.id) > 5
order by rev desc limit 100
```

### After (following conventions)

```sql
WITH active_users AS (
    SELECT
        user_id,
        email,
        first_name,
        last_name
    FROM dim_user
    WHERE is_active = TRUE
),

user_orders AS (
    SELECT
        user_id,
        COUNT(order_id) AS order_count,
        SUM(order_total) AS total_revenue
    FROM fct_order
    WHERE ordered_at > '2025-01-01'
    GROUP BY user_id
    HAVING COUNT(order_id) > 5
)

SELECT
    au.user_id,
    au.email,
    au.first_name,
    au.last_name,
    uo.order_count,
    uo.total_revenue
FROM active_users AS au
INNER JOIN user_orders AS uo
    ON au.user_id = uo.user_id
ORDER BY uo.total_revenue DESC
LIMIT 100
```

---

## Summary Checklist

| Rule | Standard |
|---|---|
| Keywords | UPPERCASE |
| Identifiers | lowercase snake_case |
| Complex queries | CTEs, not subqueries |
| Column lists | Explicit (no SELECT *) |
| Commas | Trailing |
| Multi-column | One per line (3+) |
| JOINs | Explicit type, ON indented |
| WHERE | One condition per line, AND/OR leading |
| Indentation | 4 spaces |
| Table aliases | Short but meaningful, using AS |
