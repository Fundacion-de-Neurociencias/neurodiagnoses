# Contributing to Neurodiagnoses

## Overview
Neurodiagnoses is an **open-source AI diagnostic ecosystem** for **complex central nervous system (CNS) disorders**. This project is supported by the **Fundación de Neurociencias** and integrates **clinical, neuroimaging, and molecular data** to enhance AI-driven diagnostics.

We welcome contributions from researchers, clinicians, and AI developers to improve the platform. Contributions can be in the form of **code, data curation, documentation, or clinical validation**.

## How to Contribute

### 1️⃣ Get Started
1. **Fork the Repository**: Visit [Neurodiagnoses GitHub](https://github.com/Fundacion-de-Neurociencias/neurodiagnoses) and fork the repository.
2. **Clone the Repo**: 
   ```sh
   git clone https://github.com/your-username/neurodiagnoses.git
   cd neurodiagnoses
   ```
3. **Set Up a Virtual Environment** (Recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

### 2️⃣ Contribution Guidelines
#### 🖥️ **Code Contributions**
- All code should follow **PEP8** and be properly documented.
- Submit **pull requests (PRs)** to the `develop` branch.
- Ensure your changes pass unit tests:
  ```sh
  pytest
  ```
- Major contributions require an **issue discussion** before implementation.

#### 📊 **Data Contributions**
- New datasets should be submitted through **EBRAINS** or **GitHub Datasets Directory**.
- Ensure data privacy compliance (GDPR, HIPAA).
- Convert datasets to **CSV, JSON, or HDF5** formats.
- Submit dataset metadata for documentation.

#### 📝 **Documentation Contributions**
- Improve guides in `docs/` directory.
- Submit edits via pull requests.

### 3️⃣ Issue Tracking
- View open issues: GitHub Issues
- Report new issues with detailed descriptions.
- Label issues appropriately (`bug`, `enhancement`, `documentation`).

### 4️⃣ Join the Discussion
- GitHub Discussions: Neurodiagnoses Forum
- Slack/Discord: Community link in repository README.
- eBrains Collaboration: Neurodiagnoses on eBrains

### 5️⃣ Licensing & CLA
Neurodiagnoses follows a **dual-license model (MIT + Commercial)**.
- **MIT License** allows unrestricted usage for research & non-commercial applications.
- **Commercial Licensing** is required for industry applications (contact info@neurodiagnoses.com).
- All contributors must sign a **Contributor License Agreement (CLA)** before merging PRs.

### 🚀 Get Involved Today!
We appreciate your interest in Neurodiagnoses! Start contributing today and help shape the future of AI-assisted CNS diagnosis.
