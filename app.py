import streamlit as st
import datetime
import csv # For reading the interpretations CSV
import numerology_calculator_patched as nc

# --- Page Configuration ---
st.set_page_config(
    page_title="Numerology Calculator",
    page_icon="🔢",
    layout="centered"
)

# --- Helper function to load interpretations ---
@st.cache_data # Cache the data so CSV is loaded only once
def load_interpretations(csv_file_path='interpretations.csv'):
    interpretations = {}
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            if 'key' not in reader.fieldnames or 'text' not in reader.fieldnames:
                st.error(f"CSV file '{csv_file_path}' must contain 'key' and 'text' columns. Interpretations will not be loaded.")
                return {} # Return empty if headers are wrong
            for row in reader:
                interpretations[row['key']] = row['text']
        if not interpretations:
            st.warning(f"No data found in '{csv_file_path}' or file is empty. Interpretations might not display.")
        # else:
            # st.success("Interpretations loaded successfully.") # Optional: for debugging
    except FileNotFoundError:
        st.error(f"Interpretation file not found: '{csv_file_path}'. Please ensure it's in the app's root directory. Interpretations will not be available.")
        return {}
    except Exception as e:
        st.error(f"Error loading interpretations from '{csv_file_path}': {e}")
        return {}
    return interpretations

# --- Helper function to parse numerology number strings ---
def get_numerology_parts(num_str):
    """
    Parses a numerology number string (e.g., "5", "11", "23/5")
    into an initial part and a final part.
    Returns (initial_part, final_part).
    If num_str is a single number like "5", returns (None, "5").
    If num_str is invalid or not a string, returns (None, None).
    """
    if not isinstance(num_str, str) or not num_str:
        return None, None

    if '/' in num_str:
        parts = num_str.split('/', 1)
        if len(parts) == 2 and parts[0].strip().isdigit() and parts[1].strip().isdigit():
            return parts[0].strip(), parts[1].strip()
        else: # Malformed (e.g., "23/abc", "23/", "/5")
            return None, num_str # Fallback for display, but key lookup will likely fail
    elif num_str.strip().isdigit():
        return None, num_str.strip()
    else: # Non-numeric string like "Error", "Invalid Input"
        return None, None # Indicates no valid parts for lookup

# Load interpretations once at the start
interpretations_data = load_interpretations()

# --- Main Application UI ---
st.title("Numerology Calculator 🔮")
st.markdown("""
Enter your full name and date of birth to calculate your core numerology numbers.
The calculation logs, results, and their interpretations will be displayed below.
""")

st.divider()

# --- Input Fields ---
st.subheader("Enter Your Details:")
full_name = st.text_input("Full Name:", placeholder="E.g., Jane Emily Doe")
default_dob = datetime.date.today() - datetime.timedelta(days=30*365 + 7)
birth_date_obj = st.date_input(
    "Date of Birth:",
    value=default_dob,
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date.today()
)

st.divider()

# --- Calculation and Display ---
if st.button("✨ Calculate Numerology ✨", type="primary", use_container_width=True):
    if full_name and birth_date_obj:
        birth_date_to_pass = birth_date_obj
        st.info(f"Calculating for: **{full_name}** (DOB: **{birth_date_obj.strftime('%Y-%m-%d')}**)")
        st.spinner("Performing calculations...")

        try:
            all_results = nc.calculate_all_numerology(full_name, birth_date_to_pass)
            st.success("Calculations Complete!")
            st.balloons()
            st.subheader("📊 Your Numerology Report:")

            # Define the order for display
            numerology_types_ordered = ["Life Path", "Expression", "Soul Urge", "Personality"]

            for number_name in numerology_types_ordered:
                if number_name not in all_results:
                    continue # Should not happen if calculator is correct
                
                data = all_results[number_name]
                st.markdown(f"---") # Horizontal line separator for each number type
                
                col1, col2 = st.columns([3,1])
                with col1:
                    st.markdown(f"#### {number_name} Number")
                with col2:
                    st.markdown(f"### `{data.get('number', 'N/A')}`")
                
                st.markdown(f"**Initial Sum:** `{data.get('sum', 'N/A')}`")

                # --- Display Interpretations ---
                calculated_num_str = data.get('number')
                # Proceed only if the number is valid and interpretations are loaded
                if calculated_num_str and calculated_num_str not in ['Error', 'Invalid Input', 'N/A'] and interpretations_data:
                    initial_part, final_part = get_numerology_parts(calculated_num_str)
                    
                    collected_interpretation_texts = []

                    # 1. Get text for the final_part (e.g., for '5' in '23/5', or '11' in '11')
                    if final_part:
                        final_text_key = f"Numerology{final_part}"
                        text_from_db = interpretations_data.get(final_text_key) # Returns None if key not found

                        # As per your JS: combined_text = final_text if not final_text.startswith('Interpr') else f"[Text not found for {final_part}]"
                        if text_from_db and not text_from_db.lower().startswith('interpr'):
                            display_text = text_from_db
                        else:
                            display_text = f"[Text for aspect '{final_part}' not found or is a placeholder in interpretations.csv]"
                        collected_interpretation_texts.append(display_text)

                    # 2. Get text for the initial_part (e.g., for '23' in '23/5'), if it exists
                    if initial_part:
                        initial_text_key = f"Numerology{initial_part}"
                        # As per your JS: initial_text = get_text(initial_text_key, db_dict, default_text="")
                        # if initial_text: combined_text += f"\n\n{initial_text}"
                        initial_text_from_db = interpretations_data.get(initial_text_key, "") # Default to empty string if not found

                        if initial_text_from_db: # Add if not an empty string (even if it's a placeholder like "Interpr...")
                            # Add a separator if both final_part and initial_part texts are present
                            if collected_interpretation_texts and collected_interpretation_texts[0] != "" and not collected_interpretation_texts[0].startswith("[Text for aspect"):
                                collected_interpretation_texts.append("\n\n---\n\n" + f"**Regarding the initial sum component ({initial_part}):**\n{initial_text_from_db}")
                            else:
                                collected_interpretation_texts.append(f"**Regarding the initial sum component ({initial_part}):**\n{initial_text_from_db}")
                    
                    # Display collected interpretations if any
                    if collected_interpretation_texts:
                        st.markdown(" ") # Little space before interpretation
                        for Rtext_block in collected_interpretation_texts:
                            st.markdown(Rtext_block)
                
                elif not interpretations_data and calculated_num_str and calculated_num_str not in ['Error', 'Invalid Input', 'N/A']:
                     st.warning(f"Interpretations for '{number_name}' not shown. Data from 'interpretations.csv' could not be loaded.")


                with st.expander(f"View Calculation Log for {number_name}"):
                    st.text(data.get('log', 'No log available.'))
                st.markdown(" ") # Extra space after each number's section

        except Exception as e:
            st.error(f"An error occurred during calculation or display: {e}")
            st.exception(e)

    elif not full_name:
        st.error("❗ Please enter your full name.")

st.divider()
st.markdown("""
<div style="text-align: center; font-size:small; color:grey;">
    Numerology calculations are based on the provided script's logic. Interpretations from interpretations.csv.
</div>
""", unsafe_allow_html=True)
