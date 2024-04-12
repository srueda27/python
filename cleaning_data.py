import pandas as pd

def main():
    blockbuster_data = {
        'release_date': ['2020-12-15', '2018-07-18', '2019-05-02', '2020-11-17', '2021-08-05'],
        'shoot_date': ['2019-06-30', '2017-05-20', '2018-03-15', '2020-11-20', '2020-09-10'],
        'title': ['Space Adventure', 'The Ocean Quest', 'The Mountain King', 'Time Unraveled', 'Desert Winds'],
        'gross_revenue': ['500000000', '300000000', '-100000', '250000000', '100000000'],
        'budget': ['200000000', '150000000', '50000000', '100000000', '50000000'],
        'ratings': ['PG-13', 'unrated', 'not rated', 'PG', 'R'],
        'company': ['Columbia Pictures', 'Universal Studios', 'Columbia Pictures', 'Warner Bros', 'Columbia Pictures']
    }

    blockbuster_df = pd.DataFrame(blockbuster_data)
    
    netflix_data = {
        'release_date': ['2020-12-15', '2019-10-11', '2018-07-18', '2021-02-14', '2021-08-05'],
        'shoot_date': ['2019-06-30', '2018-08-25', '2017-05-20', '2020-01-07', '2020-09-10'],
        'title': ['Space Adventure', 'Cyber Runner', 'The Ocean Quest', 'Love in the Clouds', 'Desert Winds'],
        'gross_revenue': ['505000000', '150000000', '305000000', '80000000', '102000000'],
        'budget': ['205000000', '75000000', '155000000', '40000000', '52000000'],
        'ratings': ['PG-13', 'not rated', 'unrated', 'PG', 'R'],
        'company': ['Columbia Pictures', 'Netflix Original', 'Universal Studios', 'Columbia Pictures', 'Columbia Pictures']
    }
    netflix_df = pd.DataFrame(netflix_data)

    # Save the DataFrame to a CSV file
    blockbuster_csv_file_path = './blockbuster_movies.csv'
    blockbuster_df.to_csv(blockbuster_csv_file_path, index=False)
    netflix_csv_file_path = './netflix_movies.csv'
    netflix_df.to_csv(netflix_csv_file_path, index=False)
    
    print(cleaning_data('blockbuster_movis.csv', 'netflix_movies.csv'))

def columns_exist(blockbuster_movies, netflix_movies, columns):
    try:
        # Get the columns from the dataframes
        blockbuster_columns = set(blockbuster_movies.columns)
        netflix_columns = set(netflix_movies.columns)
        
        # Filtered the columns that are the same in both dataframes
        intersection_columns = (blockbuster_columns & netflix_columns)
        
        # Get the missing columns 
        missing_columns = set(columns) - intersection_columns

        if missing_columns:
            raise ValueError(f"The missing columns in one or both datasets are: {', '.join(missing_columns)}. Please make sure all columns exist in both datasets before Proceeding with data cleaning.")
        else:
            return True

    except ValueError as e:
        print(e)


# Function to clean and merge the datasets
def cleaning_data(blockbuster_csv, netflix_csv):
    # File Error handling
    try:
        blockbuster_df = pd.read_csv(blockbuster_csv)
        netflix_df = pd.read_csv(netflix_csv)
    except FileNotFoundError:
        raise FileNotFoundError("Cannot open one or both of the files.")
    except Exception as e:
        raise Exception(f"Error whilst trying to read the files: {e}")

    # Define the columns needed and verify both dataframes have them.
    columns = ["release_date", "shoot_date", "title", "gross_revenue", "budget", "ratings", "company"]
    if columns_exist(blockbuster_df, netflix_df, columns):
        print("All columns exist in both datasets. Proceeding with data cleaning.")
    else:
        return
        
    # Perform the inner join by title with the according suffixes
    merged_df = pd.merge(blockbuster_df, netflix_df, on="title", how="inner", suffixes=('_blockbuster', '_netflix'))

    # Keep the Netflix columns and remove the suffix
    merged_df = merged_df[["release_date_netflix", "shoot_date_netflix", "title", "gross_revenue_netflix", "budget_netflix", "ratings_netflix", "company_netflix"]]
    merged_df.rename(columns={'release_date_netflix': 'release_date', "shoot_date_netflix": "shoot_date", "gross_revenue_netflix" : "gross_revenue", 'budget_netflix': 'budget', "ratings_netflix" : "ratings", "company_netflix" : "company"}, inplace=True)
    
    # Remove duplicates
    merged_df.drop_duplicates(inplace=True)
    
    # Remove rows with missing values 
    merged_df.dropna(subset=["title"], inplace=True)
    
    merged_df[['gross_revenue', 'budget']] = merged_df[['gross_revenue', 'budget']].apply(pd.to_numeric)

    # Standardize 'ratings' without case sensitivity
    merged_df["ratings"] = merged_df["ratings"].replace(to_replace=r'(?i)^not rated$', value='unrated', regex=True)
    
    # Filtered rows where the 'gross_revenue' and 'budget' columns are not null and greater than 0
    merged_df = merged_df[pd.notnull(merged_df['gross_revenue']) & pd.notnull(merged_df['budget'])]
    merged_df = merged_df[(merged_df["gross_revenue"] >= 0) & (merged_df["budget"] >= 0)]

    # Filtered rows where 'company' is "Columbia Pictures"
    merged_df = merged_df[merged_df["company"] == "Columbia Pictures"]
    
    # Convert 'release_date' and 'shoot_date' into date data types
    merged_df["release_date"] = pd.to_datetime(merged_df["release_date"], errors="coerce")
    merged_df["shoot_date"] = pd.to_datetime(merged_df["shoot_date"], errors="coerce")

    # Remove records where the release date is greater than the shoot date
    merged_df = merged_df[merged_df["shoot_date"] <= merged_df["release_date"]]

    return merged_df


main()

