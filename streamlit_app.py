# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!
    """)

import streamlit as st

name_on_order = st.text_input("Name of Smoothie")
st.write("The name on your smoothie will be:", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
)
if ingredients_list:
    # Combine ingredients into a single string
    ingredients_string = ' '.join(ingredients_list)

    # Adjust the INSERT statement based on the actual table structure
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients)
        VALUES ('{ingredients_string}')
    """

    # Show the SQL statement for debugging
    st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie '{name_on_order}' is ordered!", icon="✅")
