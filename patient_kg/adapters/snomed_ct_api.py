import pandas as pd

description_file = 'template_package/adapters/sct2_Description_Snapshot-en_INT_20231001.txt'
snomed_df = pd.read_csv(description_file, delimiter='\t', header=0)

def get_snomed_name(code):
    name = snomed_df[(snomed_df['conceptId'] == int(code)) & (snomed_df['typeId'] == 900000000000003001)]['term'].values[0]
    return name

# Example usage
code = '126815003'  # Replace with your SNOMED CT code

#name = get_snomed_name(code)
#if name:
#    print("Name for SNOMED CT code {}: {}".format(code, name))
#else:
#    print("No name found for SNOMED CT code {}".format(code))
