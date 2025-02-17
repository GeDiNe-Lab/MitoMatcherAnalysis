# Import necessary modules
from JSON_verification import load_json  # Custom function to load JSON data
import logging  # Module for logging warnings and errors
import requests  # Module for making HTTP requests to APIs


def extracting_HPO(patient_data):
    """
    Extracts Human Phenotype Ontology (HPO) terms from the provided patient data.

    :param patient_data: Dictionary containing clinical and ontology information of the patient.
    :return: Tuple containing patient ID and a dictionary of HPO terms.
    """

    # Extract the patient ID from the nested "Clinical" dictionary
    patient_id = patient_data.get("Clinical", {}).get("patient_id")

    # Extract the HPO terms from the nested "Ontology" dictionary
    hpo_info = patient_data.get("Ontology", {}).get("hpo", {})

    return patient_id, hpo_info


def asking_HPO_names(patient_id, hpo_info):
    """
    Queries an external HPO API to retrieve HPO term names based on HPO IDs.

    :param patient_id: The unique ID of the patient.
    :param hpo_info: Dictionary containing HPO term IDs for the patient.
    :return: Dictionary in the format { "patient_id": [(hpo_id, hpo_name), ...] }.
    """

    # Base URL of the HPO API
    api_url = "https://clinicaltables.nlm.nih.gov/api/hpo/v3/search"

    # Initialize the final output dictionary
    final_output_hpo = {patient_id: []}

    # Iterate through each HPO term ID in the patient's data
    for hpo in hpo_info.keys():
        # Construct query parameters for the API request
        query_params = {
            "terms": hpo,  # The HPO term ID to search for
            "df": "name",  # Retrieve the name of the HPO term
            "sf": "id",  # Specify search field as ID
            "cf": "id"  # Configure response format to include ID
        }

        # Construct the full API request URL
        query_url = api_url + "?" + requests.compat.urlencode(query_params)

        # Send the API request
        response = requests.get(query_url)

        # Parse the response as JSON
        data = response.json()

        # Check if the API returned results
        if len(data[1]) > 0:
            # Append the HPO ID and its corresponding name to the output dictionary
            final_output_hpo[patient_id].append((hpo, data[3][0][0]))
        else:
            # Log a warning if no name was found for the HPO ID
            logging.warning(f"\nThe HPO '{hpo}' could not be found via the API.\n")
            final_output_hpo[patient_id].append((hpo, ""))  # Store an empty string if no name is found

    return final_output_hpo  # Return the final structured dictionary


def HPO_requesting_process(input_path):
    """
    Main function that processes patient data and retrieves HPO names via API requests.

    :param input_path: Path to the JSON file containing patient data.
    :return: Dictionary containing the structured HPO information.
    """

    # Extract the filename without extension from the input path
    input_filename = input_path.split("/")[-1].replace(".json", "")

    # Load the patient data JSON file
    file_data = load_json(input_path)

    # Extract patient ID and HPO terms
    patient_id, hpo_info = extracting_HPO(file_data)

    # Query the API to retrieve HPO names for the patient's HPO terms
    hpo_output = asking_HPO_names(patient_id, hpo_info)

    # Log that the process was successfully completed
    logging.info(f"The HPO file '{input_filename}' has been processed successfully.")

    return hpo_output  # Return the structured HPO data
