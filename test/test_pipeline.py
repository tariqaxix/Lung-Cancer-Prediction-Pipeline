
import pytest, requests, json
from jsonschema import validate, ValidationError
import pandas as pd

with open('docs/data_contract.json') as f:
    CONTRACT = json.load(f)
INPUT_SCHEMA = CONTRACT['input']
OUTPUT_SCHEMA = CONTRACT['output']

API_URL = 'http://localhost:8000'

VALID_INPUT = {
    'age': 55,
    'country': 'Finland',
    'gender': 'Male',
    'smoker': 'Yes',
    'years_of_smoking': 20,
    'cigarettes_per_day': 15
}



class TestDataContract:
    def test_valid_input_passes_schema(self):
        validate(instance=VALID_INPUT, schema=INPUT_SCHEMA)  # raises if invalid

    def test_missing_required_field_fails(self):
        bad = {k: v for k, v in VALID_INPUT.items() if k != 'age'}
        with pytest.raises(ValidationError):
            validate(instance=bad, schema=INPUT_SCHEMA)

    def test_age_out_of_range_fails(self):
        bad = {**VALID_INPUT, 'age': 999}
        with pytest.raises(ValidationError):
            validate(instance=bad, schema=INPUT_SCHEMA)

    def test_invalid_gender_fails(self):
        bad = {**VALID_INPUT, 'gender': 'X'}
        with pytest.raises(ValidationError):
            validate(instance=bad, schema=INPUT_SCHEMA)

    def test_invalid_smoking_status_fails(self):
        bad = {**VALID_INPUT, 'smoker': 'sometimes'}
        with pytest.raises(ValidationError):
            validate(instance=bad, schema=INPUT_SCHEMA)



class TestAPI:
    def test_health_endpoint(self):
        r = requests.get(f'{API_URL}/health')
        assert r.status_code == 200
        assert r.json()['status'] == 'ok'

    def test_predict_returns_200(self):
        r = requests.post(f'{API_URL}/predict', json=VALID_INPUT)
        assert r.status_code == 200

    def test_predict_response_schema(self):
        r = requests.post(f'{API_URL}/predict', json=VALID_INPUT)
        validate(instance=r.json(), schema=OUTPUT_SCHEMA)

    def test_risk_score_in_range(self):
        r = requests.post(f'{API_URL}/predict', json=VALID_INPUT)
        score = r.json()['risk_score']
        assert 0.0 <= score <= 1.0

    def test_risk_label_valid(self):
        r = requests.post(f'{API_URL}/predict', json=VALID_INPUT)
        assert r.json()['risk_label'].lower() in ['low', 'medium', 'high']

    def test_invalid_input_returns_422(self):
        r = requests.post(f'{API_URL}/predict', json={'age': 'old'})
        assert r.status_code == 422



class TestSampleData:
    def test_sample_csv_has_required_columns(self):
        df = pd.read_csv('data/sample_lung_cancer.csv')
        required = {'age', 'country', 'gender', 'lung_cancer_diagnosis'}
        assert required.issubset(set(df.columns))

    def test_no_negative_ages_in_sample(self):
        df = pd.read_csv('data/sample_lung_cancer.csv')
        assert (df['age'] >= 0).all()

    def test_cancer_column_is_binary(self):
        df = pd.read_csv('data/sample_lung_cancer.csv')
        assert set(df['lung_cancer_diagnosis'].unique()).issubset({'Yes', 'No'})
