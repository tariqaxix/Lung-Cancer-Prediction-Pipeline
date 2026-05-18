# Pipeline Examples

---

## 1. Data Lineage — Full Pipeline Flow

![Data Lineage](data_lineage.jpg)

---

## 2. Bronze - Raw Files Uploaded to Databricks Volume

`/Volumes/workspace/bronze/raw_files/` — WHO_pollution.csv (2.15 MB), abstract-lungcancer.txt (25.25 MB), lung_cancer_dataset.csv (22.40 MB)

![Raw Files in Catalog](Raw%20files%20inside%20catalog.png)

---


## 3. Bronze - Structured & Unstructured Ingestion Row Counts

`bronze.raw_lung_cancer`: 220,632 rows | `bronze.raw_who_pollution`: 13,176 rows | `bronze.raw_pubmed`: 487,202 rows

![Bronze Row Counts](LungsData%2C%20WHO%2C%20PubMed%20Data.png)

---

## 4. Bronze - Real-Time Air Quality Ingestion (14 Countries × 120 Records)

Total: 1,680 records fetched → saved to `bronze.raw_air_quality`

![Air Quality Ingestion](API%20Air%20quality%20Ingestion.png)

---

## 5. Bronze - Scheduled Databricks Job for Air Quality

![Databricks Job Schedule](Job%20Schedule%20Air%20Quality.png)

---

## 6. Silver - Lung Cancer Data Cleaned

`silver.lung_cancer`: 220,632 → 220,632 rows (0 dropped)

![Silver Lung Cancer](Silver%20Lung%20cancer%20data%20clean.png)

---


## 7. Silver - WHO Pollution Data Cleaned

`silver.who_pollution`: 13,176 records

![Silver WHO](WHO%20silver%20clean%20data.png)

---


## 8. Silver - Air Quality Aggregated

`silver.air_quality`: 14 records (one per country)

![Silver Air Quality](Air%20Quality%20Silver%20Clean.png)

---

## 9. Silver - PubMed Abstracts Structured

`silver.abstracts`: 10,000 records

![Silver PubMed](PubMed%20Clean%20Silver.png)

---

## 10. Gold - Risk by Country Aggregated

`gold.risk_by_country`: 25 rows (one per country)

![Gold Risk by Country](gold_risk_by_country_aggregated.jpg)

---

## 11. Gold - Optimization (ZORDER + VACUUM)

All Gold tables are optimized with `OPTIMIZE ... ZORDER BY (...)`, `VACUUM RETAIN 168 HOURS`, and `DESCRIBE HISTORY` to improve query performance and manage storage.

![Gold Optimization](gold%20optimization.jpg)

---

## 12. ML - Train/Test Split

Train: 176,505 | Test: 44,127 | Cancer rate: 4.1%

![Train Test Split](Train%20Test%20Split%20for%20ML%20model.png)

---

## 13. ML - XGBoost Performance (MLflow Run)

AUC: 0.6528 | Accuracy: 0.6199 | F1: 0.1270

![XGBoost Performance](Performance%20of%20XGBoost%20model.png)

---

## 14. Dashboard - Cancer Rate by Country

![Cancer Rate Graph](Cancer%20Rate%20percentage%20Graph.png)

---

## 15. Dashboard - Cancer Rate vs. Air Quality (AQI)

![AQI vs Cancer Rate](Air%20Quality%20and%20Cancer%20rate%20percentage%20graph.png)

---

## 16. Dashboard - Risk Keywords from PubMed Abstracts (Word Cloud)

![Keyword Word Cloud](Wordcloud%20for%20keywords%20used%20in%20abstracts%20graph.png)

---

## 17. Dashboard - Smoker Rate by Country (World Map)

![Smoker Rate Map](Country%20and%20smoker%20percentage%20graph.png)

---

## 18. API - Swagger UI

![Swagger UI](Lung%20Cancer%20Risk%20prediction%20API.png)

---

## 19. External Visualization - Google Looker Studio

![Looker Studio](external_visualization_google_looker_studio.jpg)

---

## 20. Tests - Local pytest Run (14 tests)

![Test Results](test_results.jpg)

---

## 21. CI - GitHub Actions (Runs on Every Push)

![GitHub Actions](automated_testing_github_actions.jpg)


