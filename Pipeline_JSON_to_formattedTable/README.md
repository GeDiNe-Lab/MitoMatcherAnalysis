# **JSON Clinical Data to Formated Table for Analysis**

This Python-based pipeline is designed to process clinical data stored in JSON format. The goal of this pipeline is to transform raw data files into a structured dataset for downstream analysis. It extracts, filters, and organizes data related to Human Phenotype Ontology (HPO) terms, variants, and clinical data. The final output is a clinical table that combines these data sources.

---

## **Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Arguments](#arguments)
- [Workflow Overview](#workflow-overview)
- [Modules](#modules)
- [Logging](#logging)
- [Output](#output)
- [Upgrades](#upgrades)

---

## **Installation**

### Prerequisites

Ensure you have the following dependencies installed:
- Python 3.x
- Pip (Python package installer)

### Installation Steps

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/GeDiNe-Lab/MitoMatcherAnalysis.git
   ```

2. Navigate into the project directory:
   ```bash
   cd MitoMatcherAnalysis/Pipeline_JSON_to_formattedTable
   ```

---

## **Usage**

To run the pipeline, use the following command:

```bash
python3 Pipeline_JSON_to_formattedTable/main.py <input_folder> <output_folder> <hpo_path> <variants> <het_threshold> <norm_status>
```

Where:
- `<input_folder>`: Path to the folder containing the input JSON files.
- `<output_folder>`: Path where the output CSV files and logs will be stored.
- `<hpo_path>`: Path to the file containing HPO terms for matching.
- `<variants>`: Comma-separated list of variants (e.g., `"A3243G,A73G"`).
- `<het_threshold>`: Minimum threshold for variant heteroplasmy rate (float, e.g., `0.1`).
- `<norm_status>`: Normalization status for mutation analysis (e.g., `'yes'`, `'no'`, `'blood'`, `'urine'`).

### Example:
```bash
python3 Pipeline_JSON_to_formattedTable/main.py /path/to/input /path/to/output /path/to/hpo_file "A3243G,A73G" 0.1 "yes"
```

---

## **Workflow Overview**

### **Step 1: Verification of JSON Files**
The pipeline starts by verifying the input JSON files. Each file is validated to ensure that it follows the required format and contains the necessary data. Any files that do not pass verification are logged and skipped.

### **Step 2: HPO Data Processing**
For each valid JSON file, the pipeline extracts the relevant HPO terms either from an API request or a local file. This information is then aggregated into a global dictionary.

### **Step 3: Generation of Presence/Absence Table**
A table is generated that records the presence or absence of each HPO term for each patient, providing a structured way to analyze phenotype data.

### **Step 4: Variant Data Processing**
Variant information is extracted and filtered based on the provided threshold (`het_threshold`). The pipeline checks for variants in the input files and generates a table of variant data.

### **Step 5: Clinical Table Generation**
A final clinical table is generated that contains key patient information, associated HPO terms, and variant data. This table is stored as a CSV file in the output folder.

---

## **Modules**

The pipeline leverages several modules to separate functionality and ensure maintainability:

1. **HPO_terms_API_request.py**: Contains logic for querying an API for HPO terms.
2. **HPO_terms_infile_research.py**: Performs offline research for HPO terms based on local files.
3. **HPO_unique_csv.py**: Creates a CSV file containing the concatenated HPO data.
4. **variant_generation_csv.py**: Handles the generation of a CSV file containing concatenated variant data.
5. **generate_absence_presence_HPO.py**: Creates a presence/absence table for HPO terms.
6. **generation_clinical_table.py**: Generates the final clinical table with combined patient data.

---

## **Logging**

The pipeline generates logs of its execution in the `process.log` file in the output folder. It logs information at various levels (e.g., `INFO`, `ERROR`, `DEBUG`) depending on the event.

- `INFO`: General processing updates.
- `ERROR`: When errors occur, such as a file failing verification.
- `DEBUG`: Detailed debug messages (for development purposes).

Example log message:
```bash
2025-02-17 14:25:32,872 - INFO - Starting pipeline
2025-02-17 14:26:45,239 - ERROR - File 'patient_001.json' did not pass verification.
```

---

## **Output**

After running the pipeline, you will find the following files in the output folder:
- `concatenate_HPO.csv`: A CSV containing HPO terms for each patient.
- `concatenate_variants.csv`: A CSV containing variant information for each patient.
- `process.log`: A log file detailing the execution and errors (if any).
- `clinical_table.csv`: The final generated clinical table.


## **Upgrades**

- Tests
- Randomly generated input data