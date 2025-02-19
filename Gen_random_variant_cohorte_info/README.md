# 🧬 Random Patient Variant Generator

This script generates **randomized mitochondrial variant data** for a set of patients.  
Each patient is assigned **30-50 variants (configurable)**, with key attributes like **haplogroup, tissue type, variant type, and heteroplasmy rates**.

---

## 📥 Installation

Make sure you have **Python 3** installed. You also need **pandas** and **numpy**:

```sh
pip install pandas numpy
```

---

## 🛠 Usage

Run the script from the command line:

```sh
python generate_patients.py --num_patients 150 --min_variants 35 --max_variants 60 --output my_patients.csv
```

### **📝 Arguments**
| Argument | Description | Default |
|----------|-------------|---------|
| `--num_patients` | Number of patients to generate | `100` |
| `--min_variants` | Minimum number of variants per patient | `30` |
| `--max_variants` | Maximum number of variants per patient | `50` |
| `--output` | Output CSV file name | `patients_random_variants.csv` |

---

## 📊 Example Output
The script generates a **CSV file** with the following columns:

| Column | Description |
|--------|-------------|
| `chr` | Mitochondrial chromosome (`chrMT`) |
| `pos` | Variant position (random between 1-16569) |
| `ref` | Reference allele (`A, T, C, G`) |
| `alt` | Alternate allele (`A, T, C, G`) |
| `heteroplasmy_rate` | Random float **(0-1)** |
| `patient_id` | Unique patient ID (e.g., `PAT001`) |
| `sex` | `M` or `F` |
| `age_of_onset` | Random age (1-80) |
| `age_at_sampling` | Random age (>= age_of_onset, max 90) |
| `tissue` | `Blood`, `Urine` |
| `haplogroup` | Weighted random haplogroup (`H8472`, `J5123`, etc.) |
| `m3243_het` | Random float (0-1) |
| `m3243_het_normalized` | Random float (0-1) > m3243_het |

---

## 🔍 Example CSV Output
```
chr,pos,ref,alt,heteroplasmy_rate,patient_id,sex,age_of_onset,age_at_sampling,tissue,type,haplogroup,m3243_het,m3243_het_normalized,id,hap_maj,hap_min
chrMT,1345,A,G,0.765,PAT001,M,45,50,Muscle,Pathogenic,H4728,0.452,0.783,3481,L2,B
chrMT,7896,C,T,0.123,PAT001,M,45,50,Blood,Benign,L31024,0.601,0.921,5910,L5,A
chrMT,14078,G,C,0.543,PAT001,M,45,50,Skin,VUS,K8472,0.378,0.632,8123,L1,E
chrMT,8765,T,A,0.312,PAT002,F,60,62,Brain,Pathogenic,U5237,0.255,0.487,2345,L3,D
chrMT,4563,C,G,0.982,PAT002,F,60,62,Blood,Benign,T2934,0.759,0.841,6789,L4,F
```

## Upgrade 

- Add real Haplogroups
- Base random on other distributions