import streamlit as st
from Home import face_rec
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Authentication Function
def authenticate(username, password):
    # Replace these with your actual credentials
    valid_username = "admin"
    valid_password = "password123"
    return username == valid_username and password == valid_password

# Login Page
if not st.session_state.authenticated:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid username or password.")
else:
    # Main Registration Page
    st.subheader("Registration Form")

    # Init registration form
    registration_form = face_rec.RegistrationForm()

    # Step-1: Collect person name and role
    person_name = st.text_input(label="Name", placeholder="First & Last Name")
    role = st.selectbox(label="Select your Role", options=("Student", "Teacher"))

    # Step-2: Collect facial embedding of that person
    def video_callback_func(frame):
        img = frame.to_ndarray(format="bgr24")  # 3D array BGR
        reg_img, embedding = registration_form.get_embedding(img)
        # Two-step process: save data into a local file
        if embedding is not None:
            with open("face_embedding.txt", mode="ab") as f:
                np.savetxt(f, embedding)

        return av.VideoFrame.from_ndarray(reg_img, format="bgr24")

    webrtc_streamer(
        key="registration",
        video_frame_callback=video_callback_func,
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}],
        },
    )

    # Step-3: Save the data in Redis database
    if st.button("Submit"):
        return_val = registration_form.save_data_in_redis_db(person_name, role)
        if return_val == True:
            st.success(f"{person_name} registered successfully")
        elif return_val == "name_false":
            st.error("Please enter the name: Name cannot be empty or spaces")
        elif return_val == "file_false":
            st.error("face_embedding.txt is not found. Please refresh the page and execute again.")

    # Logout Button
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()
