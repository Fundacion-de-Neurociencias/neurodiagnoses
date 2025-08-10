import random
from neurodiagnoses_code.axis_2.classifier import predict_probabilities, CSF_FEATURES

def main():
    print("=====================================================")
    print("===   INICIANDO SIMULACIÓN DE NEURODIAGNÓSTICO    ===")
    print("=====================================================")
    print("\n[INFO] Obteniendo perfil proteómico del paciente...")
    sample_patient_data = {protein: random.uniform(0.0, 2.5) for protein in CSF_FEATURES}
    print("  > Perfil obtenido con éxito.")
    print("\n[INFO] Enviando perfil al clasificador del Eje 2...")
    # NOTA: Necesitamos entrenar un modelo primero para que esto funcione.
    # from neurodiagnoses_code.axis_2.classifier import train_model
    # train_model() 
    diagnostic_probabilities = predict_probabilities(sample_patient_data)
    if diagnostic_probabilities:
        print("  > Predicción recibida con éxito.")
        print("\n----------------- RESULTADO DEL DIAGNÓSTICO -----------------")
        class_names = {0: 'Control (CO)', 1: 'Alzheimer (AD)', 2: 'Parkinson (PD)', 3: 'Frontotemporal (FTD)', 4: 'Cuerpos de Lewy (DLB)'}
        for class_index, probability in sorted(diagnostic_probabilities.items(), key=lambda item: item[1], reverse=True):
            class_name = class_names.get(class_index, f"Clase Desconocida {class_index}")
            print(f"  - {class_name:<25}: {probability:.2%}")
        print("-------------------------------------------------------------")
    else:
        print("\n[ERROR] No se pudo obtener un diagnóstico. Asegúrese de que el archivo del modelo (axis2_model.pkl) existe.")
if __name__ == '__main__':
    main()
