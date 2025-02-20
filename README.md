# Analysis_mito_cohorte

## Overview
This project is designed for analyzing mitochondrial cohort data, focusing on clinical and genetic variant analyses. The repository is organized into multiple components that handle data preprocessing, variant annotation, and clinical table generation.


## More context

Mitochondrial diseases are highly heterogeneous, both clinically and genetically. 
The diagnostic network for mitochondrial diseases (MitoDiag) is developing a national clinico-biological database to reduce diagnostic error in these diseases. 
As part of the MITOMICS project, CHU d'Angers has developed Mitomatcher, a platform for sharing and querying genomic and clinical data, tailored to the needs of the MitoDiag network. Bioanalysis of the first patient cohorts thus constituted will enable the initiation of ancillary projects targeting mitochondrial genetics, including sSNV.


## Repository Structure

```
Analysis_mito_cohorte/
│   ├── Analysis_mito_cohorte.Rproj 
│   ├── R                            
│   │   ├── clinical_analysis.Rmd
│   │   ├── m3243_cohort_analysis.Rmd
│   │   ├── mitochondrial_tRNA_analysis.Rmd
│   │   └── mitochondrial_tRNA_analysis.html
│   ├── README.md                    
│   ├── data                        
│   │   ├── apogee2_score_filtered.txt
│   │   ├── apogee2_trna.csv
│   │   ├── concatenate_HPO.csv
│   │   ├── concatenate_variants.csv
│   │   ├── functional_variant_tRNA_anticodon_table.tsv
│   │   ├── genome_loci_table.csv
│   │   ├── mtGeneSize.txt
│   │   ├── presence_absence_hpos.csv
│   │   ├── random_dataset_var_20250219.csv
│   │   ├── resume_clinical_table.csv
│   │   └── tRNA_names.txt
├── Gen_random_variant_cohorte_info
│   ├── README.md
│   ├── random_dataset_var.csv
│   └── random_gen_of_m3243_var_cohorte.py
├── Pipeline_JSON_to_formattedTable
│   ├── README.md
│   ├── __pycache__
│   │   ├── HPO_terms.cpython-312.pyc
│   │   ├── HPO_terms_infile_research.cpython-312.pyc
│   │   ├── HPO_unique_csv.cpython-312.pyc
│   │   ├── JSON_verification.cpython-312.pyc
│   │   ├── generate_absence_presence_HPO.cpython-312.pyc
│   │   ├── generation_clinical_table.cpython-312.pyc
│   │   ├── variant_generation_csv.cpython-312.pyc
│   │   └── variants_unique_format.cpython-312.pyc
│   ├── data
│   │   └── local_hpo_version_2024-07-01_dict.json
│   ├── docs
│   ├── main.py
│   ├── pipeline
│   │   ├── HPO_terms_API_request.py
│   │   ├── HPO_terms_infile_research.py
│   │   ├── HPO_unique_csv.py
│   │   ├── JSON_verification.py
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── HPO_terms_API_request.cpython-312.pyc
│   │   │   ├── HPO_terms_infile_research.cpython-312.pyc
│   │   │   ├── HPO_unique_csv.cpython-312.pyc
│   │   │   ├── JSON_verification.cpython-312.pyc
│   │   │   ├── generate_absence_presence_HPO.cpython-312.pyc
│   │   │   ├── generation_clinical_table.cpython-312.pyc
│   │   │   ├── variant_generation_csv.cpython-312.pyc
│   │   │   └── variants_unique_format.cpython-312.pyc
│   │   ├── generate_absence_presence_HPO.py
│   │   ├── generation_clinical_table.py
│   │   ├── variant_generation_csv.py
│   │   └── variants_unique_format.py
│   └── tests
└── README.md # This README
```



## Components
### 1. **Gen_random_variant_cohorte_info**
This folder contains scripts and data for generating random variants in the mitochondrial cohort.
- `random_dataset_var.csv` - Randomly generated variant dataset.
- `random_gen_of_m3243_var_cohorte.py` - Python script for generating random variants.
- `README.md` - Description of the dataset generation process.

### 2. **Pipeline_JSON_to_formattedTable**
Processes JSON data and converts it into a formatted table for further analysis.
- `main.py` - Main script for executing the pipeline.
- `pipeline/` - Contains various Python scripts for JSON verification, variant formatting, and clinical table generation.
- `data/local_hpo_version_2024-07-01_dict.json` - HPO term dictionary for analysis.
- `tests/` - Contains test scripts for validating pipeline outputs.

### 3. **Analysis_mito_cohorte (R-based Analysis)**
Includes R markdown scripts and datasets for conducting clinical and genetic analyses.
- `clinical_analysis.Rmd` - R markdown for analyzing clinical data.
- `m3243_cohort_analysis.Rmd` - R markdown focused on m.3243A>G cohort analysis.
- `mitochondrial_tRNA_analysis.Rmd` - Analysis of mitochondrial tRNA variants.
- `data/` - Contains various datasets required for the analysis.

## Installation & Dependencies
### **R Environment Setup**
Ensure `renv` is used to manage package dependencies:
```r
install.packages("renv")
renv::restore()
```

## Running the Analysis
### **R Analysis**
Open `Analysis_mito_cohorte.Rproj` in RStudio and execute the markdown scripts as needed.


## Contact


[RAJOUTER CONTACTs]
[RAJOUTER FINANCEMENT]

