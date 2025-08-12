#!/bin/bash
# The definitive and corrected script to deploy the application to Hugging Face Spaces.
set -e

# --- Correct Configuration ---
HF_ORG="fneurociencias"
HF_SPACE="Neurodiagnoses"
HF_USER="ManMenGon" # Your username is used for authentication

# Check for the secure token
if [ -z "$HF_TOKEN" ]; then
    echo "ERROR: The HF_TOKEN secret is not set. Please ensure it's configured in the repository's Codespaces secrets and rebuild the Codespace if necessary."
    exit 1
fi

echo "--> STEP 1: Cloning the correct Hugging Face Space: ${HF_ORG}/${HF_SPACE}"
# We remove any previous temporary directory to ensure a clean start.
rm -rf hf_space_temp
git clone "https://$HF_USER:$HF_TOKEN@huggingface.co/spaces/$HF_ORG/$HF_SPACE" hf_space_temp

echo -e "\n--> STEP 2: Copying application files..."
# Copy all necessary components for the Gradio app to run.
cp app.py hf_space_temp/
cp requirements.txt hf_space_temp/
cp unified_orchestrator.py hf_space_temp/
cp -r tools/ hf_space_temp/
cp -r models/ hf_space_temp/
mkdir -p hf_space_temp/data/simulated
cp -r data/simulated/ hf_space_temp/data/
echo "--> Files copied successfully."

echo -e "\n--> STEP 3: Committing and pushing the application..."
cd hf_space_temp
git add .
git commit -m "feat: Deploy full 3-axis application"
git push

echo -e "\n--> STEP 4: Cleaning up..."
cd ..
rm -rf hf_space_temp
echo "--> Cleanup complete."

echo -e "\n========================================================================"
echo '=== ¡DESPLIEGUE INICIADO! Tu aplicación se está construyendo en Hugging Face. ==='
echo '========================================================================'
