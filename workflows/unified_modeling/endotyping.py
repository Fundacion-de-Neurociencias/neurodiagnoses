"""
Patient Endotyping using Unsupervised Clustering and XAI.

This script applies K-Means clustering to identify patient subgroups (endotypes)
and then uses SHAP to explain the characteristics of these clusters.

Functions:
    perform_endotyping: Loads data, scales, clusters, explains, and saves results.
"""

import pandas as pd
import os
import shap
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Define paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Note: We now use the generic featured data, not the disease-specific ones for a holistic view
INPUT_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'unified_patient_data.parquet')
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'endotyped_patient_data.parquet')
REPORT_DIR = os.path.join(PROJECT_ROOT, 'reports', 'xai')

def perform_endotyping(input_path, output_path, report_dir, n_clusters=2):
    """
    Loads data, performs K-Means clustering, generates a SHAP explanation
    for the clustering, and saves the results.

    Args:
        input_path (str): Path to the unified Parquet file.
        output_path (str): Path to save the Parquet file with endotype labels.
        report_dir (str): Directory to save the XAI report.
        n_clusters (int): The number of endotypes to identify.
    """
    print("--- Starting Patient Endotyping and Explanation Process ---")
    os.makedirs(report_dir, exist_ok=True)

    try:
        df = pd.read_parquet(input_path)
    except FileNotFoundError:
        print(f"Error: The file was not found at {input_path}. Run unification first.")
        return None

    # --- 1. Select and Prepare Features for Clustering ---
    features_for_clustering = df.select_dtypes(include=['float64', 'int64']).copy()
    # Drop non-biomarker columns and fill NaNs for robustness
    features_for_clustering = features_for_clustering.drop(columns=['years_of_education'])
    features_for_clustering.fillna(features_for_clustering.median(), inplace=True)
    print(f"Selected {len(features_for_clustering.columns)} features for clustering.")

    # --- 2. Scale the Features ---
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features_for_clustering)
    
    # --- 3. Perform Clustering ---
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(scaled_features)
    print(f"K-Means clustering complete. Identified {n_clusters} endotypes.")

    # --- 4. Explain the Clustering with SHAP ---
    print("Explaining cluster assignments with SHAP...")
    # SHAP needs a model with a `predict` function. We can use the trained kmeans.
    # We use KernelExplainer as K-Means is not a tree or linear model.
    # We pass the scaled data as the background for the explainer.
    explainer = shap.KernelExplainer(kmeans.predict, scaled_features)
    shap_values = explainer.shap_values(scaled_features)

    # --- 5. Generate and Save SHAP Summary Plot ---
    summary_plot_path = os.path.join(report_dir, 'endotyping_shap_summary.png')
    plt.figure()
    shap.summary_plot(shap_values, features=features_for_clustering, show=False)
    plt.title(f"Feature Importance for Endotype Clustering (k={n_clusters})")
    plt.savefig(summary_plot_path, bbox_inches='tight')
    plt.close()
    print(f"Saved endotyping explanation plot to: {summary_plot_path}")

    # --- 6. Add Endotype Labels and Save Result ---
    df_endotyped = df.copy()
    df_endotyped['endotype'] = clusters
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_endotyped.to_parquet(output_path, index=False)
    print(f"Endotyped data saved to: {output_path}")

    print("\n--- Endotyping Process Complete ---")
    return df_endotyped

if __name__ == "__main__":
    perform_endotyping(INPUT_PATH, OUTPUT_PATH, REPORT_DIR)
