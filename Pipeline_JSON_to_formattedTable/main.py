#!/usr/bin/env python3

"""
Main script for processing patient JSON files.

The goal is to create a structured dataset for analysis from multiple JSON files.
This pipeline:
- Verifies and validates JSON files.
- Extracts and organizes HPO (Human Phenotype Ontology) data.
- Processes variant data, applying heteroplasmy thresholds and optional normalization.
- Generates clinical summary tables and structured CSV files.

Modules used:
- JSON_verification: Checks and validates JSON structure.
- HPO_terms_API_request: Queries HPO terms via an API.
- HPO_terms_infile_research: Extracts HPO terms from local files.
- HPO_unique_csv: Standardizes HPO data output.
- Pipeline_JSON_to_formattedTable.pipeline.variants_unique_format: Processes variant data.
- Pipeline_JSON_to_formattedTable.pipeline.variant_generation_csv: Generates variant CSV outputs.
- generate_absence_presence_HPO: Creates presence/absence tables for HPO terms.
- generation_clinical_table: Generates the final clinical dataset.
"""

import argparse
import os
import logging
import threading
# import re
import sys


# Adding the 'pipeline' directory to the system path
pipeline_path = os.path.join(os.path.dirname(__file__), 'pipeline')
sys.path.append(pipeline_path)

# Print to verify the path
print(f"Appending to sys.path: {pipeline_path}")


import JSON_verification

# Importing necessary functions from other modules
from HPO_terms_API_request import HPO_requesting_process
from HPO_terms_infile_research import main_research_HPO
from HPO_unique_csv import hpo_standard_output_file
from variants_unique_format import main_concatenation_variants
from variant_generation_csv import generate_variant_csv
from generate_absence_presence_HPO import main_generation_absence_presence_hpo
from generation_clinical_table import generation_clinical_table




# ------------------------------
# LOGGING SETUP
# ------------------------------

def setup_logger(log_file):
    """
    Configures logging to output messages to a log file.

    :param log_file: Path to the log file where processing details will be stored.
    """
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


# Global dictionaries for storing extracted HPO and variant data
global_hpo_result = {}  # Stores HPO results per patient
global_variant_result = {}  # Stores variant results per patient


def update_global_hpo(result):
    """
    Updates the global HPO result dictionary with new patient data.

    :param result: Dictionary containing extracted HPO terms for a patient.
    """
    global global_hpo_result
    global_hpo_result.update(result)


def update_global_variant(result):
    """
    Updates the global variant result dictionary with new patient data.

    :param result: Dictionary containing extracted variant information for a patient.
    """
    global global_variant_result
    global_variant_result.update(result)


# ------------------------------
# MAIN PROCESSING FUNCTION
# ------------------------------

def main(input_folder, output_folder, hpo_path, input_variants, het_treshold, normalization_status=None):
    """
    Main function to process JSON files, extract variant and HPO information, and generate output files.

    Steps:
    1. Verify JSON file correctness.
    2. Extract HPO terms from API/local file.
    3. Generate presence/absence tables for HPO terms.
    4. Extract variant data and apply filtering.
    5. Generate final structured clinical dataset.

    :param input_folder: Path to the input folder containing JSON files.
    :param output_folder: Path to the output folder where results will be stored.
    :param hpo_path: Path to the HPO reference file.
    :param input_variants: List of variants used for filtering, formatted as "A3243G,A73G".
    :param het_treshold: Minimum heteroplasmy threshold for variant filtering.
    :param normalization_status: Defines normalization behavior ("yes", "no", "blood", "urine").
    """

    # ------------------------------
    # STEP 0: FOLDER & LOG SETUP
    # ------------------------------

    # Ensure output folder exists, create if missing
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
        print(f"The output folder '{output_folder}' has been created.")

    # Initialize logging
    log_file = os.path.join(output_folder, "process.log")
    setup_logger(log_file)
    logger = logging.getLogger(__name__)
    logger.info("Starting pipeline\n################################\n")

    # Validate input folder existence
    if not os.path.isdir(input_folder):
        logger.error(f"Input folder '{input_folder}' does not exist.")
        return

    # ------------------------------
    # STEP 1: VERIFY JSON FILES
    # ------------------------------
    
    logger.info("STEP 1: Verifying JSON files.\n####################")

    correct_JSON_files = []  # Stores valid JSON files
    total_JSON_files = []  # Tracks all tested JSON files

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_path = os.path.join(input_folder, filename)
            total_JSON_files.append(filename)

            try:
                # Perform JSON verification and filtering
                tested_file = JSON_verification.verification_JSON(input_path, input_variants, het_treshold)

                if tested_file:
                    correct_JSON_files.append(tested_file)
                    logger.info(f"File '{filename}' passed verification.\n")
                else:
                    logger.error(f"File '{filename}' failed verification.\n")

            except Exception as e:
                logger.error(f"Error verifying file '{filename}': {e}\n")

    logger.info(f"Total correct JSON files: {len(correct_JSON_files)}")
    logger.info(f"Total JSON files tested: {len(total_JSON_files)}\n")

    # ------------------------------
    # STEP 2: PROCESS HPO DATA
    # ------------------------------

    logger.info("STEP 2: Extracting HPO terms.\n####################")

    # Extract HPO terms for each patient
    for filename in correct_JSON_files:
        if filename.endswith(".json"):
            input_path = os.path.join(input_folder, filename)
            update_global_hpo(main_research_HPO(input_path, hpo_path))

    # Generate presence/absence HPO table
    for_clinical_presence_absence = main_generation_absence_presence_hpo(global_hpo_result, output_folder)

    # Save full HPO data to CSV
    output_path_concatenate_hpo = os.path.join(output_folder, "concatenate_HPO.csv")
    hpo_standard_output_file(global_hpo_result, output_path_concatenate_hpo)
    logger.info(f"The HPO concatenate file '{output_path_concatenate_hpo}' has been created.")

    # ------------------------------
    # STEP 3: PROCESS VARIANT DATA
    # ------------------------------

    logger.info("STEP 3: Extracting variant data.\n####################")

    # Extract variant data from JSON files
    threads = []
    for filename in correct_JSON_files:
        if filename.endswith(".json"):
            input_path = os.path.join(input_folder, filename)
            thread = threading.Thread(target=lambda: update_global_variant(
                main_concatenation_variants(input_path, het_treshold, input_variants, normalization_status)))
            threads.append(thread)
            thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Generate structured variant CSV file
    output_path_concatenate_variants = os.path.join(output_folder, "concatenate_variants.csv")
    generate_variant_csv(global_variant_result, output_path_concatenate_variants)
    logger.info(f"The concatenate variant file '{output_path_concatenate_variants}' has been created.")

    # ------------------------------
    # STEP 4: GENERATE CLINICAL TABLE
    # ------------------------------

    logger.info("STEP 4: Creating clinical dataset.\n####################")
    generation_clinical_table(global_variant_result, output_folder)


# ------------------------------
# ENTRY POINT (ARGUMENT PARSING)
# ------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pipeline to transform JSON files into structured datasets for analysis.')
    
    # Define command-line arguments
    parser.add_argument('input_folder', type=str)
    parser.add_argument('output_folder', type=str)
    parser.add_argument('hpo_path', type=str)
    parser.add_argument('invariants', type=str)
    parser.add_argument('het_treshold', type=float)
    parser.add_argument('norm_status', type=str)

    args = parser.parse_args()
    main(args.input_folder, args.output_folder, args.hpo_path, args.invariants, args.het_treshold, args.norm_status)