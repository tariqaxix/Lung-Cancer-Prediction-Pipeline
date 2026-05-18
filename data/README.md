# Data Directory

The raw dataset and files are stored in this folder. The files in these folders can be used to reproduce the results of our project. Our pipeline actually uses the datasets stored in Databricks Volume (/Volumes/workspace/bronze/raw_files/).



#### lung_cancer_dataset.csv - Primary structured dataset
Source: Kaggle - [Lung Cancer Risk & Trends Across 25 Countries](https://www.kaggle.com/datasets/ankushpanday1/lung-cancer-risk-and-trends-across-25-countries)

Size: 220,632 rows × 24 columns

Separator: comma

We are using this as the main dataset for prediction model. The rows in the table represent individuals and the columns show their demographic, lifestyle, and clinical attributes.

| Column | Type | Description | Example Values |
|---|---|---|---|
| ID | integer | Unique patient identifier | 1, 2, 3, ... |
| Country | string | Country of residence | China, Iran, Mexico |
| Population_Size | integer | Country population (in Million) | 1400, 84, 128|
| Age | integer | Patient age in years | 23-85 |
| Gender | string | Patient gender | Male, Female |
| Smoker | string | Current/former smoker | Yes, No |
| Years_of_Smoking | integer | Duration of smoking in years | 0-60 |
| Cigarettes_per_Day | integer | Average cigarettes per day | 0-40 |
| Passive_Smoker | string | Exposed to secondhand smoke | Yes, No |
| Family_History | string | Family history of cancer | Yes, No |
| Lung_Cancer_Diagnosis | string | **Target variable** | Yes, No |
| Cancer_Stage | string | Clinical stage at diagnosis | None, Stage I, Stage II, Stage III |
| Survival_Years | float | Years survived post-diagnosis | 0.0-10.0 |
| Adenocarcinoma_Type | string | Subtype of lung cancer | Yes, No |
| Air_Pollution_Exposure | string | General exposure level | Low, Medium, High |
| Occupational_Exposure | string | Workplace carcinogen exposure | Yes, No |
| Indoor_Pollution | string | Indoor air pollution exposure | Yes, No |
| Healthcare_Access | string | Access to medical care | Good, Poor |
| Early_Detection | string | Detected via screening | Yes, No |
| Treatment_Type | string | Treatment received | None, Surgery, Chemotherapy, Radiotherapy |
| Developed_or_Developing | string | Development status | Developed, Developing |
| Annual_Lung_Cancer_Deaths | integer | Deaths per year in country | country-level statistic |
| Lung_Cancer_Prevalence_Rate | float | Prevalence per 100k | country-level statistic |
| Mortality_Rate | float | Mortality rate for individual | 0.0-3.5 |

25 countries covered: USA, China, India, Brazil, Germany, UK, Japan, Russia, South Africa, Nigeria, Mexico, France, Italy, Egypt, Turkey, Iran, Pakistan, Bangladesh, Vietnam, Philippines, Indonesia, Myanmar, Ethiopia, DR Congo, Thailand



--



#### WHO_pollution.csv - WHO ambient air pollution mortality data
Source: [WHO Global Health Observatory](https://datasource.kapsarc.org/explore/dataset/ambientairpollution_attributabledeaths/information/?disjunctive.indicator&disjunctive.parentlocation&disjunctive.location&disjunctive.dim1&disjunctive.dim2&sort=period&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJsaW5lIiwiZnVuYyI6IkFWRyIsInlBeGlzIjoiZmFjdHZhbHVlbnVtZXJpY2hpZ2giLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiJyYW5nZS1BY2NlbnQifV0sInhBeGlzIjoiaW5kaWNhdG9yIiwibWF4cG9pbnRzIjpudWxsLCJ0aW1lc2NhbGUiOiIiLCJzb3J0IjoiIiwic2VyaWVzQnJlYWtkb3duIjoiZGltMSIsImNvbmZpZyI6eyJkYXRhc2V0IjoiYW1iaWVudGFpcnBvbGx1dGlvbl9hdHRyaWJ1dGFibGVkZWF0aHMiLCJvcHRpb25zIjp7ImRpc2p1bmN0aXZlLmluZGljYXRvciI6dHJ1ZSwiZGlzanVuY3RpdmUucGFyZW50bG9jYXRpb24iOnRydWUsImRpc2p1bmN0aXZlLmxvY2F0aW9uIjp0cnVlLCJkaXNqdW5jdGl2ZS5kaW0xIjp0cnVlLCJkaXNqdW5jdGl2ZS5kaW0yIjp0cnVlLCJzb3J0IjoicGVyaW9kIn19fV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWUsInRpbWVzY2FsZSI6IiJ9)

Size: 13,177 rows × 11 columns

Separator: semicolon (;)

Years covered: 2016-2019

The dataset gives annual country-level estimates of deaths caused by ambient air pollution.

| Column | Type | Description | Example Values |
|---|---|---|---|
| Year | integer | Data year | 2016, 2019 |
| Country | string | Country name | Finland, China, USA |
| Region | string | WHO region | EUR, WPRO, AMRO |
| Indicator | string | WHO indicator | Ambient air pollution attributable deaths |
| Gender | string | Sex | Male, Female, Both sexes |
| Cause | string | Cause of death | Trachea/bronchus/lung cancers, COPD, Stroke, Ischaemic heart disease |
| Dim2ValueCode | string | Dimension code | e.g., "ENVCAUSE000" |
| ValueNumeric | float | Numerical Value  | e.g., 0.17 |
| ValueLow | float | Lowest Value | e.g., 0.0 |
| ValueHigh | float | Highest Value | e.g., 0.15 |
| Value | string | Formatted range string | 0.23 [0.12 - 0.38] |



--



#### abstract-lungcancer.txt - PubMed scientific abstracts (unstructured)
Source: [PubMed](https://pubmed.ncbi.nlm.nih.gov/?term=lung+cancer) - We extracted 10,000 abstracts with keyword 'Lung Cancer' from PubMed articles.

Size: 487,202 lines

Format: Numbered sequential abstracts (1. Journal. Year...)



**Example entry structure**:

1.Int J Mol Sci. 2021 Aug 12;22(16):8661. doi: 10.3390/ijms22168661.

Current and Future Development in Lung Cancer Diagnosis.

Nooreldeen R(1), Bach H(1).

Author information:
(1)Division of Infectious Diseases, Faculty of Medicine, The University of 
British Columbia, Vancouver, BC V6H 3Z6, Canada.

Lung cancer is the leading cause of cancer-related deaths in North America and 
other developed countries. One of the reasons lung cancer is at the top of the 
list is that it is often not diagnosed until the cancer is at an advanced stage. 
Thus, the earliest diagnosis of lung cancer is crucial, especially in screening 
high-risk populations, such as smokers, exposure to fumes, oil fields, toxic 
occupational places, etc. Based on the current knowledge, it looks that there is 
an urgent need to identify novel biomarkers. The current diagnosis of lung 
cancer includes different types of imaging complemented with pathological 
assessment of biopsies, but these techniques can still not detect early lung 
cancer developments. In this review, we described the advantages and 
disadvantages of current methods used in diagnosing lung cancer, and we provide 
an analysis of the potential use of body fluids as carriers of biomarkers as 
predictors of cancer development and progression.

DOI: 10.3390/ijms22168661
PMCID: PMC8395394
PMID: 34445366 [Indexed for MEDLINE]

Conflict of interest statement: Authors reported no conflict of interest.



**Risk keywords extracted** 

We extracted the following keywords associated with lunge cancer from the available abstracts.

RISK_TERMS = [
    'smoking', 'tobacco', 'cigarette', 'radon', 'asbestos',
    'pm2.5', 'pm10', 'particulate', 'pollution', 'carcinogen',
    'exposure', 'occupational', 'genetic', 'mutation',
    'adenocarcinoma', 'squamous', 'small cell', 'non-small cell'
]

--


#### Streaming Data - Air Quality API

The streaming or live data is not stored in this directory. We are using API to fetch the data in real-time. 

Endpoint: https://air-quality-api.open-meteo.com/v1/air-quality

The API call is made during the execution of Bronze_Ingestion.ipynb notebook. In this case, we get the current air quality reading. 

| Field | Type | Description |
|---|---|---|
| latitude / longitude | float | Coordinates used for the request |
| time | string | Hourly timestamp |
| pm2_5 | float | PM2.5 particulate concentration (µg/m³) |
| pm10 | float | PM10 particulate concentration (µg/m³) |

The data accumulates as we call the API key with each run. 



--

## Note

All the mentioned files are large enough, so upload them to the Databricks Volume (`/Volumes/workspace/bronze/raw_files/`) before any pipeline execution. The real-time air-quality is fetched upon execution. 


