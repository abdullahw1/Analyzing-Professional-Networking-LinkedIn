import json
import pandas as pd

def clean_data(input_file, output_file, max_profiles=1000):
    with open(input_file, 'r') as file:
        data = [json.loads(line) for line in file]

    reduced_data = data[:max_profiles]
    cleaned_profiles = []
    first_names_seen = set()  # To avoid duplicate first names

    for profile in reduced_data:
        if 'public_identifier' in profile and profile.get('first_name', '') not in first_names_seen:
            education = [
                {
                    "school": edu.get("school", ""),
                    "field_of_study": edu.get("field_of_study", ""),
                    "start_year": edu.get("starts_at", {}).get("year", "") if edu.get("starts_at") else "",
                    "end_year": edu.get("ends_at", {}).get("year", "") if edu.get("ends_at") else ""
                }
                for edu in profile.get('education', [])
                if edu.get("school") and "Computer Science" in (edu.get("field_of_study") or "") and edu.get("starts_at") and edu.get("ends_at")
            ]

            experiences = [
                {
                    "company": exp.get("company", ""),
                    "starts_at": exp.get("starts_at", {}).get("year", "") if exp.get("starts_at") else "",
                    "ends_at": exp.get("ends_at", {}).get("year", "") if exp.get("ends_at") else ""
                }
                for exp in profile.get('experiences', [])
                if exp.get("company") and exp.get("starts_at") and exp.get("ends_at")
            ]

            if education and experiences:
                new_profile = {
                    "public_identifier": profile["public_identifier"],
                    "first_name": profile.get("first_name", ""),
                    "education": education,
                    "experiences": experiences
                }
                cleaned_profiles.append(new_profile)
                first_names_seen.add(profile.get('first_name', ''))

    df = pd.DataFrame(cleaned_profiles)
    df.to_csv(output_file, index=False)
    print(f"Data cleaned and saved to {output_file}")

input_file_path = 'us_person_profile.txt'
output_file_path = 'cs_simplified_linkedin_profiles.csv'
clean_data(input_file_path, output_file_path)
