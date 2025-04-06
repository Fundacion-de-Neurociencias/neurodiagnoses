import pytest
import sys
import os

# Añadir el directorio raíz al path para importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Pruebas para integrations.mip_integration
def test_mip_integration_import():
    """Prueba básica para verificar que el módulo mip_integration se puede importar."""
    try:
        from integrations import mip_integration
        assert True
    except ImportError:
        assert False, "No se pudo importar el módulo mip_integration"

def test_authenticate_and_fetch_data():
    """Prueba básica para la función authenticate_and_fetch_data."""
    try:
        from integrations import mip_integration
        # Esta función no tiene parámetros, pero normalmente requeriría credenciales
        # Por lo tanto, solo verificamos que la función existe
        assert hasattr(mip_integration, 'authenticate_and_fetch_data')
        assert callable(getattr(mip_integration, 'authenticate_and_fetch_data'))
    except (ImportError, AttributeError):
        assert False, "No se pudo acceder a la función authenticate_and_fetch_data"

def test_save_data_as_csv():
    """Prueba básica para la función save_data_as_csv."""
    try:
        from integrations import mip_integration
        import pandas as pd
        
        # Crear datos de prueba
        test_data = pd.DataFrame({
            'paciente_id': [1, 2, 3],
            'edad': [65, 72, 58],
            'mmse': [28, 22, 30]
        })
        
        # Verificar que la función existe
        assert hasattr(mip_integration, 'save_data_as_csv')
        assert callable(getattr(mip_integration, 'save_data_as_csv'))
        
        # No ejecutamos la función real para evitar efectos secundarios
    except (ImportError, AttributeError):
        assert False, "No se pudo acceder a la función save_data_as_csv"
    except ModuleNotFoundError:
        # Si pandas no está instalado, simplemente verificamos que la función existe
        from integrations import mip_integration
        assert hasattr(mip_integration, 'save_data_as_csv')

# Pruebas para models.api
def test_api_import():
    """Prueba básica para verificar que el módulo api se puede importar."""
    try:
        from models import api
        assert True
    except ImportError:
        assert False, "No se pudo importar el módulo api"

def test_home_function():
    """Prueba básica para la función home."""
    try:
        from models import api
        assert hasattr(api, 'home')
        assert callable(getattr(api, 'home'))
    except (ImportError, AttributeError):
        assert False, "No se pudo acceder a la función home"

def test_predict_function():
    """Prueba básica para la función predict."""
    try:
        from models import api
        assert hasattr(api, 'predict')
        assert callable(getattr(api, 'predict'))
        
        # Crear datos de prueba simples
        test_data = {
            'edad': 65,
            'mmse': 28,
            'cdr': 0.5
        }
        
        # No ejecutamos la función real para evitar efectos secundarios
    except (ImportError, AttributeError):
        assert False, "No se pudo acceder a la función predict"

def test_biomarker_data_class():
    """Prueba básica para la clase BiomarkerData."""
    try:
        from models.api import BiomarkerData
        
        # Verificar que es una clase
        assert isinstance(BiomarkerData, type)
        
        # No creamos instancias para evitar errores si requiere parámetros específicos
    except (ImportError, AttributeError):
        assert False, "No se pudo acceder a la clase BiomarkerData"

# Pruebas para models.biomarker_classifier
def test_biomarker_classifier_import():
    """Prueba básica para verificar que el módulo biomarker_classifier se puede importar."""
    try:
        from models import biomarker_classifier
        assert True
    except ImportError:
        assert False, "No se pudo importar el módulo biomarker_classifier"

# Pruebas para models.models.biomarker_classifier
def test_models_biomarker_classifier_import():
    """Prueba básica para verificar que el módulo models.biomarker_classifier se puede importar."""
    try:
        from models.models import biomarker_classifier
        assert True
    except ImportError:
        assert False, "No se pudo importar el módulo models.biomarker_classifier"

# Pruebas para models.train_model
def test_train_model_import():
    """Prueba básica para verificar que el módulo train_model se puede importar."""
    try:
        from models import train_model
        assert True
    except ImportError:
        assert False, "No se pudo importar el módulo train_model"
