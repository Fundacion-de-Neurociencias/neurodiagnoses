from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional

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
    value: any
    unit: str
    category: BiomarkerCategory

@dataclass
class GeneticData:
    """Structured data for genetic information."""
    key_markers: dict = field(default_factory=dict)

@dataclass
class PatientRecord:
    """A unified data structure for a patient, based on the Neuromarker ontology."""
    patient_id: str
    metadata: dict
    clinical_data: dict = field(default_factory=dict)
    genetic_data: Optional[GeneticData] = None
    neuropathology_data: dict = field(default_factory=dict)
    biomarkers: List[Biomarker] = field(default_factory=list)

    def add_biomarker(self, name: str, value: any, unit: str, category: BiomarkerCategory):
        """Helper method to add a biomarker to the record."""
        self.biomarkers.append(
            Biomarker(name=name, value=value, unit=unit, category=category)
        )
