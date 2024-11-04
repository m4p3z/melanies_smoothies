# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Choose your fruits you want in your custom smoothie!
    \n !Elija las frutas que quiere para su smoothie personalizado!.
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

### Add multiselect:
Nombre = st.text_input("Nombre para el pedido / Order´s name", "Nombre")

ingredients_list = st.multiselect(
    'Elija hasta 5 ingredientes/Choose until 5 ingredients: ', 
    my_dataframe,
    max_selections=5
)

if (ingredients_list):
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string =''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Información Nutricional/Nutritional Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data = fruityvice_response.json(), user_container_width=True)

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """' , '""" + Nombre + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        #session.sql(my_insert_stmt).collect()

        if ingredients_string:

            if Nombre != 'Nombre':
                session.sql(my_insert_stmt).collect()                
                st.success(Nombre + ' Your Smoothie is ordered!', icon="✅")


#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response)
#st.text(fruityvice_response.json())
#fv_df = st.dataframe(data = fruityvice_response.json(), user_container_width=True)

