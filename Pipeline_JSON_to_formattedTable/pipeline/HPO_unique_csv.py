import csv  # Module for handling CSV file operations


def hpo_standard_output_file(global_hpo_info, output_path):
    """
    Generates a standardized CSV output file containing HPO information for each patient.

    :param global_hpo_info: Dictionary structured as { "patient_id": [(hpo_terms, hpo_names), ...] }.
    :param output_path: Path to the output CSV file.
    """

    # Open the output file in write mode
    with open(output_path, "w", newline="") as fh_out:
        writer = csv.writer(fh_out, delimiter=";")  # Use semicolon as delimiter

        # Write the CSV header row
        writer.writerow(["patient_id", "HPO_terms", "HPO_name"])

        # Iterate over each patient in the provided HPO dictionary
        for patient_id, list_hpo in global_hpo_info.items():
            # Iterate over each HPO term-name pair for the patient
            for hpo_terms, hpo_names in list_hpo:
                # Write the patient ID, HPO term, and corresponding name to the CSV file
                writer.writerow([patient_id, hpo_terms, hpo_names])

    return  # Function completes without returning any values
