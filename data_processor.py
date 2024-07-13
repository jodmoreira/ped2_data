import pandas as pd

def extract_personal_details(file_path):
    """
    Extract personal details from the CSV file with specific formatting.

    Parameters:
    file_path (str): Path to the CSV file.

    Returns:
    pd.DataFrame: DataFrame containing formatted personal details.
    """
    # Load the CSV file
    df = pd.read_csv(file_path, encoding='latin1', sep=';')

    # Define columns related to personal details
    personal_details_columns = [
        'NM_CANDIDATO', 'DT_NASCIMENTO', 'NM_MUNICIPIO_NASCIMENTO', 'SG_UF_NASCIMENTO',
        'DS_GENERO', 'DS_COR_RACA', 'DS_ESTADO_CIVIL'
    ]

    # Select columns related to personal details
    personal_details_df = df[personal_details_columns]

    # Convert birth date to datetime format
    personal_details_df['DT_NASCIMENTO'] = pd.to_datetime(personal_details_df['DT_NASCIMENTO'], format='%d/%m/%Y')

    # Capitalize the first letter of names and cities, ignoring prepositions
    def capitalize_name(name):
        exceptions = ['de', 'da', 'do', 'das', 'dos']
        return ' '.join([word.capitalize() if word not in exceptions else word for word in name.split()])

    # Apply capitalization to relevant columns
    personal_details_df['NM_CANDIDATO'] = personal_details_df['NM_CANDIDATO'].apply(capitalize_name)
    personal_details_df['NM_MUNICIPIO_NASCIMENTO'] = personal_details_df['NM_MUNICIPIO_NASCIMENTO'].apply(capitalize_name)
    personal_details_df['DS_GENERO'] = personal_details_df['DS_GENERO'].str.capitalize()
    personal_details_df['DS_COR_RACA'] = personal_details_df['DS_COR_RACA'].str.capitalize()
    personal_details_df['DS_ESTADO_CIVIL'] = personal_details_df['DS_ESTADO_CIVIL'].str.capitalize()

    return personal_details_df

# Example usage
file_path = 'data/consulta_cand_2022_BRASIL.csv'
personal_details_df = extract_personal_details(file_path)

# Display the first few rows of the filtered DataFrame
print(personal_details_df.head())32
