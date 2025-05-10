import streamlit as st
import datetime
import numerology_calculator_patched as nc # nc is an alias for your script

# --- Page Configuration ---
st.set_page_config(
    page_title="Numerology Calculator",
    page_icon="🔮",
    layout="centered"
)

# --- Main Application UI ---
st.title("Numerology Calculator 🔮")
st.markdown("""
Enter your full name and date of birth to calculate your core numerology numbers.
The calculation logs and results will be displayed below.
""")

st.divider()

# --- Input Fields ---
st.subheader("Enter Your Details:")
full_name = st.text_input("Full Name:", placeholder="E.g., Jane Emily Doe")

# Default to a reasonable date, e.g., 30 years ago
default_dob = datetime.date.today() - datetime.timedelta(days=30*365 + 7) # Approx 30 years
birth_date_obj = st.date_input(
    "Date of Birth:",
    value=default_dob,
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date.today() # Prevent future dates
)

st.divider()

# --- Calculation and Display ---
if st.button("✨ Calculate Numerology ✨", type="primary", use_container_width=True):
    if full_name and birth_date_obj:
        # Your numerology_calculator_patched.py's calculate_life_path
        # can handle datetime.date objects or string 'YYYY-MM-DD'.
        # Passing the object directly is fine.
        # birth_date_to_pass = birth_date_obj.strftime('%Y-%m-%d') # Option 1: Pass as string
        birth_date_to_pass = birth_date_obj # Option 2: Pass as date object (your script supports this)

        st.info(f"Calculating for: **{full_name}** (DOB: **{birth_date_obj.strftime('%Y-%m-%d')}**)")
        st.spinner("Performing calculations...") # Show a spinner during calculation

        try:
            # Call the main calculation function from your imported module
            all_results = nc.calculate_all_numerology(full_name, birth_date_to_pass)

            st.success("Calculations Complete!")
            st.balloons()

            # Displaying results and logs
            st.subheader("📊 Your Numerology Report:")

            for number_name, data in all_results.items():
                st.markdown(f"---")
                col1, col2 = st.columns([3,1]) # Make number name prominent
                with col1:
                    st.markdown(f"#### {number_name} Number")
                with col2:
                    st.markdown(f"### `{data.get('number', 'N/A')}`") # .get for safety

                st.markdown(f"**Initial Sum:** `{data.get('sum', 'N/A')}`")

                with st.expander(f"View Calculation Log for {number_name}"):
                    st.text(data.get('log', 'No log available.')) # Use st.text for pre-formatted log

        except Exception as e:
            st.error(f"An error occurred during calculation: {e}")
            st.exception(e) # Shows a more detailed traceback for debugging if needed

    elif not full_name:
        st.error("❗ Please enter your full name.")
    else: # Should not happen if birth_date_obj is always set by st.date_input
        st.warning("❗ Please ensure all details are entered.")

st.divider()
st.markdown("""
<div style="text-align: center; font-size:small; color:grey;">
    Numerology calculations are based on the provided script's logic.
</div>
""", unsafe_allow_html=True)