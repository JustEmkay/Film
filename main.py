import streamlit as st
import cv2
import numpy as np
import requests
import time


API_URL = "http://127.0.0.1:5000/api/"

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
    
                   
def main():
    
    with st.sidebar:
        st.header("Film Ne2Po",divider='rainbow')    

        with st.container(border=True):
            option : str = st.radio("Select input option",
                              ['Upload Photo','Image URL','Capture Photo'])
    st.header("Film Negative to Positive",divider='rainbow',anchor=False)
    
    if option == 'Upload Photo':
        image_file = st.file_uploader("upload image here",type=['png', 'jpg'])
        if image_file is not None:
            bytes_data = image_file.getvalue()
            image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                     
    if option == 'Capture Photo':
        
        picture = st.camera_input("Take a picture")
        if picture is not None:
            st.image(picture)

            bytes_data = picture.getvalue()
            image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        
    # if option == 'Image URL':
    #     try:
    #         image_url = st.text_input('image url',label_visibility='collapsed',
    #                               placeholder="Enter/paste image url here")
    #         if image_url : st.image(image_url,output_format='JPEG')
    #         st.text(type(image_url))
    #     except Exception as e:
    #         st.error(f"{e}")
        
    col1 , col2 = st.columns(2)
    
    with col1.container(border=True):
        r_col,g_col,b_col = st.columns(3)
        
        in_r = r_col.number_input("in_r",step=1,value=0)
        in_g = g_col.number_input("in_g",step=1,value=127)
        in_b = b_col.number_input("in_b",step=1,value=255)

    with col2.container(border=True):
        r_col2,g_col2,b_col2 = st.columns(3)
        
        out_r = r_col2.number_input("out_r",step=1,value=255)
        out_g = g_col2.number_input("out_g",step=1,value=80)
        out_b = b_col2.number_input("out_b",step=1,value=20)

    lut_in = [in_r, in_g, in_b]
    lut_out = [out_r, out_g, out_b]

    if st.button("Confirm",use_container_width=True):
        with st.status("Uploading Negative-image for conversion...", expanded=True) as status:
            time.sleep(1)
            status.update(
                label="Processing image..", state="running", expanded=False
            )
            st.text('')
            
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
    main()

