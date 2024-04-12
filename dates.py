from datetime import date

def date_formatter(input_str:str):
    """
    This function takes an input string and matches it with three 
    possible known formats and returns the date correctly formatted.
    """
    
    # Variable initialization.
    parsed_date = []
    
    # First, if the input has the wrong length, the function should return "0".
    if not input_str or (len(input_str) != 10 and len(input_str) != 8):
        print("Invalid input length")
        return "2"
    
    # Then check the format in two steps.
        # length check:
    original_format = len(input_str) == 8
    current_format = len(input_str) == 10
    new_format = current_format

    if not original_format and not current_format and not new_format:
        print("Invalid input length")
        return "2"

        # punctuation check:    
    original_format = original_format and input_str.count("/") == 2
    current_format = current_format and input_str.count("/") == 2
    new_format = new_format and input_str.count("-") == 2

    if new_format:
        split_input = input_str.split("-")
    
    elif current_format or original_format:
        split_input = input_str.split("/")
    
    else:
        print("Invalid format")
        return "1"
    

    # Data collection from split_input
    for s in split_input:
        if s.isdigit():
            parsed_date.append(int(s))
        
        else:
            print("Invalid format")
            return "1"

    if len(parsed_date) != 3:
        print("Invalid format")
        return "1"

    # Since date() raises an exception if the data inputted is invalid,
    # the function has a try-and-catch blocks when date() is used. 
    try:
        if original_format:
            formatted_date = date(parsed_date[2] + 1900, parsed_date[2], parsed_date[0])
            p = "Report of previously deprecated format found: {0} changed to {1}"
            print(p.format(input_str,formatted_date))
        
        
        elif current_format:
            formatted_date = date(parsed_date[2], parsed_date[0],parsed_date[1])

        else:
            formatted_date = date(parsed_date[0],parsed_date[1],parsed_date[2])
        
        if formatted_date.weekday() >= 5:
            print("Invalid purchase date")
            return "3"

        return str(formatted_date)
    
    except:
        print("Invalid date")
        return "0"
    
    
         
        

print(date_formatter("09-25-02"))    # Should return 0
print(date_formatter("10/04/"))      # Should return 0
print(date_formatter("not/a/date"))  # Should return 0
print(date_formatter("09/25/2002"))  # Should format to 2002-09-25
print(date_formatter("2002-07-09"))  # Should format to 2002-07-09
print('new data')
print(date_formatter("2002-10-10"))
print(date_formatter("10/05/01"))
print(date_formatter("2001-02-29"))
print(date_formatter("random/s/t"))
print(date_formatter("1"))

print(date_formatter("2024-03-23"))