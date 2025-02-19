# Analysis_mito_cohorte

## Overview
This folder is designed for analyzing mitochondrial cohort data, focusing on clinical and genetic variant analyses.

## Repository Structure

```
Analysis_mito_cohorte/
│   ├── Analysis_mito_cohorte.Rproj  # R project file
│   ├── R                            # R scripts and markdowns
│   │   ├── clinical_analysis.Rmd
│   │   ├── m3243_cohort_analysis.Rmd
│   │   ├── mitochondrial_tRNA_analysis.Rmd
│   │   └── mitochondrial_tRNA_analysis.html
│   ├── README.md                    # This README file
│   ├── data                         # Input datasets
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
```

## Components

### 1. **Analysis_mito_cohorte (R-based Analysis)**
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
For any issues or questions, please create an issue in the repository or contact the project maintainers.

