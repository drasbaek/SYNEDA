from datetime import datetime
import locale

def format_date_variety(date_str):
    formatted_dates = []
    
    # Set the locale to Danish
    locale.setlocale(locale.LC_TIME, "da_DK.utf-8")

    # Convert the input date string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Define a list of different date formats
    date_formats = [
        "%d. %b %y",                   # 20. jul 21
        "%d/%m/%y",                    # 20/07/21
        "%d. %B %Y",                   # 20. juli 2021
        "%B %d %Y",                    # Juli 20 2021
        "%Y-%m-%d",                    # 2021-07-20
        "%d-%m-%Y",                    # 20-07-2021
        "%d %b, %Y",                   # 20 jul, 2021
        "%A, %d. %B %Y",               # Tirsdag, 20. juli 2021
        "%d/%b/%Y",                    # 20/jul/2021
        "%b %dth, %Y",                 # jul 20th, 2021
        "%A, %d-%b-%y",                # Tirsdag, 20-jul-21
        "%A, %d. %B '%y",               # Tirsdag, 20. juli '21
    ]

    # Format the date using each format and append to the list
    for date_format in date_formats:
        formatted_dates.append(date_obj.strftime(date_format))

    return formatted_dates

def main():
    input_date = "2021-07-20"
    formatted_dates = format_date_variety(input_date)
    for date in formatted_dates:
        print(date)

if __name__ == "__main__":
    main()