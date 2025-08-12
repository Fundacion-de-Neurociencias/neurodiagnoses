#!/bin/bash
# Script to add the missing matplotlib dependency and redeploy to Hugging Face.
set -e

echo "--> STEP 1: Adding 'matplotlib' to requirements.txt..."
# We append the missing library to the end of the requirements file.
echo "matplotlib" >> requirements.txt
# Also install it in our current Codespace environment to be thorough.
pip install -r requirements.txt
echo "--> requirements.txt updated and dependencies installed."

echo -e "\n--> STEP 2: Committing the dependency fix to the main GitHub repository..."
git add requirements.txt
git commit -m "fix(deps): Add missing matplotlib dependency for SHAP plots"
git push
echo "--> Fix has been pushed to the main GitHub repository."

echo -e "\n--> STEP 3: Re-deploying the updated application to Hugging Face Spaces..."
# We execute the deployment script that we know works.
# This will copy the updated repository contents, including the new requirements.txt,
# to your Hugging Face Space and trigger a new build.
bash deploy_to_hf.sh

echo -e "\n========================================================================"
echo "=== ¡ARREGLO ENVIADO! La aplicación se está reconstruyendo en Hugging Face. ==="
echo "========================================================================"
