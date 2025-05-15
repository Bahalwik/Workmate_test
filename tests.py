import pytest
import tempfile

from main import (
    read_employees_from_csv,
    calculate_payout,
    generate_payout_report
)


def create_temp_csv(content):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write(content)
        f.flush()
        return f.name


@pytest.fixture
def sample_csv_file_1():
    content = """id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
3,carol@example.com,Carol Williams,Design,170,60"""
    return create_temp_csv(content)


@pytest.fixture
def sample_csv_file_2():
    content = """department,id,email,name,hours_worked,rate
HR,101,grace@example.com,Grace Lee,160,45
Marketing,102,henry@example.com,Henry Martin,150,35
HR,103,ivy@example.com,Ivy Clark,158,38"""
    return create_temp_csv(content)


# Тесты для read_employees_from_csv
def test_read_employees_from_csv(sample_csv_file_1, sample_csv_file_2):
    test_employees = read_employees_from_csv([sample_csv_file_1, sample_csv_file_2])
    assert len(test_employees) == 6
    assert all(isinstance(e, dict) for e in test_employees)
    assert all('name' in e for e in test_employees)
    assert all('department' in e for e in test_employees)
    assert all('hours_worked' in e for e in test_employees)
    assert all('rate' in e for e in test_employees)


# Тесты для calculate_payout
def test_calculate_payout():
    test_employees = [
        {'department': 'HR', 'hours_worked': '160', 'rate': '50'},
        {'department': 'HR', 'hours_worked': '150', 'rate': '40'},
        {'department': 'Design', 'hours_worked': '170', 'rate': '60'},
    ]

    result = calculate_payout(test_employees)

    assert 'HR' in result
    assert 'Design' in result
    assert result['HR']['hours'] == 310
    assert result['HR']['payout'] == 160 * 50 + 150 * 40
    assert result['Design']['hours'] == 170
    assert result['Design']['payout'] == 170 * 60


# Тесты для generate_payout_report
def test_generate_payout_report():
    test_employees = [
        {'department': 'HR', 'name': 'Alice', 'hours_worked': '160', 'rate': '50'},
        {'department': 'HR', 'name': 'Bob', 'hours_worked': '150', 'rate': '40'},
        {'department': 'Design', 'name': 'Carol', 'hours_worked': '170', 'rate': '60'},
    ]

    payouts = calculate_payout(test_employees)
    report = generate_payout_report(payouts, test_employees)

    assert "HR" in report
    assert "Design" in report
    assert "Alice" in report
    assert "Bob" in report
    assert "Carol" in report
    assert "Total" in report
    assert "$8000" in report
    assert "$6000" in report
    assert "$10200" in report
