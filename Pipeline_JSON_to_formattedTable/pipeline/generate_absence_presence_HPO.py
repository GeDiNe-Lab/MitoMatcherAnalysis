import csv

# Function to generate the absence/presence HPO table
def generate_absence_presence_HPO(global_hpo):
    """
    This function generates a table of presence/absence of HPO terms for each patient. 

    :param global_hpo: Dictionary containing patient HPO data, structured as 
                        {"patient_id": [(hpo_terms, hpo_name), ...]}.

    :return: A tuple consisting of:
        - unique_symptome_list: List of all unique HPO names found across all patients.
        - presence_absence_complete: Dictionary containing the presence (1) or absence (0) of each symptom for each patient.
    """

    unique_symptome_list = [] # List to store unique HPO names across all patients
    patient_data = {} # Dictionary to store the HPO names for each patient

    # Structure: {"patient_id" : [(hpo_terms, hpo_name), ]}

    presence_absence_complete = {} # Dictionary to store presence (1) or absence (0) of HPO terms for each patient

    # Loop through all the patients and their associated HPO data
    for patient, hpos in global_hpo.items():

        hpo_names_for_one_patient = [] # List to store HPO names for the current patient

        # Loop through all the HPO combinations for the patient
        for hpo_combination in hpos:

            hpo_name = hpo_combination[1] # Extract the HPO name

            # Add the HPO name to the patient's list
            hpo_names_for_one_patient.append(hpo_name)
            
            # Add the HPO name to the list of unique symptoms if it's not already there and not an empty string
            if hpo_name not in unique_symptome_list and hpo_name != "":
                unique_symptome_list.append(hpo_name)

        # Store the list of HPO names for the current patient
        patient_data[patient] = hpo_names_for_one_patient

    # 2. Create a dictionary of presence (1) or absence (0) of each HPO term for each patient
    for patient, values in patient_data.items():

        # Initialize an empty list for each patient's presence/absence data
        presence_absence_complete[patient] = []

        # For each unique HPO name, check if it is present in the patient's data
        for symptome in unique_symptome_list:
            # Append 1 if the symptom is present, 0 if it is absent
            presence_absence_complete[patient].append([0 if symptome not in values else 1][0])

    return unique_symptome_list, presence_absence_complete


# Function to structure and write the presence/absence data into a CSV file
def structuring_presence_absence_hpo(unique_symptome_list, presence_absence_complete, output_folder):
    """
    This function writes the structured presence/absence data to a CSV file.

    :param unique_symptome_list: List of all unique HPO names found across all patients.
    :param presence_absence_complete: Dictionary containing the presence (1) or absence (0) of each symptom for each patient.
    :param output_folder: Path to the folder where the output CSV file will be saved.
    
    :return: A list representing the structured presence/absence data.
    """

    # Define the output path for the CSV file
    output_path = output_folder + "presence_absence_hpos.csv"
    for_clinical_presence_absence = [] # List to store the final structured data for all patients

    # Open the output CSV file for writing
    with open(output_path, "w") as fh_out:
        # Create a CSV writer object, using ";" as delimiter
        writer = csv.writer(fh_out, delimiter= ";") 


        # Write the header row to the CSV file (patient_id followed by all unique symptoms)
        header = ["patient_id"] +  unique_symptome_list
        for_clinical_presence_absence.append(header)
        writer.writerow(header)

        # Write the patient data rows, each row containing the patient ID and their presence/absence data
        for patient, values in presence_absence_complete.items():
            writer.writerow([patient, *values]) 
            for_clinical_presence_absence.append([patient,*values])
    
    return for_clinical_presence_absence

# Main function to generate and structure the presence/absence HPO data and write it to CSV
def main_generation_absence_presence_hpo(global_hpo_result, output_folder):
    """
    This function orchestrates the generation and structuring of the presence/absence HPO data.

    :param global_hpo_result: Dictionary containing HPO data for each patient.
    :param output_folder: Path to the folder where the output CSV file will be saved.

    :return: A list of the structured presence/absence data for all patients.
    """

    # Generate the unique HPO names and the presence/absence data
    unique_symptome_list, presence_absence_complete = generate_absence_presence_HPO(global_hpo_result)

    # Structure the data and write it to a CSV file
    for_clinical_presence_absence =  structuring_presence_absence_hpo(unique_symptome_list, presence_absence_complete, output_folder)
    
    return for_clinical_presence_absence