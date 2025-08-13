# -*- coding: utf-8 -*-
"""
Unit tests for the data ingestion pipeline, specifically the NACC parser.

These tests use a small, controlled mock dataset to verify that the
parser correctly reads raw data and transforms it into standardized
PatientRecord objects.
"""

import sys
import os
import pytest
import pandas as pd

# Ensure the project root is in the Python path for module imports
# This is typically handled by setting PYTHONPATH or by the execution environment.
# For direct execution, consider adding the project root to sys.path if necessary.
# Example: sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tools.data_ingestion.parsers import nacc_parser # Assuming the parser module is named this
from tools.ontology.neuromarker import PatientRecord

@pytest.fixture
def mock_nacc_data_path():
    """Pytest fixture to provide the path to the mock data file."""
    return "tests/data/mock_nacc_data.csv"

def test_nacc_parser_initialization(mock_nacc_data_path):
    """Tests that the NACC parser can be initialized correctly."""
    parser = nacc_parser.NaccParser(mock_nacc_data_path)
    assert parser.data_path == mock_nacc_data_path

def test_nacc_parser_produces_patient_records(mock_nacc_data_path):
    """Tests that the parser's main method returns a list of PatientRecord objects."""
    parser = nacc_parser.NaccParser(mock_nacc_data_path)
    patient_records = parser.parse()
    assert isinstance(patient_records, list)
    # The mock data has two unique patients: PAT001 and PAT002
    assert len(patient_records) == 2 
    assert all(isinstance(p, PatientRecord) for p in patient_records)

def test_nacc_parser_correctly_parses_data(mock_nacc_data_path):
    """
    Tests that the data within the parsed PatientRecord objects is correct.
    """
    parser = nacc_parser.NaccParser(mock_nacc_data_path)
    patient_records = parser.parse()

    # Find patient PAT001 from the parsed records
    p1 = next((p for p in patient_records if p.patient_id == 'PAT001'), None)
    assert p1 is not None

    # PAT001 has two visits. The parser should handle multiple visits and
    # correctly extract and store biomarkers. Let's check the last visit's MMSE.
    mmse_biomarker = p1.get_biomarker('MMSE')
    assert mmse_biomarker is not None
    assert mmse_biomarker.value == 27 # From the second visit (age 73)
    
    # Check patient PAT002
    p2 = next((p for p in patient_records if p.patient_id == 'PAT002'), None)
    assert p2 is not None
    assert p2.get_biomarker('MMSE').value == 22
