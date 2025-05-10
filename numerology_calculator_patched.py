# D:\numerology_streamlit_app\numerology_calculator.py
import math
import datetime
import re # Used for cleaning the name string

# --- Configuration ---
# Based on the provided table
letter_values = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

# Vowels (Standard definition, Y is not treated as a vowel based on user feedback)
VOWELS = 'AEIOU'


def is_y_vowel(name, index):
    """
    Determines if 'Y' is acting as a vowel at a specific index in the name.
    """
    # THIS IS YOUR ORIGINAL is_y_vowel FUNCTION
    if name[index] != 'Y':
        return False

    vowels = 'AEIOU' # Using local variable as in your original
    prev_char = name[index - 1] if index > 0 else ''
    next_char = name[index + 1] if index < len(name) - 1 else ''

    # Rule 1: Surrounded by consonants or at edge and not near vowels
    if (prev_char not in vowels and next_char not in vowels):
        return True

    # Rule 2: At end of word and makes a vowel sound (simplified)
    if index == len(name) - 1 and prev_char not in vowels:
        return True

    return False

# --- Helper Functions ---

def is_master_number(num):
    """Checks if a number is a Master Number (11, 22, ..., 99)."""
    return num in [11, 22, 33, 44, 55, 66, 77, 88, 99]

def sum_digits(n):
    """Calculates the sum of the digits of a positive integer."""
    s = 0
    # Handle potential floating point inputs by converting to int first if necessary
    try:
        n = int(n)
    except (ValueError, TypeError):
        return 0 # Or raise an error if preferred

    while n > 0:
        s += n % 10
        n //= 10
    return s

def reduce_number(num):
    """
    Reduces a number according to the specific multi-step numerology rules
    provided in the Apps Script logic.

    Returns a dictionary containing calculation steps and the final string.
    """
    # THIS IS YOUR ORIGINAL reduce_number FUNCTION LOGIC
    if not isinstance(num, int) or num < 0:
        # Adding a check for non-integer inputs which might happen if sum is zero initially
        if isinstance(num, (float, int)) and num == 0:
             num = 0 # Allow zero
        else:
            return {'initial': num, 'final': 'Invalid Input', 'log': 'Input must be a non-negative integer'}


    log = [f"Reducing: {num}"]
    initial_num = num
    r1, r2, r3 = None, None, None # Initialize reduction variables

    # Rule 1: Check if initial number is <= 19 or a Master Number
    if num <= 19 or is_master_number(num):
        final_str = str(num)
        log.append(f" -> Rule 1: Initial <= 19 or Master. Final: {final_str}")
        return {'initial': initial_num, 'r1': r1, 'r2': r2, 'r3': r3, 'final': final_str, 'log': "\n".join(log)}

    # Rule 2: First Reduction
    r1 = sum_digits(num)
    log.append(f" -> R1 = sum_digits({num}) = {r1}")

    # Rule 3: Check if R1 is a Master Number
    if is_master_number(r1):
        final_str = str(r1)
        log.append(f" -> Rule 3: R1 is Master. Final: {final_str}")
        return {'initial': initial_num, 'r1': r1, 'r2': r2, 'r3': r3, 'final': final_str, 'log': "\n".join(log)}

    # Rule 4: Check if R1 <= 19 AND initial number was 2 digits (num < 100)
    if r1 <= 19 and num < 100:
        final_str = f"{num}/{r1}" # Format from Apps Script comments/examples
        log.append(f" -> Rule 4: R1 <= 19 and num < 100. Final: {final_str}")
        return {'initial': initial_num, 'r1': r1, 'r2': r2, 'r3': r3, 'final': final_str, 'log': "\n".join(log)}

    # Rule 5: Check if R1 <= 19 AND initial number was 3+ digits (num >= 100)
    if r1 <= 19 and num >= 100:
        final_str = str(r1) # Format from Apps Script comments/examples
        log.append(f" -> Rule 5: R1 <= 19 and num >= 100. Final: {final_str}")
        return {'initial': initial_num, 'r1': r1, 'r2': r2, 'r3': r3, 'final': final_str, 'log': "\n".join(log)}

    # Rule 6: Second Reduction (only happens if r1 > 19)
    r2 = sum_digits(r1)
    log.append(f" -> R2 = sum_digits({r1}) = {r2}")

    # Rule 7: Check if R2 is a Master Number
    if is_master_number(r2):
        final_str = str(r2)
        log.append(f" -> Rule 7: R2 is Master. Final: {final_str}")
        return {'initial': initial_num, 'r1': r1, 'r2': r2, 'r3': r3, 'final': final_str, 'log': "\n".join(log)}

    # Rule 8: Complex rules for 3+ digit initial numbers where R1 > 19
    if num >= 100 and r1 > 19:
        # Rule 8a: If R2 <= 19
        if r2 <= 19:
            final_str = f"{r1}/{r2}" # Format from Apps Script comments/examples
            log.append(f" -> Rule 8a: num >= 100, R1 > 19, R2 <= 19. Final: {final_str}")
            return {'initial': initial_num, 'r1': r1, 'r2': r2, 'r3': r3, 'final': final_str, 'log': "\n".join(log)}
        # Rule 8b: If R2 > 19
        else:
            r3 = sum_digits(r2)
            log.append(f" -> R3 = sum_digits({r2}) = {r3}")
            # Assuming the final format uses r1 and r3 based on App Script: firstReduction + "/" + thirdReduction
            final_str = f"{r1}/{r3}"
            log.append(f" -> Rule 8b: num >= 100, R1 > 19, R2 > 19. Final: {final_str}")
            return {'initial': initial_num, 'r1': r1, 'r2': r2, 'r3': r3, 'final': final_str, 'log': "\n".join(log)}

    # Rule 9: Default case (likely num < 100 and R1 > 19)
    # The Apps script uses 'num + "/" + secondReduction' which is 'initial_num / r2'
    final_str = f"{initial_num}/{r2}"
    log.append(f" -> Rule 9: Default (num < 100, R1 > 19). Final: {final_str}")
    return {'initial': initial_num, 'r1': r1, 'r2': r2, 'r3': r3, 'final': final_str, 'log': "\n".join(log)}


# --- Calculation Functions ---

def calculate_expression(name):
    """Calculates the Expression Number from the full name."""
    clean_name = re.sub(r'[^A-Z]', '', name.upper()) # Keep only letters
    total = 0
    log = [f"Calculating Expression for: {name} -> {clean_name}"]
    for i, letter in enumerate(clean_name): # ensure 'i' is used if needed by is_y_vowel, though it's not in your original
        value = letter_values.get(letter, 0)
        total += value
        log.append(f"  '{letter}' = {value}")
    log.append(f"  Total Sum = {total}")

    reduction_result = reduce_number(total)
    log.append(reduction_result['log']) # Append reduction log
    return {'number': reduction_result['final'], 'sum': total, 'log': "\n".join(log)}

def calculate_soul_urge(name):
    """Calculates the Soul Urge Number from vowels in the full name."""
    clean_name = re.sub(r'[^A-Z]', '', name.upper())
    total = 0
    log = [f"Calculating Soul Urge for: {name} -> {clean_name}"]
    for i, letter in enumerate(clean_name): # 'i' is the index
        if letter in VOWELS or (letter == 'Y' and is_y_vowel(clean_name, i)):
            value = letter_values.get(letter, 0)
            total += value
            log.append(f"  '{letter}' (Vowel) = {value}")
        else:
             log.append(f"  '{letter}' (Consonant) skipped")
    log.append(f"  Total Sum = {total}")

    reduction_result = reduce_number(total)
    log.append(reduction_result['log'])
    return {'number': reduction_result['final'], 'sum': total, 'log': "\n".join(log)}

def calculate_personality(name):
    """Calculates the Personality Number from consonants in the full name."""
    clean_name = re.sub(r'[^A-Z]', '', name.upper())
    total = 0
    log = [f"Calculating Personality for: {name} -> {clean_name}"]
    for i, letter in enumerate(clean_name): # 'i' is the index
        if letter not in VOWELS and not (letter == 'Y' and is_y_vowel(clean_name, i)):
            value = letter_values.get(letter, 0)
            total += value
            log.append(f"  '{letter}' (Consonant) = {value}")
        else:
            log.append(f"  '{letter}' (Vowel) skipped")

    log.append(f"  Total Sum = {total}")

    reduction_result = reduce_number(total)
    log.append(reduction_result['log'])
    return {'number': reduction_result['final'], 'sum': total, 'log': "\n".join(log)}

def calculate_life_path(birth_date_str):
    """
    Calculates the Life Path Number from the birth date (YYYY-MM-DD).
    Sums Year, Month, Day digits individually.
    """
    log = [f"Calculating Life Path for: {birth_date_str}"]
    try:
        # Ensure input is parsed correctly
        if isinstance(birth_date_str, datetime.date):
            birth_date = birth_date_str
        elif isinstance(birth_date_str, datetime.datetime):
             birth_date = birth_date_str.date()
        else:
            # This is your original parsing for string input
            birth_date = datetime.datetime.strptime(birth_date_str, '%Y-%m-%d').date()

        year = birth_date.year
        month = birth_date.month
        day = birth_date.day
        log.append(f"  Date parsed: Year={year}, Month={month}, Day={day}")

        # Sum digits of year, month, day (as per original app script logic)
        total = sum(int(digit) for digit in str(year)) + \
                sum(int(digit) for digit in str(month)) + \
                sum(int(digit) for digit in str(day))

        log.append(f"  Digits sum ({year}+{month}+{day}): {total}") # Using concatenated method from Apps Script

        reduction_result = reduce_number(total)
        log.append(reduction_result['log'])
        return {'number': reduction_result['final'], 'sum': total, 'log': "\n".join(log)}

    except ValueError:
        log.append("  Error: Invalid date format. Please use YYYY-MM-DD.")
        return {'number': 'Error', 'sum': 0, 'log': "\n".join(log)}
    except Exception as e:
         log.append(f"  An unexpected error occurred: {e}")
         return {'number': 'Error', 'sum': 0, 'log': "\n".join(log)}


# --- Main Calculation Function ---
def calculate_all_numerology(full_name, birth_date_str):
    """
    Calculates all core numbers for a given name and birth date.
    Returns a dictionary containing results and logs.
    Prints logs to console during calculation.
    """
    # Commenting out print statements as per your request for Streamlit integration
    # print(f"\n--- Calculating Numerology for {full_name}, DOB: {birth_date_str} ---")

    expression = calculate_expression(full_name)
    # print("\n" + expression['log']) # Print log as it happens

    soul_urge = calculate_soul_urge(full_name)
    # print("\n" + soul_urge['log']) # Print log as it happens

    personality = calculate_personality(full_name)
    # print("\n" + personality['log']) # Print log as it happens

    life_path = calculate_life_path(birth_date_str)
    # print("\n" + life_path['log']) # Print log as it happens

    results = {
        "Expression": expression,
        "Soul Urge": soul_urge,
        "Personality": personality,
        "Life Path": life_path
    }

    # Commenting out summary print block
    # print("\n--- Numerology Summary ---")
    # print(f"Expression Number:  Sum={results['Expression']['sum']} -> Final={results['Expression']['number']}")
    # print(f"Soul Urge Number:   Sum={results['Soul Urge']['sum']} -> Final={results['Soul Urge']['number']}")
    # print(f"Personality Number: Sum={results['Personality']['sum']} -> Final={results['Personality']['number']}")
    # print(f"Life Path Number:   Sum={results['Life Path']['sum']} -> Final={results['Life Path']['number']}")
    # print("------------------------\n")

    # Return the results dictionary which contains the final numbers and the logs
    return results

# End of file D:\AstroReportTool\numerology_calculator.py