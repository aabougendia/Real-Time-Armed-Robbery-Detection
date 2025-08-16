import streamlit as st
import cv2
from ultralytics import YOLO
import tempfile
import requests

telegram_bot_token = "7472762937:AAH9Z7PWkJhZuDOvRVf9WPnF3YnrNKXKpwo"
chat_id = 1379730969 # sends alerts to my phone for testing

def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"   
    payload = {"chat_id": chat_id, "text": message}

    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            st.error(f"Failed to send Telegram message: {response.text}")
    except Exception as e:
        st.error(f"Error sending Telegram message: {e}")



st.set_page_config(layout="wide")

# Sidebar
st.sidebar.title("Weapon Detection Settings")
video_source = st.sidebar.selectbox(
    "Select Video Source",
    ("MP4 File", "Webcam", "RTSP Stream")
)
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.5)
frame_threshold = st.sidebar.slider("Frames to Trigger Alert", 1, 100, 20)


# Streamlit Session State
if "alert_triggered" not in st.session_state:
    st.session_state.alert_triggered = False
# if "alert_log" not in st.session_state:
    # st.session_state.alert_log = []
if "frame_counter" not in st.session_state:
    st.session_state.frame_counter = 0

# Dashboard Main Title
st.title("Real-Time Armed Robbery Detection App")

# Dashboard layout
col1, col2, col3 = st.columns([4, 0.2, 2])

video_placeholder = col1.empty()
alert_placeholder = col3.empty()

alert_placeholder.markdown(
                     """
                        <div style="
                        background-color: #262730;
                        border: 2px solid black;
                        border-radius: 10px;
                        padding: 20px;
                        width: 400; 
                        height: 250px; 
                        overflow-y: auto;
                        font-family: monospace;
                        color: white;
                    ">
                    <h4 style="text-align:left; color: white;">Alert Panel:</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# load model

model = YOLO("weights/best.pt")
model.model.names[0] = "Weapon"


# Get video source path
if video_source == "MP4 File":
    uploaded_file = st.sidebar.file_uploader("Upload MP4 file", type=["mp4"])
    if uploaded_file is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        temp_file.write(uploaded_file.read())
        video_path = temp_file.name
    else:
        video_path = None

elif video_source == "Webcam":
    video_path = 0
else:  # RTSP
    video_path = st.sidebar.text_input("Enter RTSP URL")

# Track last loaded video name
if "last_video_name" not in st.session_state:
    st.session_state.last_video_name = None

# Determine current video name
current_video_name = None
if video_source == "MP4 File" and uploaded_file is not None:
    current_video_name = uploaded_file.name
elif video_source == "RTSP Stream":
    current_video_name = video_path
elif video_source == "Webcam":
    current_video_name = "webcam"


st.session_state.alert_triggered = False
st.session_state.frame_counter = 0
st.session_state.last_video_name = current_video_name

# If the video file/URL changes, reset alert state
if current_video_name != st.session_state.last_video_name:
    st.session_state.alert_triggered = False
    st.session_state.frame_counter = 0
    # st.session_state.alert_log = []
    st.session_state.last_video_name = current_video_name

if video_path is not None:
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        st.error("Error: Could not open video source.")
    else:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            model_out = model.predict(frame, conf=confidence_threshold, verbose=False)
            annotated_frame = model_out[0].plot()

            is_frame_detected = len(model_out[0].boxes) > 0

            if is_frame_detected:
                st.session_state.frame_counter += 1

            if not st.session_state.alert_triggered and st.session_state.frame_counter >= frame_threshold:
                st.session_state.alert_triggered = True
            


                gmaps_link = r"https://maps.app.goo.gl/MkTYf3qohwLfdTEU6"
                message = f"""ARMED ROBBERY DETECTION APP\n\nDetected Armed Individuals!\nLocation: {gmaps_link}\nPlease Call Emergency Services"""
                send_telegram_message(message)
                
            if st.session_state.alert_triggered:
                alert_placeholder.markdown(
                     """
                        <div style="
                        background-color: #262730;
                        border: 2px solid red;
                        border-radius: 10px;
                        padding: 20px;
                        width: 400px; 
                        height: 250px; 
                        overflow-y: auto;  
                        text-align: left;
                        font-family: monospace;
                        line-height: 0.8;
                    ">
                        <h4 style="text-align:left; font-size: 24px; color: white;">Alert Panel:</h4>
                        <p style="font-size: 14px; color:red; margin:1;">>> ALERT: WEAPON DETECTED</p>
                        <p style="font-size: 14px; color:white; margin:1;">>> Alert message sent to operator via Telegram</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                 alert_placeholder.markdown(
                     """
                        <div style="
                        background-color: #262730;
                        border: 2px solid black;
                        border-radius: 10px;
                        padding: 20px;
                        width: 400px; 
                        height: 250px; 
                        overflow-y: auto;  
                        text-align: left;
                        color: red;
                        font-weight: bold;
                        font-size: 24px;
                        line-height: 1.2;
                    ">
                        <h4 style="text-align:left; color: white;">Alert Panel:</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Convert BGR to RGB for Streamlit
            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(rgb_frame, channels="RGB")

        cap.release()