import streamlit as st
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time

st.subheader('Real-Time Attendance System')
st.write('This page is used to take attendance in real-time using the webcam')

# time
waitTime = 5  # time in sec
setTime = time.time()
realtimepred = face_rec.RealTimePred()  # real time prediction class
redis_face_db = face_rec.retrieve_data(name='academy:register')


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
