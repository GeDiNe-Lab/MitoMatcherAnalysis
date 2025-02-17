# Importing necessary modules
from JSON_verification import load_json  # Custom function to load JSON data
import json  # Built-in module for handling JSON files
import logging  # Module for logging warnings and errors


def extracting_HPO(patient_data):
    """
    Extracts Human Phenotype Ontology (HPO) terms from patient data.

    :param patient_data: Dictionary containing clinical and ontology information.
    :return: Tuple containing patient ID and a dictionary of HPO terms.
    """
    # Extract patient ID from the nested "Clinical" dictionary
    patient_id = patient_data.get("Clinical", {}).get("patient_id")

    # Extract HPO terms from the nested "Ontology" dictionary
    hpo_info = patient_data.get("Ontology", {}).get("hpo", {})

    return patient_id, hpo_info


def intern_HPO_research(hpo_file_path, hpo_info, patient_id):
    """
    Searches for HPO term names corresponding to their IDs in a provided HPO JSON file.

    :param hpo_file_path: Path to the JSON file containing HPO terms.
    :param hpo_info: List of HPO term IDs associated with a patient.
    :param patient_id: The unique ID of the patient.
    :return: Dictionary mapping each HPO ID to its corresponding name.
    """
    
    # Read and parse the JSON file containing HPO term information
    with open(hpo_file_path, "r") as file:
        data = json.load(file)

    # Dictionary to map HPO IDs to their respective names
    hpo_to_name = {}

    # Iterate through all ontology nodes to extract HPO IDs and names
    for node in data["graphs"][0]["nodes"]:
        hpo_id = node["id"].split("/")[-1]  # Extract HPO ID from the URL-like identifier
        hpo_name = node.get("lbl", "Nom non disponible")  # Retrieve the label (HPO name) or a default message if missing
        hpo_to_name[hpo_id] = hpo_name  # Store in dictionary
    
    # Initialize dictionary to store patient-specific HPO terms and their names
    dict_patient_hpo = {}

    # Search for each patient’s HPO ID in the extracted HPO dictionary
    for hpo in hpo_info:
        if hpo not in hpo_to_name:  # If HPO ID is not found in the reference dictionary
            logging.warning(f"\nThe HPO '{hpo}' was not found in hp.json for the patient {patient_id}\n")
            dict_patient_hpo[hpo] = ""  # Assign an empty string when no name is available
        else:
            dict_patient_hpo[hpo] = hpo_to_name[hpo]  # Assign the corresponding HPO name
    
    return dict_patient_hpo  # Return the mapping of patient HPO terms to their names


def main_research_HPO(input_path, hpo_file_path):
    """
    Main function to retrieve HPO information for a given patient and structure it in a dictionary.

    :param input_path: Path to the patient's JSON file.
    :param hpo_file_path: Path to the HPO reference JSON file.
    :return: Dictionary in the format { "patient_id": [(hpo_id, hpo_name), ...] }.
    """

    # Load the JSON file containing patient data
    file_data = load_json(input_path)

    # Extract patient ID and HPO terms from the loaded data
    patient_id, hpo_info = extracting_HPO(file_data)

    # Convert HPO IDs to a list, replacing colons with underscores for uniformity
    hpo_list = [hpo.replace(":", "_") for hpo in hpo_info.keys()]

    # Perform HPO term lookup in the ontology file
    dict_patient_hpo = intern_HPO_research(hpo_file_path, hpo_list, patient_id)

    # Construct the final output format: { "patient_id": [(hpo_id, hpo_name), ...] }
    final_output_hpo = {patient_id: [(hpo_id, hpo_name) for hpo_id, hpo_name in dict_patient_hpo.items()]}

    return final_output_hpo  # Return structured patient HPO information


# Entry point for the script execution
if __name__ == "__main__":
    # Define the file path for the HPO ontology JSON
    hpo_file_path = "raw_data/HPOs/hp.json"

    # Run the main function with a sample patient JSON file and print results
    print(main_research_HPO("raw_data/180114196_129-S5-187-RUN129_MITO.json", hpo_file_path))
