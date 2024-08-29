import streamlit as st
import cv2
import numpy as np
import requests
import time

if 'api_connection' not in st.session_state : 
    st.session_state.api_connection = False

API_URL = "http://127.0.0.1:5000/api/"

# GET REQUEST
def test_api():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return True
    return False


# POST REQUEST
def send_image(image : list[list] , lut_in : list[int],lut_out : list[int]):
    
    image_data = {"image_data":image.tolist(),"lut_in":lut_in,"lut_out": lut_out}

    response = requests.post(API_URL,json=image_data)
    if response.status_code == 200:
        st.toast(":green-background[Compeleted Conversion]",icon='✔️')
        return response.json()
    else:
        st.toast(":red-background[Error Occured!]",icon="⚠️")
        return None
  
def api_connection_check():
    with st.status("Establishing connection...",expanded=False) as status:
        time.sleep(2)
        status.update(
            label="Accessing API...", state="running", expanded=False
        )
        time.sleep(2)
        if not test_api():
            time.sleep(2)
            status.update(
                label="Accessing API...", state="error", expanded=False
            )
            st.error("Error Connecting to API",icon="❌")
            time.sleep(1)
            return False
        else:
            status.update(
                label="Accessing API...", state="complete", expanded=True
            )
            time.sleep(2)
            st.success("Connection Successful",icon="✔")                
            time.sleep(2)
            status.update(
                label="Swicthing to Home-page.....", state="running", expanded=True
            )
            with st.spinner('Wait for it...'):
                time.sleep(5)
            return True           
            
            
                  
def main():
    
    image_capture = None
    image_file = None
    
    with st.sidebar:
        st.header("Film Ne2Po",divider='rainbow')    

        with st.container(border=True):
            option : str = st.radio("Select input option",
                              ['Upload Photo','Image URL','Capture Photo'])

        if option == 'Capture Photo':
            image_capture = st.camera_input("Take a picture")
    
        if option == 'Upload Photo':
            image_file = st.file_uploader("upload image here",type=['png', 'jpg'])
    
        with st.container(border=True):
            r_col,g_col,b_col = st.columns(3)
            
            in_r = r_col.number_input("in_r",step=1,value=0)
            in_g = g_col.number_input("in_g",step=1,value=127)
            in_b = b_col.number_input("in_b",step=1,value=255)

        with st.container(border=True):
            r_col2,g_col2,b_col2 = st.columns(3)
            
            out_r = r_col2.number_input("out_r",step=1,value=255)
            out_g = g_col2.number_input("out_g",step=1,value=80)
            out_b = b_col2.number_input("out_b",step=1,value=20)
            
            
    header_col , pop_col = st.columns([3,1],vertical_alignment='bottom')       
    header_col.header("Film Negative to Positive",divider='rainbow',anchor=False)
    
    with pop_col.popover("height",
                         use_container_width=True):
        if image_capture is not None:
            st.image(image_capture)
            bytes_data = image_capture.getvalue()
            image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8),
                                cv2.IMREAD_COLOR)
        elif image_file is not None:
            bytes_data = image_file.getvalue()
            image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        else:
            st.info("Upload/Capture Negative-image")  
   

    # if option == 'Image URL':
    #     try:
    #         image_url = st.text_input('image url',label_visibility='collapsed',
    #                               placeholder="Enter/paste image url here")
    #         if image_url : st.image(image_url,output_format='JPEG')
    #         st.text(type(image_url))
    #     except Exception as e:
    #         st.error(f"{e}")
    
    lut_in = [in_r, in_g, in_b]
    lut_out = [out_r, out_g, out_b]
        

    if st.button("Confirm",use_container_width=True):
        with st.status("Uploading Negative-image for conversion...", expanded=True) as status:
            time.sleep(1)
            status.update(
                label="Processing image..", state="running", expanded=False
            )
            
            image_out = send_image(image,lut_in,lut_out)
            
            if image_out:
                status.update(
                    label="Conversion Successful", state="running", expanded=False
                )
                time.sleep(1)
                status.update(
                    label="Downloading Data", state="running", expanded=False
                )
                time.sleep(1)
                image_out_restore = np.array(image_out["image_out"], dtype=np.uint8)
                status.update(
                    label="Conversion complete!", state="complete", expanded=True
                )
                cv2.imwrite('out_image.jpg', image_out_restore)

            else:
                status.update(
                    label="Error ⚠", state="error", expanded=True
                )
                st.text("An unexpected error occured!!")
                

            og_col,out_col = st.columns(2)
            
            og_col.subheader("Input: :red[Negative]",anchor=False,divider='red')
            og_col.image(image=image,channels='BGR')
            
            out_col.subheader("Output: :green[Positive]",anchor=False,divider='green')
            out_col.image(image=image_out_restore,channels='BGR',output_format='auto') 
            # out_col.image(image='out_image.jpg')   



    
if __name__ == '__main__' :
    if not st.session_state.api_connection:
        st.session_state.api_connection = api_connection_check()
        
    if st.session_state.api_connection:
        main()

