import json
from datetime import datetime


def filter_passengers(passenger_data, target_date_str, target_city):
    """
    Filters a list of passengers based on the following criteria:
    1. The passenger's registration city must be {target_city}.
    2. The passenger's boarding date must start with {target_date}.
    3. The passenger must be older than 35 years as of {target_date}.
    4. The passenger must be 40 years or older as of today.
    5. The passenger's birth month must be January, July, or September.
    Parameters:
    - passenger_data: A list of passengers.
      Each passenger includes 'date_of_birth', 'registration_city', 'boarding_date', and 'id'.
    - target_date: string with format 'YYYY-MM-DD'
    - target_city: string with the registration city

    Returns:
    - list: A list of filtered passenger information. 
      Each passenger includes the passenger's 'id', 
      'name', 
      age as of today ('current_date'),
      age as of the target date ('age_target_date'), 
      and birth month ('birth_month').
    """
    filtered_passengers = [] 
    today = datetime.today() 
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")

    # Filter the list of passengers who got on the bus on the target date and the target city 
    for passenger in passenger_data:    
      # Parse the date string to a datetime object
      born_date = datetime.strptime(passenger["date_of_birth"], "%Y-%m-%d")

      # Calculate the passenger's current age and the age by the target date 
      age = today.year - born_date.year - ((today.month, today.day) < (born_date.month, born_date.day))
      age_target_date = target_date.year - born_date.year - ((target_date.month, target_date.day) < (born_date.month, born_date.day))
    
      # Filter passengers 40 years old or older today, older than 35 years by the target date, 
      # got on the bus on the target date and the target city, and was born in January, July, or September
      if (age >= 40 and
          age_target_date > 35 and 
          passenger["registration_city"] == target_city and 
          passenger["boarding_date"].startswith(target_date_str) and 
          born_date.month in [1, 7, 9]):
          
          filtered_passengers.append({
              "id": passenger["id"], 
              "name": passenger["name"], 
              "current_age": age, 
              "age_target_date": age_target_date, 
              "birth_month": born_date.strftime("%B"),
              "refund": round(passenger["fare_paid"] * 0.40, 2) # Calculate the 40% to be reimbursed
          }) 
    return filtered_passengers


# Usage example
passenger_data_json = '''[
   {
      "id": 1,
      "name": "John Smith",
      "boarding_date": "2023-10-15T00:00:00Z",
      "fare_paid": 2.50,
      "registration_city": "New York City",
      "date_of_birth": "1988-05-10"
   },
   {
      "id": 2,
      "name": "Mary Brown",
      "boarding_date": "2023-11-01T00:00:00Z",
      "fare_paid": 2.75,
      "registration_city": "Los Angeles",
      "date_of_birth": "1980-08-20"
   },
   {
      "id": 3,
      "name": "Peter Jones",
      "boarding_date": "2023-11-01T00:00:00Z",
      "fare_paid": 3.00,
      "registration_city": "Los Angeles",
      "date_of_birth": "1985-09-02"
   },
   {
      "id": 4,
      "name": "Anna Williams",
      "boarding_date": "2024-01-05T00:00:00Z",
      "fare_paid": 1.50,
      "registration_city": "Houston",
      "date_of_birth": "2004-11-28"
   },
   {
      "id": 5,
      "name": "David Miller",
      "boarding_date": "2024-02-02T00:00:00Z",
      "fare_paid": 2.25,
      "registration_city": "Phoenix",
      "date_of_birth": "1969-09-03"
   },
   {
      "id": 6,
      "name": "Anna South",
      "boarding_date": "2023-11-01T00:00:00Z",
      "fare_paid": 3.50,
      "registration_city": "Los Angeles",
      "date_of_birth": "1983-01-01"
   }
]'''

passenger_data = json.loads(passenger_data_json)
target_date = "2023-11-01"
target_city = "Los Angeles"
filtered_passengers = filter_passengers(passenger_data, target_date, target_city)
for passenger in filtered_passengers:
    print(passenger)