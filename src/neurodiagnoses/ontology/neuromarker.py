from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional

# Based on the "Core Biomarker Categories" table from the project documentation.
class BiomarkerCategory(Enum):
    """Enumeration for the core biomarker categories in the Neuromarker ontology."""
    MOLECULAR = "Molecular Biomarkers"
    NEUROIMAGING = "Neuroimaging Biomarkers"
    FLUID = "Fluid Biomarkers"
    NEUROPHYSIOLOGICAL = "Neurophysiological Biomarkers"
    DIGITAL = "Digital Biomarkers"
    CLINICAL_PHENOTYPIC = "Clinical Phenotypic Markers"
    GENETIC = "Genetic Biomarkers"
    ENVIRONMENTAL = "Environmental & Lifestyle Factors"

@dataclass
class Biomarker:
    """A generic data structure for a single biomarker instance."""
    name: str
    value: float
    unit: str
    category: BiomarkerCategory
    source_dataset: Optional[str] = None # e.g., "ADNI", "PPMI"

@dataclass
class GeneticData:
    """Structured data for genetic information as per the specification."""
    pathogenic_variants: List[str] = field(default_factory=list)
    disease_specific_risk: List[str] = field(default_factory=list)
    non_specific_risk: List[str] = field(default_factory=list)

@dataclass
class PatientRecord:
    """
    A unified data structure for a patient, designed to hold data
    categorized by the Neuromarker ontology. This will be the input
    to the 'Modality-Agnostic Processing' layer.
    """
    patient_id: str
    biomarkers: List[Biomarker] = field(default_factory=list)
    genetics: Optional[GeneticData] = None

    def add_biomarker(self, name: str, value: float, unit: str, category: BiomarkerCategory, source: str = None):
        """Helper method to add a biomarker to the record."""
        self.biomarkers.append(
            Biomarker(name=name, value=value, unit=unit, category=category, source_dataset=source)
        )
