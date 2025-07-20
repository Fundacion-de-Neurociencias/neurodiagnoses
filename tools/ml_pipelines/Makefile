.PHONY: setup process_data train_models

setup:
	python -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt

process_data:
	python src/data_processing/adni_preprocessor.py
	python src/data_processing/ppmi_preprocessor.py

train_models:
	python src/modeling/tau_classifier.py
	python src/modeling/np3tot_regressor.py

docker_build:
	docker build -t neurodiagnosis-ml .
