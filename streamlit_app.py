# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Title and description
st.title("My Parent's New Healthy Dinner")
st.write("Choose the fruit you want in your custom smoothie!")

# Text input for smoothie name
name_on_order = st.text_input("Name of Smoothie")
st.write("The name on your smoothie will be:", name_on_order)

# Snowflake connection
try:
    cnx = st.connection("Snowflake")
    session = cnx.session()

    # Query fruit options
    snowflake_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
    fruit_options = pd.DataFrame(snowflake_df.collect())['FRUIT_NAME'].tolist()

    # Multiselect for ingredients
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        fruit_options
    )

    if ingredients_list:
        # Combine ingredients into a single string
        ingredients_string = ', '.join(ingredients_list)

        # Parameterized SQL for safety
        my_insert_stmt = """
            INSERT INTO smoothies.public.orders (name, ingredients)
            VALUES (%s, %s)
        """

        # Show the SQL statement for debugging
        st.write(f"Your smoothie '{name_on_order}' includes: {ingredients_string}")

        # Button to submit order
        time_to_insert = st.button("Submit Order")
        if time_to_insert:
            session.sql(my_insert_stmt, (name_on_order, ingredients_string)).collect()
            st.success(f"Your Smoothie '{name_on_order}' is ordered!", icon="✅")

    # Optional: Fetching fruit data from external API
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
    if smoothiefroot_response.status_code == 200:
        st.write("Fruit API Response:", smoothiefroot_response.json())
    else:
        st.error("Failed to fetch data from the fruit API.")
except Exception as e:
    st.error(f"An error occurred: {e}")
