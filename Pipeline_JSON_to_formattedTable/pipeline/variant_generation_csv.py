import csv  # Module for handling CSV file operations

def generate_variant_csv(variant_dictionnary, output_path):
    """
    Generates a CSV file containing variant data.

    :param variant_dictionnary: Dictionary containing variant data, where each key represents a patient 
                                and values are lists of variant-related information.
    :param output_path: Path where the CSV file will be created.
    :return: None
    """

    # Open the output file in write mode
    with open(output_path, "w", newline='') as fh_out:
        writer = csv.writer(fh_out, delimiter=";")  # Initialize CSV writer with semicolon delimiter

        # Writing the CSV header row
        writer.writerow([
            "chr", "pos", "ref", "alt", "heteroplasmy_rate", "patient_id", "sex", "age_of_onset",
            "age_at_sampling", "tissue", "type", "haplogroup", "m3243_het", "m3243_het_normalized"
        ])

        # Iterate over each patient's data in the dictionary
        for values in variant_dictionnary.values():
            for variant in values:  # Each variant is a tuple/list of values
                writer.writerow(variant)  # Write each variant's details as a row in the CSV file
