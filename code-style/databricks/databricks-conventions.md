# Databricks & Spark Conventions

Standards for Databricks notebooks, PySpark pipelines, Unity Catalog naming, DLT expectations, and SQL warehouses. Designed for consistency across data engineering projects.

---

## 1. Notebook vs Script Conventions

### When to Use Notebooks

- **Exploration and prototyping** — quick data profiling, ad-hoc analysis
- **DLT pipelines** — Delta Live Tables expects notebook-based definitions
- **Dashboards and visualizations** — interactive output cells
- **Collaborative debugging** — sharing results with stakeholders

### When to Use Scripts (.py files)

- **Production ETL** — scheduled jobs, CI/CD-deployed pipelines
- **Shared libraries** — reusable functions, utility modules
- **Unit-testable code** — anything that needs `pytest` coverage
- **Complex transformations** — logic that benefits from IDE tooling and version control diffs

### Notebook Naming Convention

```
{layer}_{entity}_{action}.py
```

| Component | Description | Examples |
|---|---|---|
| `layer` | Medallion layer | `bronze`, `silver`, `gold` |
| `entity` | Data source or domain entity | `oura`, `garmin`, `hr_survey` |
| `action` | What the notebook does | `ingest`, `clean`, `aggregate`, `export` |

**Examples:**

```
bronze_oura_ingest.py
silver_oura_clean.py
gold_health_aggregate.py
bronze_hr_survey_ingest.py
```

### Notebook Structure Rules

- **Max 20 cells per notebook** — split into multiple notebooks if larger
- **First cell: documentation** — always start with a markdown cell containing:
  - Notebook purpose (one sentence)
  - Input tables
  - Output tables
  - Owner/maintainer
- **Last cell: validation** — assert expected row counts or schema checks
- **No hardcoded credentials** — use Databricks secrets or environment variables

```python
# Example documentation cell (markdown)
"""
## bronze_oura_ingest

**Purpose:** Ingest raw Oura API data into bronze layer.
**Input:** Oura REST API (via secrets/oura-api-token)
**Output:** dev.health.bronze_oura_sleep, dev.health.bronze_oura_activity
**Owner:** data-engineering
"""
```

---

## 2. Unity Catalog Naming

### Three-Level Namespace

```
catalog.schema.table
```

All objects use **lowercase snake_case**.

### Catalog: Environment-Based

| Catalog | Purpose |
|---|---|
| `dev` | Development and experimentation |
| `stg` | Staging / pre-production validation |
| `prd` | Production — source of truth |

### Schema: Domain-Based

| Schema | Purpose | Examples |
|---|---|---|
| `health` | Health and fitness data | Oura, Garmin, Apple Health |
| `finance` | Financial data | Bank transactions, budgets |
| `hr` | HR and people data | Surveys, employee metrics |
| `meta` | Pipeline metadata | Audit logs, run history |
| `sandbox` | Temporary exploration | Ad-hoc analysis (dev only) |

### Table Naming

```
{layer}_{source}_{entity}
```

| Component | Description | Examples |
|---|---|---|
| `layer` | Medallion layer | `bronze`, `silver`, `gold` |
| `source` | Origin system | `oura`, `garmin`, `bank` |
| `entity` | Business entity | `sleep`, `activity`, `transaction` |

**Examples:**

```sql
-- Bronze: raw data
dev.health.bronze_oura_sleep
prd.health.bronze_garmin_activity

-- Silver: cleaned data
prd.health.silver_oura_sleep
prd.finance.silver_bank_transaction

-- Gold: aggregated / business-ready
prd.health.gold_daily_health_score
prd.hr.gold_monthly_engagement
```

### Views: `vw_` Prefix (Gold Layer)

Gold-layer views that expose business metrics use the `vw_` prefix:

```sql
prd.health.vw_weekly_sleep_summary
prd.finance.vw_monthly_spending
prd.hr.vw_team_engagement_trend
```

### Volumes and External Locations

```
-- Volume naming
catalog.schema.vol_{purpose}
dev.health.vol_raw_files
prd.meta.vol_export

-- External location naming
ext_{provider}_{purpose}
ext_azure_landing
ext_s3_archive
```

---

## 3. Medallion Layer Rules

### Bronze (Raw Ingestion)

| Rule | Detail |
|---|---|
| **Append-only** | Never update or delete rows in bronze |
| **Source schema preserved** | Keep the original column names and types |
| **Metadata columns required** | `_ingested_at` (timestamp), `_source_file` (if file-based) |
| **Format** | Delta tables (always) |
| **Partitioning** | By `_ingested_at` date for large tables |
| **No transformations** | Raw data exactly as received from source |

```python
from pyspark.sql import functions as F

df_raw = (
    spark.read.json("/mnt/landing/oura/sleep/")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.input_file_name())
)

df_raw.write.mode("append").saveAsTable("dev.health.bronze_oura_sleep")
```

### Silver (Cleaned & Conformed)

| Rule | Detail |
|---|---|
| **Cleaned** | Nulls handled, invalid records filtered or flagged |
| **Typed** | All columns cast to correct types (no string-only tables) |
| **Deduplicated** | Remove exact duplicates, handle late-arriving data |
| **Business keys** | Add surrogate keys or derive natural keys |
| **SCD Type 1 default** | Overwrite with latest value unless history is required |
| **Naming** | Rename source columns to snake_case business terms |

```python
from pyspark.sql import functions as F

df_silver = (
    spark.read.table("dev.health.bronze_oura_sleep")
    .dropDuplicates(["sleep_date", "user_id"])
    .withColumn("sleep_date", F.to_date("sleep_date"))
    .withColumn("total_sleep_hours", F.col("total_sleep_seconds") / 3600)
    .withColumn("_cleaned_at", F.current_timestamp())
    .select(
        "user_id",
        "sleep_date",
        "total_sleep_hours",
        "deep_sleep_seconds",
        "rem_sleep_seconds",
        "sleep_score",
        "_cleaned_at",
    )
)

df_silver.write.mode("overwrite").saveAsTable("dev.health.silver_oura_sleep")
```

### Gold (Business-Ready)

| Rule | Detail |
|---|---|
| **Aggregated** | Pre-computed metrics, summary tables, dimension tables |
| **Business metrics** | Named in business terms, not technical terms |
| **No PII** | No personally identifiable information unless explicitly tagged and access-controlled |
| **Optimized for consumption** | Indexed, partitioned, and Z-ordered for query performance |
| **Documented** | Every gold table has a description in Unity Catalog |

```python
from pyspark.sql import functions as F

df_gold = (
    spark.read.table("prd.health.silver_oura_sleep")
    .groupBy("user_id", F.date_trunc("week", "sleep_date").alias("week_start"))
    .agg(
        F.avg("total_sleep_hours").alias("avg_sleep_hours"),
        F.avg("sleep_score").alias("avg_sleep_score"),
        F.count("sleep_date").alias("nights_tracked"),
    )
)

df_gold.write.mode("overwrite").saveAsTable("prd.health.gold_weekly_sleep_summary")
```

---

## 4. DLT Patterns (Delta Live Tables)

### Table and View Decorators

Use `@dlt.table` for materialized tables and `@dlt.view` for virtual views:

```python
import dlt
from pyspark.sql import functions as F

@dlt.table(
    name="bronze_oura_sleep",
    comment="Raw Oura sleep data ingested from API",
)
def bronze_oura_sleep():
    return (
        spark.read.json("/mnt/landing/oura/sleep/")
        .withColumn("_ingested_at", F.current_timestamp())
    )

@dlt.view(
    name="vw_sleep_quality",
    comment="Sleep quality view for dashboards",
)
def vw_sleep_quality():
    return dlt.read("silver_oura_sleep").filter(F.col("sleep_score").isNotNull())
```

### Expectations (Data Quality Gates)

Use expectations as **guard rails** that enforce data quality, not just monitors:

```python
@dlt.table(name="silver_oura_sleep")
@dlt.expect_or_drop("valid_date", "sleep_date IS NOT NULL")
@dlt.expect_or_drop("valid_score", "sleep_score BETWEEN 0 AND 100")
@dlt.expect_or_fail("has_user_id", "user_id IS NOT NULL")
@dlt.expect("positive_sleep", "total_sleep_seconds > 0")
def silver_oura_sleep():
    return (
        dlt.read("bronze_oura_sleep")
        .withColumn("sleep_date", F.to_date("sleep_date"))
        .withColumn("total_sleep_hours", F.col("total_sleep_seconds") / 3600)
    )
```

| Expectation Type | Behavior | Use When |
|---|---|---|
| `@dlt.expect` | Log warning, keep row | Non-critical quality check |
| `@dlt.expect_or_drop` | Drop failing rows | Bad data should be excluded |
| `@dlt.expect_or_fail` | Fail the pipeline | Critical data integrity violation |

### Pipeline Naming Conventions

```
{environment}_{domain}_{purpose}_pipeline
```

**Examples:**

```
dev_health_ingestion_pipeline
prd_health_transformation_pipeline
prd_finance_reporting_pipeline
```

### DLT Best Practices

- **One pipeline per domain** — do not mix `health` and `finance` in the same pipeline
- **Separate ingestion from transformation** — bronze in one pipeline, silver+gold in another
- **Use `dlt.read()` for inter-table dependencies** — not `spark.read.table()`
- **Set `pipelines.maxFlowRetryAttempts`** for transient failure handling
- **Tag pipelines** with `owner`, `domain`, and `cost_center` for attribution

---

## 5. SQL Warehouse Best Practices

### Warehouse Type Selection

| Type | Use Case | Cost |
|---|---|---|
| **Serverless** | Ad-hoc queries, BI dashboards, low-latency interactive workloads | Per-query (highest per-unit, lowest idle cost) |
| **Pro** | Scheduled reports, moderate concurrency, advanced SQL features | Per-DBU (balanced) |
| **Classic** | Legacy workloads, maximum control over configuration | Per-DBU (lowest per-unit) |

**Default recommendation:** Serverless for dashboards and interactive use, Pro for scheduled ETL queries.

### Query Tagging for Cost Attribution

Always tag queries with cost attribution metadata:

```sql
-- Set query tag before running workload
SET spark.databricks.queryTag = 'team=data-eng,project=health,env=prd';

SELECT
    user_id,
    avg_sleep_score
FROM prd.health.gold_weekly_sleep_summary
WHERE week_start >= '2026-01-01'
```

In Python:

```python
spark.conf.set("spark.databricks.queryTag", "team=data-eng,project=health,env=prd")
```

### Warehouse Sizing Recommendations

| Workload | Size | Auto-Scale | Notes |
|---|---|---|---|
| Dashboard (< 5 users) | Small | 1-2 clusters | Low cost, sufficient for small teams |
| Dashboard (5-20 users) | Medium | 1-4 clusters | Scale based on concurrency |
| Scheduled reports | Small | 1-1 clusters | No scaling needed for batch |
| Ad-hoc exploration | Medium | 1-3 clusters | Allow burst for complex queries |
| Large ETL queries | Large | 1-2 clusters | Size up, do not scale out |

### Idle Timeout Settings

| Environment | Auto-Stop After | Rationale |
|---|---|---|
| `dev` | 10 minutes | Save costs during development |
| `stg` | 15 minutes | Moderate tolerance for testing |
| `prd` | 30 minutes | Avoid restart latency for dashboards |

### Additional Recommendations

- **Enable query result caching** for dashboards with repeated queries
- **Use `LIMIT` during development** — never run unbounded queries on large tables in dev
- **Monitor per-warehouse costs** weekly via system tables (`system.billing.usage`)
- **Separate warehouses by workload type** — do not mix BI queries and ETL on the same warehouse

---

## 6. Spark DataFrame Style Guide

### Chain Transformations with `.transform()`

Use `.transform()` for readable, composable pipelines:

```python
from pyspark.sql import DataFrame, functions as F


def add_ingestion_timestamp(df: DataFrame) -> DataFrame:
    """Add _ingested_at timestamp column."""
    return df.withColumn("_ingested_at", F.current_timestamp())


def filter_valid_records(df: DataFrame) -> DataFrame:
    """Remove records with null primary keys."""
    return df.filter(F.col("user_id").isNotNull())


def cast_date_columns(df: DataFrame) -> DataFrame:
    """Cast string dates to proper date type."""
    return df.withColumn("event_date", F.to_date("event_date"))


# Readable pipeline
df_result = (
    spark.read.table("dev.health.bronze_oura_sleep")
    .transform(filter_valid_records)
    .transform(cast_date_columns)
    .transform(add_ingestion_timestamp)
)
```

### Column Reference Style

**Prefer `F.col("name")` over `df["name"]` or `df.name`:**

```python
from pyspark.sql import functions as F

# CORRECT — explicit, works in all contexts
df.select(F.col("user_id"), F.col("sleep_score"))
df.filter(F.col("sleep_score") > 80)
df.withColumn("score_pct", F.col("sleep_score") / 100)

# WRONG — ambiguous in joins, breaks with special characters
df.select(df["user_id"], df["sleep_score"])
df.filter(df.sleep_score > 80)
```

**Why `F.col()`?**
- Works inside `.transform()` functions that receive generic `DataFrame`
- Unambiguous in joins between tables with overlapping column names
- Consistent style across the entire codebase

### Always Alias Complex Expressions

```python
from pyspark.sql import functions as F

# CORRECT — every derived column has a clear alias
df.select(
    F.col("user_id"),
    (F.col("total_sleep_seconds") / 3600).alias("total_sleep_hours"),
    F.avg("sleep_score").alias("avg_sleep_score"),
    F.when(F.col("sleep_score") >= 85, "good")
     .when(F.col("sleep_score") >= 70, "fair")
     .otherwise("poor")
     .alias("sleep_quality_tier"),
)

# WRONG — unnamed expressions create confusing auto-generated column names
df.select(
    F.col("user_id"),
    F.col("total_sleep_seconds") / 3600,
    F.avg("sleep_score"),
)
```

### Avoid `collect()` in Production Code

`collect()` pulls all data to the driver node and can cause out-of-memory errors:

```python
# WRONG — dangerous in production
all_rows = df.collect()
for row in all_rows:
    process(row)

# CORRECT — use DataFrame operations
df_processed = df.withColumn("result", F.upper(F.col("name")))

# ACCEPTABLE — small lookups only (< 1000 rows, verified)
config_rows = df_config.filter(F.col("is_active")).collect()
```

**Exceptions:**
- Collecting configuration/lookup tables with verified small row counts
- Collecting scalar aggregation results (e.g., `df.count()`)
- Never use `collect()` inside a loop or UDF

### Use `spark.sql()` for Complex Joins, DataFrame API for Simple Transforms

```python
# Simple transform — use DataFrame API
df_clean = (
    df_raw
    .filter(F.col("status") == "active")
    .withColumn("full_name", F.concat_ws(" ", "first_name", "last_name"))
    .select("user_id", "full_name", "email")
)

# Complex multi-table join — use spark.sql() for readability
df_report = spark.sql("""
    SELECT
        s.user_id,
        s.sleep_date,
        s.sleep_score,
        a.total_steps,
        a.active_calories,
        h.resting_heart_rate
    FROM prd.health.silver_oura_sleep AS s
    INNER JOIN prd.health.silver_garmin_activity AS a
        ON s.user_id = a.user_id
        AND s.sleep_date = a.activity_date
    LEFT JOIN prd.health.silver_garmin_heart_rate AS h
        ON s.user_id = h.user_id
        AND s.sleep_date = h.measurement_date
    WHERE s.sleep_date >= '2026-01-01'
    ORDER BY s.sleep_date DESC
""")
```

### Additional DataFrame Rules

- **Import convention:** `from pyspark.sql import functions as F` and `from pyspark.sql import types as T`
- **One transformation per line** when chaining — use parentheses for multi-line expressions
- **Avoid `withColumnRenamed` chains** — use a single `.select()` with aliases instead
- **Prefer `F.lit()` for constants** — not Python literals in column expressions
- **Cache strategically** — only cache DataFrames reused more than twice in the same job

```python
# CORRECT — single select with aliases
df_renamed = df.select(
    F.col("usr_id").alias("user_id"),
    F.col("slp_score").alias("sleep_score"),
    F.col("dt").alias("sleep_date"),
)

# WRONG — chain of renames
df_renamed = (
    df
    .withColumnRenamed("usr_id", "user_id")
    .withColumnRenamed("slp_score", "sleep_score")
    .withColumnRenamed("dt", "sleep_date")
)
```

---

## Cross-References

- **Python linting:** [`../python/ruff.toml`](../python/ruff.toml) — Ruff linter configuration for all Python code including PySpark
- **SQL conventions:** [`../sql/sql-conventions.md`](../sql/sql-conventions.md) — SQL formatting rules for warehouse queries and `spark.sql()` blocks
- **Pre-commit hooks:** [`../python/.pre-commit-config.yaml`](../python/.pre-commit-config.yaml) — Automated quality checks for Python files
- **Secret scanning:** [`../../security/security-standards.md`](../../security/security-standards.md) — Credential handling and secret management

---

## Summary Checklist

| Area | Standard |
|---|---|
| Notebook naming | `{layer}_{entity}_{action}.py` |
| Max cells per notebook | 20 |
| Unity Catalog namespace | `catalog.schema.table` |
| Catalog naming | Environment-based (`dev`, `stg`, `prd`) |
| Schema naming | Domain-based (`health`, `finance`, `hr`) |
| Table naming | `{layer}_{source}_{entity}` |
| Gold views | `vw_` prefix |
| Bronze layer | Append-only, source schema preserved, `_ingested_at` |
| Silver layer | Cleaned, typed, deduplicated, SCD Type 1 |
| Gold layer | Aggregated, no PII, business metrics |
| DLT expectations | `@dlt.expect_or_drop` for guard rails |
| DLT pipeline naming | `{env}_{domain}_{purpose}_pipeline` |
| SQL warehouse default | Serverless for dashboards, Pro for ETL |
| Warehouse idle timeout | dev: 10m, stg: 15m, prd: 30m |
| Column references | `F.col("name")` not `df["name"]` |
| Complex expressions | Always `.alias()` |
| `collect()` | Avoid in production |
| Complex joins | `spark.sql()` |
| Simple transforms | DataFrame API |
