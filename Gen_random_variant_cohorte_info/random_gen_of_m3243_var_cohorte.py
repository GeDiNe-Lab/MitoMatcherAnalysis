import pandas as pd
import numpy as np
import random
import argparse
import os


# Haplogroup distribution based on given counts
haplogroups = [
    ("A", 158), ("B", 324), ("C", 148), ("D", 334), ("E", 32), ("F", 104), ("G", 73), ("H", 978), ("HV", 94),
    ("I", 63), ("J", 240), ("K", 198), ("L0", 157), ("L1", 100), ("L2", 132), ("L3", 199), ("L4", 17),
    ("L5", 12), ("L6", 3), ("M", 686), ("N", 248), ("O", 3), ("P", 28), ("Q", 40), ("R", 39), ("S", 8),
    ("T", 230), ("U", 533), ("V", 61), ("W", 60), ("X", 89), ("Y", 14), ("Z", 27)
]

# Create weighted list of haplogroups
haplogroup_choices = [hg for hg, count in haplogroups for _ in range(count)]


def read_csv2(file_path, sep=";", header=0, index_col=0):
    """
    Reads a semicolon-separated CSV file with a specified index column.

    Args:
        file_path (str): The path to the CSV file.
        sep (str): The field separator character (default: ";").
        header (int): The row number to use as column names (default: 0).
        index_col (int): The column number to use as the row index (default: 0).

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the CSV file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.ParserError: If there is an issue parsing the CSV file.
    """
    try:
        df = pd.read_csv(file_path, sep=sep, header=header, index_col=index_col)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Error parsing CSV file: {e}")

def generate_patient_data(num_patients, min_variants, max_variants, output_file, mt_var):
    data = []
    
    for i in range(1, num_patients + 1):
        patient_id = f"PAT{str(i).zfill(3)}"
        sex = random.choice(["M", "F"])
        age_of_onset = random.randint(1, 80)
        age_at_sampling = random.randint(age_of_onset, 90)
        haplogroup = random.choice(haplogroup_choices) + str(random.randint(1000, 9999))
        
        num_variants = random.randint(min_variants, max_variants)
        
        # Tirage sans remise des variants de mt_var
        if num_variants > len(mt_var):
            print(f"Warning: Patient {patient_id} requested {num_variants} variants, but mt_var has only {len(mt_var)} rows. Using all available rows.")
            selected_variants = mt_var.sample(n=len(mt_var), replace=False)
        else:
            selected_variants = mt_var.sample(n=num_variants, replace=False)

        for _, row in selected_variants.iterrows():
            data.append([
                row["Chr"],
                row["Position"],
                row["Ref"],
                row["Alt"],
                round(np.random.uniform(0, 1), 3),  # Heteroplasmy rate
                patient_id,
                sex,
                age_of_onset,
                age_at_sampling,
                random.choice(["Blood", "Urine"]),
                haplogroup,
            ])

    df = pd.DataFrame(data, columns=[
        "chr", "pos", "ref", "alt", "heteroplasmy_rate", "patient_id", "sex", "age_of_onset", "age_at_sampling",
        "tissue", "haplogroup"
    ])

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

    # Relative path to genome_loci_table.csv
    data_folder = "data"
    file_name = "genome_loci_table.csv"
    file_path = os.path.join(data_folder, file_name)
    mt_var = read_csv2(file_path)
    
    generate_patient_data(args.num_patients, args.min_variants, args.max_variants, args.output, mt_var)

    