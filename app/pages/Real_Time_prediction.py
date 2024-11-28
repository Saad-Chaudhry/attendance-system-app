import streamlit as st
from ..Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time

# st.set_page_config(page_title='Predictions')
st.subheader('Real-Time Attendance System')

# Retrieve the data from redis database
with st.spinner('Retrieving Data From Redis DB ....'):
    redis_face_db = face_rec.retrive_data(name='academy:register')
    st.dataframe(redis_face_db)
    st.success("Data successfully retrieved from Redis")

# time
waitTime = 30  # time in sec
setTime = time.time()
realtimepred = face_rec.RealTimePred()  # real time prediction class


# Real Time Prediction
# streamlit webrtc
# callback function
def video_frame_callback(frame):
    global setTime

    img = frame.to_ndarray(format="bgr24")  # 3 dimension numpy array
    # operation that you can perform on the array
    pred_img = realtimepred.face_prediction(img, redis_face_db,
                                            'facial_features', ['Name', 'Role'], thresh=0.5)

    time_now = time.time()
    diff_time = time_now - setTime
    if diff_time >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time()  # reset time
        print('Save Data to redis database')

    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback,
                rtc_configuration={
                    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                })
