import pandas as pd
import os

# Test 1: Check cleaned dataset exists
def test_cleaned_data_exists():
    path = 'data/cleaned/WB_undernourishment_cleaned.csv'
    assert os.path.exists(path), "Cleaned dataset file does not exist"
    print("PASS: Cleaned dataset exists")

# Test 2: Check dataset has correct columns
def test_correct_columns():
    df = pd.read_csv('data/cleaned/WB_undernourishment_cleaned.csv')
    expected_columns = ['Country', 'Year', 'Undernourishment_Pct']
    assert list(df.columns) == expected_columns, "Columns do not match expected"
    print("PASS: Columns are correct")

# Test 3: Check dataset has more than 100 rows
def test_minimum_rows():
    df = pd.read_csv('data/cleaned/WB_undernourishment_cleaned.csv')
    assert len(df) >= 100, "Dataset has fewer than 100 rows"
    print("PASS: Dataset has sufficient rows")

# Test 4: Check no missing values
def test_no_missing_values():
    df = pd.read_csv('data/cleaned/WB_undernourishment_cleaned.csv')
    assert df.isnull().sum().sum() == 0, "Dataset contains missing values"
    print("PASS: No missing values found")

# Test 5: Check year range is valid
def test_year_range():
    df = pd.read_csv('data/cleaned/WB_undernourishment_cleaned.csv')
    assert df['Year'].min() >= 2001, "Year range starts before 2001"
    assert df['Year'].max() <= 2023, "Year range ends after 2023"
    print("PASS: Year range is valid")

# Run all tests
if __name__ == "__main__":
    test_cleaned_data_exists()
    test_correct_columns()
    test_minimum_rows()
    test_no_missing_values()
    test_year_range()
    print("\nAll tests passed successfully!")
