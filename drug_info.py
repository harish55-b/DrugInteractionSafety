# ==========================================================
# DRUG INFORMATION MODULE (Using OpenFDA API)
# ==========================================================

import requests


def get_drug_info(drug_name: str):
    """
    Fetch drug information from OpenFDA API
    """

    if not drug_name:
        return {"error": "Drug name is required."}

    drug_name = drug_name.strip().lower()

    try:
        url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}&limit=1"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return {
                "drug_name": drug_name,
                "info": "No information found in OpenFDA.",
                "provider": "OpenFDA"
            }

        data = response.json()

        if "results" not in data or not data["results"]:
            return {
                "drug_name": drug_name,
                "info": "No drug label data available.",
                "provider": "OpenFDA"
            }

        result = data["results"][0]

        return {
            "drug_name": drug_name.upper(),
            "brand_name": result.get("openfda", {}).get("brand_name", ["Not available"])[0],
            "manufacturer": result.get("openfda", {}).get("manufacturer_name", ["Not available"])[0],
            "uses": result.get("indications_and_usage", ["Not available"])[0],
            "warnings": result.get("warnings", ["Not available"])[0],
            "side_effects": result.get("adverse_reactions", ["Not available"])[0],
            "provider": "OpenFDA"
        }

    except Exception as e:
        return {
            "drug_name": drug_name,
            "error": f"Failed to fetch data: {str(e)}",
            "provider": "OpenFDA"
        }