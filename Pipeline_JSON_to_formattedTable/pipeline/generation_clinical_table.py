def filtering_global_variant(global_variant_result):
    """
    Filters the global variant result to keep only unique patient information, removing specific variant details.

    This function processes the variant data, discarding specific variant information and retaining patient-specific
    details such as tissue, age, and other patient characteristics.

    :param global_variant_result: Dictionary containing variant data for each file (patient).
    :return: A dictionary where the key is the file name (patient), and the value is the patient-specific information.
    """
    
    # Initialize an empty dictionary to store the unique patient information
    unique_patient_information = {}

    # Loop through each file (patient) and their corresponding variant data
    for file_name, variants in global_variant_result.items():
        for variant in variants:
            # Save only the patient-specific information (index 5 and beyond) 
            # while discarding the variant-specific details (the first 5 elements)
            unique_patient_information[file_name] = variant[5:]

    # Return the dictionary containing unique patient information
    return unique_patient_information


def verification_list_info(unique_patient_information, filenames):
    """
    Verifies if the data lists from multiple files (patients) are identical. If they differ, combines values at 
    the point of difference into a single list.

    :param unique_patient_information: Dictionary with unique patient data (file_name -> patient_info).
    :param filenames: List of filenames (patients) to check and combine data from.
    :return: A list containing combined data, where differing values are joined by commas.
    """

    # Initialize the variable to store the normal (expected) size of the list
    normal_size = None

    # Check if all lists are of the same size
    for key, values in unique_patient_information.items():

        if key in filenames:  # Only consider files that are in the filenames list
            if normal_size is None:
                normal_size = len(values) # Set the normal size to the first valid file's size
            elif normal_size != len(values):
                raise ValueError("All lists must have the same size.") # Raise error if sizes differ

    # Initialize an empty list to store the combined values
    combined_list = []

    # Iterate through each index position in the list
    for i in range(normal_size):  # Depending on the number of samples for one individual, then
        # Gather elements for the same index from all filenames
        elements = [valeur[i] for key, valeur in unique_patient_information.items() if key in filenames]

        # If all elements at the index are the same, append the single value to the combined list
        if all(elements[0] == elem for elem in elements):
            combined_list.append(elements[0])
        else:
            # Otherwise, join different values as a comma-separated string
            combined_list.append(",".join(map(str, elements)))

    return combined_list

def getting_one_row_by_patient(unique_patient_information):
    """
    Aggregates information for patients with multiple samples into a single row, 
    concatenating details side-by-side if necessary. 

    This function ensures that each patient appears as a single row in the final table,
    even if they have multiple samples.

    :param unique_patient_information: Dictionary of unique patient data (file_name -> patient_info).
    :return: A dictionary where the key is the patient ID and the value is a list of aggregated patient data.
    """
    # Retrieve patients with identical ids, add others directly
    # For these patients with identical ids
    # Check if the info differs step by step and then add them to a new dict

    one_patient_by_row = {} # final dictionary
    multiple_sample = set() # For multiple sample for one patient
    patient_list = set() # Full patient_id list to set difference

    # Filtering for multiple sample with same patient_id which are added to double_sample.
    for patient_info in unique_patient_information.values():
        patient_id = patient_info[0]

        if patient_id not in patient_list:
            patient_list.add(patient_id)
        else:
            multiple_sample.add(patient_id)

    # If the list contains at least one name, then go through each patient whose patient_id is present multiple times.
    if multiple_sample:
        for patient in multiple_sample:
             # Creating for each patient, the list of files that belong to it.
            filename_of_one_patient = [filename for filename, info in unique_patient_information.items() if patient in info]

            # Go through the information of each file and check the information, if they differ separate them by ",".
            combined_list = verification_list_info(unique_patient_information, filename_of_one_patient)

            # Adding info to the final dictionary.
            one_patient_by_row[patient] = combined_list

    # Adding unique patient
    one_sample_list = patient_list.difference(multiple_sample)

    for patient_id in one_sample_list:
        # retrieve the list:
        for filename, variant_info in unique_patient_information.items():
            if patient_id == variant_info[0]:
                one_patient_by_row[patient_id] = unique_patient_information[filename]

    return one_patient_by_row

def generation_clinical_table_csv(one_patient_by_row_dict, output_folder):
    """
    Generates and writes a clinical table CSV file from the processed patient data.

    This function creates a CSV file where each row represents a patient and their associated 
    clinical data (e.g., sex, age, m3243 heteroplasmy, etc.). The file is saved in the specified output folder.

    :param one_patient_by_row_dict: Dictionary where the key is the patient ID and the value is a list of aggregated data.
    :param output_folder: The folder path where the CSV file will be saved.
    """

    # Define the output path for the CSV file
    output_path = output_folder + "resume_clinical_table.csv"

    # Open the output file for writing
    with open(output_path, "w") as fh_out:

        # Writing the header
        header = ["patient_id", "sex", "age_of_onset", "age_at_sampling", "tissue", "type", "haplogroup", "m3243_het", "m3243_het_normalized"]

        # Initialize the final file lines with the header
        final_file_lines = ["\t".join(header)]

        # Loop through the patient data and write each row to the CSV file
        for variant_info in one_patient_by_row_dict.values():
            # Convert all values to strings for CSV formatting
            variant_info_str = [str(value) for value in variant_info]

            # Append the formatted row to the final lines
            final_file_lines.append("\t".join(variant_info_str))

        # Combine all rows into a single string with newline separators
        final_file = "\n".join(final_file_lines)

        # Write the final file content to the CSV file
        fh_out.write(final_file)

    return

def generation_clinical_table(global_variant_result, output_folder):
    """
    Coordinates the creation of a clinical table by calling necessary functions to process data and 
    generate the corresponding CSV file.

    This function orchestrates the entire process: filtering the global variant data, aggregating patient 
    information, and generating the final clinical table in CSV format.

    :param global_variant_result: Dictionary containing global variant data for each patient.
    :param output_folder: Folder path where the output CSV file will be saved.
    """

    # Filter global variant result to keep only unique patient information
    unique_patient_information = filtering_global_variant(global_variant_result)

    # Aggregate data into one row per patient
    one_patient_by_row  = getting_one_row_by_patient(unique_patient_information)

    # Generate and save the clinical table as a CSV
    generation_clinical_table_csv(one_patient_by_row, output_folder)
