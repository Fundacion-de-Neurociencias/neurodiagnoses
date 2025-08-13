# -*- coding: utf-8 -*-
"""
NACC Data Parser for Neurodiagnoses Project.

This module provides a parser for the National Alzheimer's Coordinating Center (NACC)
dataset, transforming raw CSV data into standardized PatientRecord objects.
"""

import pandas as pd
from tools.ontology.neuromarker import PatientRecord, Biomarker, BiomarkerCategory

class NaccParser:
    """
    Parses NACC data from a CSV file into a list of PatientRecord objects.
    """
    def __init__(self, data_path):
        self.data_path = data_path

    def parse(self):
        """
        Reads the NACC CSV data and converts it into PatientRecord objects.
        
        This is a simplified parser for demonstration. A full implementation
        would handle various forms, longitudinal data, and complex mappings.
        """
        df = pd.read_csv(self.data_path)
        
        patient_records = []
        # Group by NACCID to handle longitudinal data for each patient
        for patient_id, group in df.groupby('NACCID'):
            # For simplicity, we'll take the last visit's data for some fields
            # A real parser would aggregate or process all visits.
            last_visit = group.sort_values(by=['VISITYR', 'VISITMO', 'VISITDAY']).iloc[-1]
            
            # Create a PatientRecord
            patient = PatientRecord(
                patient_id=patient_id,
                metadata={
                    'age': last_visit['NACCAGE'],
                    'sex': 'Male' if last_visit['SEX'] == 1 else 'Female'
                }
            )
            
            # Add MMSE as a biomarker
            patient.add_biomarker(
                name='MMSE',
                value=last_visit['NACCMMSE'],
                unit='points',
                category=BiomarkerCategory.CLINICAL_PHENOTYPIC
            )
            
            patient_records.append(patient)
            
        return patient_records
