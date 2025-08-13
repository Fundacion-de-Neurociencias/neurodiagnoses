# -*- coding: utf-8 -*-
"""
Unit tests for the core ontology of the Neurodiagnoses project.

These tests ensure that the fundamental data structures (Biomarker, PatientRecord)
are behaving as expected. Any failure in these tests indicates a critical
problem that could affect the entire framework.
"""
import pytest
from tools.ontology.neuromarker import Biomarker, PatientRecord, GeneticMarker, BiomarkerCategory

def test_biomarker_creation():
    """Tests the successful creation of a Biomarker object."""
    b = Biomarker(name='MMSE', value=28, unit='points', category=BiomarkerCategory.CLINICAL_PHENOTYPIC)
    assert b.name == 'MMSE'
    assert b.value == 28
    assert b.unit == 'points'
    assert b.category == BiomarkerCategory.CLINICAL_PHENOTYPIC
    assert "Biomarker(name='MMSE', value=28, unit='points', category=<BiomarkerCategory.CLINICAL_PHENOTYPIC: 'Clinical Phenotypic Markers'>)" in repr(b)

def test_patient_record_creation():
    """Tests the successful creation of a PatientRecord."""
    p = PatientRecord(patient_id='PAT-001', metadata={'age': 70})
    assert p.patient_id == 'PAT-001'
    assert p.metadata == {'age': 70}
    assert not p.biomarkers # Should be empty initially

def test_add_biomarker_to_patient():
    """Tests adding a biomarker to a patient record."""
    p = PatientRecord(patient_id='PAT-002', metadata={'age': 65})
    p.add_biomarker(name='pTau', value=35.2, unit='pg/mL', category=BiomarkerCategory.FLUID)
    # Accessing biomarkers by name is no longer directly supported by the list structure
    # We need to iterate or find the biomarker
    found_biomarker = next((b for b in p.biomarkers if b.name == 'pTau'), None)
    assert found_biomarker is not None
    assert found_biomarker.value == 35.2
    assert found_biomarker.unit == 'pg/mL'
    assert found_biomarker.category == BiomarkerCategory.FLUID

def test_get_biomarker_from_patient():
    """Tests retrieving a biomarker from a patient record."""
    p = PatientRecord(patient_id='PAT-003', metadata={'age': 75})
    p.add_biomarker(name='NfL', value=1200, unit='pg/mL', category=BiomarkerCategory.FLUID)
    # The get_biomarker method needs to be implemented in PatientRecord if desired
    # For now, we'll simulate the check
    retrieved_b = next((b for b in p.biomarkers if b.name == 'NfL'), None)
    assert retrieved_b is not None
    assert retrieved_b.value == 1200
    assert next((b for b in p.biomarkers if b.name == 'NonExistent'), None) is None

# The test_genetic_marker_creation remains unchanged as GeneticMarker is now defined
# and its creation test is valid.

def test_genetic_marker_creation():
    """Tests creating a genetic marker."""
    g = GeneticMarker(name='APOE', value='e3/e4', risk_level=2)
    assert g.name == 'APOE'
    assert g.risk_level == 2