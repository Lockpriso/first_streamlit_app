import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')


streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# import csv file
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# add multi select menu
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show =my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# New section to display streamlit 
#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response)

#create the repeatable code block (function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
    
# Make header out of it
streamlit.header("Fruityvice Fruit Advice!")
try:
        #Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
        fruit_choice = streamlit.text_input('What fruit would you like information about?')
        if not fruit_choice:
              streamlit.error("Please select a fruit to get information.")
        else:
           back_from_function=get_fruityvice_data(fruit_choice)
           streamlit.dataframe(fruityvice_normalized)
except URLError as e:
     streamlit.error()
           
           
#streamlit.write('The user entered ', fruit_choice)


#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruit_choice)

# write your own comment -what does the next line do? 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
#streamlit.dataframe(fruityvice_normalized)

streamlit.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from FRUIT_LOAD_LIST")
        return my_cur.fetchall()

##add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
    
    


#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
       my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
       return "Thanks for adding"+ new_fruit
    
add_my_fruit=streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx= snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
 
streamlit.stop() 

#my_cur = my_cnx.cursor()
#my_cur.execute("select * from FRUIT_LOAD_LIST")
#my_data_rows = my_cur.fetchall()
#streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_rows)

#"Adding second selection tex
#Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
Second_fruit_choice = streamlit.text_input('What fruit would you like to add?','plum')
streamlit.write('Thanks for adding ', Second_fruit_choice)

#import requests
Second_fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+Second_fruit_choice)
#streamlit.text(Second_fruit_choice)

# write your own comment -what does the next line do? 
Second_fruityvice_normalized = pandas.json_normalize(Second_fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(Second_fruityvice_normalized)

#streamlit.write('Thanks for adding', add_my_fruit)
my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
