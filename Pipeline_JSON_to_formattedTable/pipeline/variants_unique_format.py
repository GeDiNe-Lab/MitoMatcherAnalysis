import json
import math
import logging


def getting_variant_info(input_path):
    """
    Load variant information from a JSON file.

    :param input_path: Path to the JSON file.
    :return: Tuple containing clinical_info, onto_info, sample_info, and a list of variant data.
    """
    try:
        with open(input_path, "r") as fh_in:
            data = json.load(fh_in)

        # Extract relevant sections from JSON
        clinical_info = data.get('Clinical', {})
        onto_info = data.get('Ontology', {})
        sample_info = data.get('Sample', {})
        variants = data.get('Catalog', [])

        # Extract variant information
        variant_array = [[v['chr'], v['pos'], v['ref'], v['alt'], v['heteroplasmy_rate']] for v in variants]

        return clinical_info, onto_info, sample_info, variant_array

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error processing file {input_path}: {e}")
        return None, None, None, None


def returning_homogenized_tissue(tissue):
    """
    Standardizes tissue names.

    :param tissue: Raw tissue name.
    :return: Standardized tissue name.
    """
    tissue = tissue.lower()

    tissue_mapping = {
        "blood": ["blood", "sang"],
        "urine": ["urines", "urine"],
        "muscle": ["muscles", "muscle"],
        "heart": ["heart"],
        "buccal": ["buccal"],
        "fibroblast": ["fibroblast"]
    }

    for standard, keywords in tissue_mapping.items():
        if any(keyword in tissue for keyword in keywords):
            return standard

    logging.warning(f"Unknown tissue: '{tissue}'")
    return tissue


def returning_m3243_het(variant_catalog):
    """
    Extract heteroplasmy rate for A3243G mutation.

    :param variant_catalog: List of variant data.
    :return: Heteroplasmy rate of A3243G if found, else None.
    """
    for variant in variant_catalog:
        variant_lbl = f"{variant[2]}{int(variant[1])}{variant[3]}"  # e.g., "A3243G"
        if variant_lbl == "A3243G":
            return float(variant[4])
    return None


def blood_m3243_normalization(m3243_het, age):
    """Normalize blood m3243 heteroplasmy based on age."""
    normalized_value = m3243_het / (0.977 ** (age + 12))
    return min(1, normalized_value)


def urine_m3243_normalization(variant_het, sex):
    """Normalize urine m3243 heteroplasmy based on sex."""
    if variant_het in (0, 1):  # Edge cases: 0% or 100% heteroplasmy
        return variant_het

    logit_urine_het = math.log(variant_het / (1 - variant_het))
    adjustment = 0.608 if sex == "F" else -0.625

    het_normalized = math.exp((logit_urine_het / 0.791) + adjustment)
    return min(1, het_normalized / (1 + het_normalized))


def normalize_heteroplasmy(variant_info, norm_info, normalization_status):
    """
    Normalize heteroplasmy level based on tissue type.

    :param variant_info: List containing variant details.
    :param norm_info: List containing [sex, age_at_sampling, tissue].
    :param normalization_status: String specifying normalization type.
    :return: Normalized heteroplasmy value (0-100).
    """
    sex, age, tissue = norm_info[0], int(norm_info[1]), norm_info[2]
    het = float(variant_info[4]) / 100  # Convert to 0-1 scale

    if normalization_status == "yes":
        if tissue == "blood":
            return round(blood_m3243_normalization(het, age) * 100, 2)
        elif tissue == "urine":
            return round(urine_m3243_normalization(het, sex) * 100, 2)

    elif normalization_status == "blood":
        return round(blood_m3243_normalization(het, age) * 100, 2)

    elif normalization_status == "urine":
        return round(urine_m3243_normalization(het, sex) * 100, 2)

    return round(het * 100, 2)  # Default: return original heteroplasmy in 0-100 range


def structuring_variant_information(clinical_info, sample_info, variant_catalog, het_treshold, input_variants, normalization):
    """
    Structure variant table for analysis.

    :param clinical_info: Patient's clinical information.
    :param sample_info: Sample-related metadata.
    :param variant_catalog: List of variant data.
    :param het_treshold: Minimum heteroplasmy threshold.
    :param input_variants: Variants to filter.
    :param normalization: Normalization mode.
    :return: Formatted list of variants.
    """
    kept_elements = []
    every_variant = []
    norm_info = []  # Data for normalization

    # Extract required information
    variables_wanted_clinical = ["patient_id", "sex", "age_of_onset"]
    variables_wanted_sample = ["age_at_sampling", "tissue", "type", "haplogroup"]

    for key in variables_wanted_clinical:
        value = clinical_info.get(key, "")
        if key == "sex":
            norm_info.append(value)
        kept_elements.append(value)

    for key in variables_wanted_sample:
        value = sample_info.get(key, "")
        if key == "age_at_sampling":
            norm_info.append(value)
        elif key == "tissue":
            value = returning_homogenized_tissue(value)
            norm_info.append(value)
        kept_elements.append(value)

    # Process variants
    m3243_normalized_value = None
    for variant in variant_catalog:
        het = float(variant[4])
        variant_lbl = f"{variant[2]}{int(variant[1])}{variant[3]}"

        if het > int(het_treshold):  # Apply heteroplasmy threshold
            every_variant.append(variant)

            if "A3243G" in input_variants and variant_lbl == "A3243G":
                if normalization != "no" and norm_info[2] in ["blood", "urine"]:
                    m3243_normalized_value = normalize_heteroplasmy(variant, norm_info, normalization)
                else:
                    m3243_normalized_value = float(variant[4])

    # Add supplementary columns if A3243G is researched
    if "A3243G" in input_variants and m3243_normalized_value is not None:
        kept_elements.append(returning_m3243_het(variant_catalog))
        kept_elements.append(m3243_normalized_value)

    # Final variant formatting
    final_variant_format = [variant + kept_elements for variant in every_variant]

    return final_variant_format


def main_concatenation_variants(input_path, het_treshold, input_variants, normalization_status):
    """
    Main function to return patient variant information.

    :param input_path: Path to the JSON file.
    :param het_treshold: Minimum heteroplasmy threshold.
    :param input_variants: Variants of interest.
    :param normalization_status: Specifies if normalization is needed.
    :return: Dictionary containing formatted variant data.
    """
    filename = input_path.replace(".json", "")

    clinical_info, onto_info, sample_info, variant_catalog = getting_variant_info(input_path)

    if None in (clinical_info, onto_info, sample_info, variant_catalog):
        logging.error("Error loading variant information. Check input JSON.")
        return {}

    every_variants_formatted = structuring_variant_information(
        clinical_info, sample_info, variant_catalog, het_treshold, input_variants, normalization_status
    )

    return {filename: every_variants_formatted}
