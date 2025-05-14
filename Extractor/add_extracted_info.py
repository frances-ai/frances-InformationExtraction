from extractor import extra_see_references, extract_names
import pandas as pd

if __name__ == '__main__':
    # Load dataframe
    input_filepath = "gaz_entry_1838"
    gaz_df = pd.read_json(input_filepath, orient='index')
    print(f"{len(gaz_df)} entries loaded")
    primary_names = []
    alternative_names = []
    references = []
    total_alternames = 0
    total_references = 0
    print("Extracting names, and references....")
    for index, row in gaz_df.iterrows():
        primary_name, alter_names = extract_names(row['name'])
        primary_names.append(primary_name)
        alternative_names.append(alter_names)
        total_alternames += len(alter_names)
        current_references = extra_see_references(row['text'])
        references.append(current_references)
        total_references += len(current_references)

    print(f"{total_references} references extracted, {total_alternames} alternames extracted")
    gaz_df['name'] = primary_names
    gaz_df['alter_names'] = alternative_names
    gaz_df['reference_terms'] = references

    result_filepath = input_filepath
    print(f"Saving dataframe to {result_filepath}...")
    gaz_df.to_json(result_filepath, orient='index')
    print("Done")



