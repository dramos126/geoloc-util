import subprocess
import json
import sys
import pytest

def run_geoloc_util(args):
    cmd = [sys.executable, "geoloc_util.py"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"geoloc_util failed: {result.stderr}"
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Output is not valid JSON: {result.stdout}")
    return output

def extract_result(result_entry):
    key, value = list(result_entry.items())[0]
    return key, value

def verify_output(output, expected_length):
    assert isinstance(output, list), "Output should be a list"
    assert len(output) == expected_length, f"Should return {expected_length} result(s)"

def verify_default_keys(result):
    assert "error" not in result, f"Unexpected error: {result.get('error')}"
    assert "name" in result, "Result should contain a 'name' field"
    assert "lat" in result, "Result should contain a 'lat' field"
    assert "lon" in result, "Result should contain a 'lon' field"
    assert result.get("country") == "US", "Country should be US"

def test_city_state():
    output = run_geoloc_util(["Torrance, CA"])
    verify_output(output, 1)
    query, result = extract_result(output[0])
    verify_default_keys(result)
    assert result["state"] == "California", "State should be California for Torrance, CA"

def test_zip_code():
    output = run_geoloc_util(["27712"])
    verify_output(output, 1)
    query, result = extract_result(output[0])
    verify_default_keys(result)
    assert result.get("zip") == "27712", "Zip field should match the input"

def test_multiple_locations():
    locations = ["Madison, WI", "12345", "Chicago, IL", "10001"]
    output = run_geoloc_util(locations)
    verify_output(output, len(locations))
    for entry in output:
        query, result = extract_result(entry)
        assert "lat" in result, f"Result for query '{query}' should have a 'lat' field"
        assert "lon" in result, f"Result for query '{query}' should have a 'lon' field"

# Negative test: use an invalid city/state input.
def test_invalid_city():
    output = run_geoloc_util(["FakeCity, ZZ"])
    verify_output(output, 1)
    query, result = extract_result(output[0])
    assert "error" in result, "Expected an error for an invalid city"
    assert "No results" in result["error"], "Error message should indicate no results"

# Negative test: use a zip code that does not exist.
def test_invalid_zip():
    output = run_geoloc_util(["00000"])
    verify_output(output, 1)
    query, result = extract_result(output[0])
    assert "error" in result, "Expected an error for an invalid zip code"
    assert ("Error" in result["error"] or "No results" in result["error"]), "Error message should indicate a problem"

def test_empty_string():
    output = run_geoloc_util([""])
    verify_output(output, 1)
    query, result = extract_result(output[0])
    assert "error" in result, "Expected an error for an empty location string"

# Test a combination of valid and invalid inputs.
def test_mixed_valid_invalid():
    locations = ["Madison, WI", "FakeCity, ZZ", "00000", "Chicago, IL"]
    output = run_geoloc_util(locations)
    verify_output(output, len(locations))
    
    for entry in output:
        query, result = extract_result(entry)
        if query in ["FakeCity, ZZ", "00000"]:
            assert "error" in result, f"Expected an error for query '{query}'"
        else:
            assert "error" not in result, f"Did not expect an error for query '{query}'"
            assert "lat" in result, f"Result for query '{query}' should contain a 'lat' field"
            assert "lon" in result, f"Result for query '{query}' should contain a 'lon' field"
