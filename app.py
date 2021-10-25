import qrcode
from PIL import Image
import numpy as np
import streamlit as st
import base64
from io import BytesIO
from numpy import asarray
# ------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title='UPI QR Code Generator', page_icon=None,
                   layout='centered', initial_sidebar_state='auto')
# Set page title
st.title('UPI QR Code Generator')
# ------------------------------------------------------------------------------------------------------------
height = 300
width = 300

mode = st.selectbox('Select details : UPI ID or Bank Details',
                    options=['UPI ID', 'Bank Details'])

if mode == 'Bank Details':
    bank_account_number = st.text_input(
        'Enter Bank Account Numebr : ')  # '6999413500377638'
    bank_ifsc = st.text_input('Enter Bank IFSC code : ')  # 'YESB0CMSNOC'
    name_ac = st.text_input('Enter Receipient name : ')
    if (name_ac == '') or (name_ac == ' '):
        st.warning('Receipent name cannot be blank')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # L -> M -> Q -> H
        box_size=4,
        border=4,
    )

    qr.add_data('upi://pay?pa='+str(bank_account_number)+'@'+str(bank_ifsc) +
                '.ifsc.npci&pn='+str(name_ac)+'&cu=INR')


elif mode == 'UPI ID':
    # bank_account_number = st.text_input('Enter Bank Account Numebr : ')#'6999413500377638'
    upi_id = st.text_input('Enter UPID ID : ')  # 'YESB0CMSNOC'
    name_ac = st.text_input('Enter Receipient name : ')
    if (name_ac == '') or (name_ac == ' '):
        st.warning('Receipent name cannot be blank')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # L -> M -> Q -> H
        box_size=4,
        border=4,
    )

    qr.add_data('upi://pay?pa='+upi_id +
                '&pn='+str(name_ac)+'&cu=INR')

    # Setting fit=True ensures the minimum size.
qr.make(fit=str(height)+'x'+str(width))

img = qr.make_image(fill_color="black", back_color="white")
img = img.resize((height, width))

st.write('UPI QR Code : ')
st.image(img)

an_image = img

x = asarray(an_image).astype('uint8')

x[x == 1] = 255


def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href


# Original image came from cv2 format, fromarray convert into PIL format
result = Image.fromarray(x)
st.markdown(get_image_download_link(result, name_ac+'_upi.png',
                                    'Click here to download UPI QR code'), unsafe_allow_html=True)
