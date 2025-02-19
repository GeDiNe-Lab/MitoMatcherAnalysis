import pandas as pd
import numpy as np
import random
import argparse

# Haplogroup distribution based on given counts
haplogroups = [
    ("A", 158), ("B", 324), ("C", 148), ("D", 334), ("E", 32), ("F", 104), ("G", 73), ("H", 978), ("HV", 94),
    ("I", 63), ("J", 240), ("K", 198), ("L0", 157), ("L1", 100), ("L2", 132), ("L3", 199), ("L4", 17),
    ("L5", 12), ("L6", 3), ("M", 686), ("N", 248), ("O", 3), ("P", 28), ("Q", 40), ("R", 39), ("S", 8),
    ("T", 230), ("U", 533), ("V", 61), ("W", 60), ("X", 89), ("Y", 14), ("Z", 27)
]

# Create weighted list of haplogroups
haplogroup_choices = [hg for hg, count in haplogroups for _ in range(count)]
                                                                         

def generate_patient_data(num_patients, min_variants, max_variants, output_file):
    data = []
    
    for i in range(1, num_patients + 1):
        patient_id = f"PAT{str(i).zfill(3)}"
        sex = random.choice(["M", "F"])
        age_of_onset = random.randint(1, 80)
        age_at_sampling = random.randint(age_of_onset, 90)  # Ensure logical consistency
        haplogroup = random.choice(haplogroup_choices) + str(random.randint(1000, 9999))  # Append 4 random digits
        
        # Random number of variants per patient
        num_variants = random.randint(min_variants, max_variants)

        for _ in range(num_variants):
            # No need of m3243 heteroplasmy as they are controls
            # m3243_het = round(np.random.uniform(0, 1), 3)
            # m3243_het_normalized = round(np.random.uniform(m3243_het, 1), 3)


            data.append([
                "chrMT",  # Mitochondrial chromosome
                np.random.randint(1, 16659),  # Position of variant
                random.choice(["A", "T", "C", "G"]),  # Reference allele
                random.choice(["A", "T", "C", "G"]),  # Alternate allele
                round(np.random.uniform(0, 1), 3),  # Heteroplasmy rate
                patient_id,  
                sex,
                age_of_onset,
                age_at_sampling,
                random.choice(["Blood", "Urine"]),  # Tissue type
                haplogroup,
                # m3243_het,  # m3243_het value
                # m3243_het_normalized,  # Normalized m3243_het
            ])

    # Create DataFrame
    df = pd.DataFrame(data, columns=[
        "chr", "pos", "ref", "alt", "heteroplasmy_rate", "patient_id", "sex", "age_of_onset", "age_at_sampling",
        "tissue", "haplogroup"
    ])

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Generated {len(df)} variants for {num_patients} patients.")
    print(f"Data saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random patient variant data.")
    
    parser.add_argument("--num_patients", type=int, default=100, help="Number of patients (default: 100)")
    parser.add_argument("--min_variants", type=int, default=30, help="Minimum variants per patient (default: 30)")
    parser.add_argument("--max_variants", type=int, default=50, help="Maximum variants per patient (default: 50)")
    parser.add_argument("--output", type=str, default="patients_random_variants.csv", help="Output CSV file name (default: patients_random_variants.csv)")

    args = parser.parse_args()
    
    generate_patient_data(args.num_patients, args.min_variants, args.max_variants, args.output)