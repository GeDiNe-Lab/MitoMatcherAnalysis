import json  # Module for handling JSON files
import logging  # Module for logging errors and warnings

#JSON Validation: Ensures that a JSON file is correctly formatted and contains all necessary information.
#Input: JSON file path  
#Output: Filename (if valid) or False (if validation fails)

def load_json(input_file):
    """
    Load JSON data from a clinical patient JSON file.

    :param input_file: Path to the JSON file.
    :return: JSON data as a dictionary if successful, else False.
    """
    try:
        with open(input_file, "r") as fh:
            return json.load(fh)  # Load and return JSON data
    except FileNotFoundError:
        logging.error(f"Error: File '{input_file}' not found.")
        return False
    except json.JSONDecodeError:
        logging.error(f"Error: File '{input_file}' is not a valid JSON.")
        return False


def verify_clinical_info(clinical_info):
    """
    Verify the clinical information section of the JSON file.

    :param clinical_info: Dictionary containing clinical information.
    :return: True if valid, otherwise False.
    """
    clinical_variables_checked = ["sex"]  # Currently, only "sex" is validated

    for key, value in clinical_info.items():
        if key in clinical_variables_checked:
            # Ensure "sex" is either "M", "F", or empty
            if key == "sex" and value not in {"M", "F", ""}:
                logging.warning(f"Invalid value for {key}: {value}")
                return False

    return True


def verify_sample_info(sample_info):
    """
    Verify the sample information section of the JSON file.

    :param sample_info: Dictionary containing sample details.
    :return: True if valid, otherwise False.
    """
    sample_variables_checked = ["age_at_sampling"]  # Only "age_at_sampling" is validated

    for key, value in sample_info.items():
        if key in sample_variables_checked:
            # Ensure "age_at_sampling" is a valid integer
            try:
                int(value)
            except ValueError:
                logging.warning(f"Invalid value for {key}: {value}")
                return False

    return True


def verify_variants(variants):
    """
    Validate the variant information section.

    :param variants: List of variants extracted from the JSON file.
    :return: True if valid, otherwise False.
    """
    for variant in variants:
        position, reference, alternative, heteroplasmy = variant[1], variant[2], variant[3], variant[4]

        # Validate that position is an integer
        try:
            int(position)
        except ValueError:
            logging.error(f"Invalid position for variant: {variant}")
            return False

        # Validate that reference and alternative sequences contain only valid nucleotides
        for nuc in reference:
            if nuc not in {"A", "T", "C", "G", "N"}:
                logging.error(f"Invalid reference nucleotide for variant: {variant}")
                return False

        for nuc in alternative:
            if nuc not in {"A", "T", "C", "G", "N"}:
                logging.error(f"Invalid alternative nucleotide for variant: {variant}")
                return False

        # Validate heteroplasmy rate
        try:
            float(heteroplasmy)
        except ValueError:
            logging.error(f"Invalid heteroplasmy rate for variant: {variant}")
            return False

        if not heteroplasmy:
            logging.error(f"Missing heteroplasmy rate for variant: {variant}")
            return False

    return True


def verify_presence_of_input_variants(variants, input_variants, het_threshold):
    """
    Validate the presence of specified input variants in the JSON data.

    :param variants: List of variants extracted from the JSON.
    :param input_variants: Comma-separated string of expected variants (e.g., "A3243G,G11778A").
    :param het_threshold: Minimum heteroplasmy rate required.
    :return: True if all specified variants are present and meet the threshold, otherwise False.
    """
    input_variants = input_variants.replace(" ", "").split(",")  # Normalize input variants

    for input_variant in input_variants:
        presence_input_var = False
        presence_m3243 = False

        for variant in variants:
            position, ref, alt, heteroplasmy = variant[1], variant[2], variant[3], variant[4]
            var_lbl = ref + str(int(position)) + alt  # Construct variant label (e.g., "A3243G")

            # Check if the input variant is found in the JSON data
            if input_variant == var_lbl:
                presence_input_var = True

                if not heteroplasmy:
                    logging.error(f"No heteroplasmy rate for variant: {input_variant}")
                    return False

                if float(heteroplasmy) < float(het_threshold):
                    logging.error(f"The variant '{input_variant}' has less than {het_threshold}% heteroplasmy.")
                    return False

            # Special handling for "A3243G" variant
            if var_lbl == "A3243G":
                presence_m3243 = True

        if not presence_input_var:
            logging.error(f"Mutation {input_variant} not found.")
            return False

        if presence_m3243 and len(variants) == 1:
            logging.warning("Only mutation A3243G detected.")

    return True


def verify_HPO(HPO_info):
    """
    Validate the presence of at least one HPO term in the JSON file.

    :param HPO_info: Dictionary containing HPO terms.
    :return: True if at least one HPO term is present, otherwise False.
    """
    return bool(HPO_info.get("hpo", False))


def verification_JSON(input_file, input_variants, het_threshold):
    """
    Perform a comprehensive validation of the JSON file.

    :param input_file: Path to the JSON file.
    :param input_variants: Comma-separated string of expected variants.
    :param het_threshold: Minimum heteroplasmy rate required.
    :return: Filename (if valid) or False (if validation fails).
    """
    logging.info(f"Loading: {input_file}")
    file_data = load_json(input_file)

    if not file_data:
        return False  # JSON loading failed

    # Validate clinical information
    clinical_info = file_data.get("Clinical", {})
    clinical_test = verify_clinical_info(clinical_info)

    # Validate sample information
    sample_info = file_data.get("Sample", {})
    sample_test = verify_sample_info(sample_info)

    # Validate HPO information
    HPO_info = file_data.get("Ontology", {})
    HPO_test = verify_HPO(HPO_info)

    if not HPO_test:
        logging.warning(f"Missing HPO terms in: {input_file}")

    # Validate variant information
    variants = file_data.get("Catalog", [])
    variant_array = [
        [variant["chr"], variant["pos"], variant["ref"], variant["alt"], variant["heteroplasmy_rate"]]
        for variant in variants
    ]
    variant_test = verify_variants(variant_array)

    # Validate input variants presence
    input_variants_test = verify_presence_of_input_variants(variant_array, input_variants, het_threshold)

    # Check overall validation results
    if any(not test for test in [clinical_test, sample_test, variant_test, input_variants_test]):
        return False  # At least one validation failed

    return input_file.split("/")[-1]  # Return the filename if validation is successful
