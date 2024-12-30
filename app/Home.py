import streamlit as st

st.set_page_config(page_title='Attendance System', layout='wide')

st.header('Attendance System using Face Recognition')

with st.spinner("Loading Models and Connecting to Redis db ..."):
    import face_rec

st.write("[Click here to go to Web Dashboard](https://oasufr-082fd6eb773f.herokuapp.com/)")

# Retrieve the data from redis database
with st.spinner('Retrieving Data From Redis DB ....'):
    if face_rec.r.exists('academy:register') == 0:
        st.error('No data found in the Redis Database')
    else:
        redis_face_db = face_rec.retrieve_data(name='academy:register')
        st.dataframe(redis_face_db)
        st.success("Data successfully retrieved from Redis")
