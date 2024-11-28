import streamlit as st
from Home import face_rec

st.set_page_config(page_title='Reporting')

st.subheader('Reporting')

# Retrieve logs data and show in Report.py
# extract data from redis list
name = 'attendance:logs'


def load_logs(name, end=-1):
    logs_list = face_rec.r.lrange(name, start=0, end=end)  # extract all data from the redis database
    return logs_list


# tabs to show the info
tab1, tab2 = st.tabs(['Registered Data', 'Logs'])

with tab1:
    if st.button('Refresh Data'):
        # Retrieve the data from Redis Database
        with st.spinner('Retrieving Data from Redis DB ...'):
            if face_rec.r.exists('academy:register') == 0:
                st.error('No data found in the Redis Database')
            else:
                redis_face_db = face_rec.retrieve_data(name='academy:register')
                st.dataframe(redis_face_db[['Name', 'Role']])

with tab2:
    if st.button('Refresh Logs'):
        st.write(load_logs(name=name))
