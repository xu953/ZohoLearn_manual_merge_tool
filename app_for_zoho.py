# -*- coding: utf-8 -*-
# Zhenyu Xu
# @ 11/17/2022

from bs4 import BeautifulSoup
import streamlit as st
import zipfile


# Initialization
dictionary={}  # stores all html files
counter = 0.0  # stores number of html files not in subdirectory
empty_html = '<html><head></head><body></body></html>'  # append html here to merge files
num = 0  # used to provide a sortable key to the dictionary

def readHTML(html, path) :
    # Extract file number from html page
    soup = BeautifulSoup(html, features="html.parser")
    html = html.decode("utf-8")
    # Fix image references if file path for them is provided
    if path != "":
        if path[-1] == '/':  # Remove trailing slash
            path = path[:-1]

        for img in soup.findAll('img'):
            html = html.replace(img.get('src'), path + "/inline-images" + img.get('src').split("/inline-images", 1)[1])

    # Cleanup uneccesary parsed content
    for script in soup(["script", "style"]):
        script.extract() 

    # Gets the header decimal number for each file after its been parsed and cleaned
    potentialNum = soup.get_text().replace('\n', '')[:3]
    if potentialNum.replace('.', '').isnumeric():
        num = float(soup.get_text().replace('\n', '')[:3])
    else:
        num = counter + 0.01

    # Update dictionary with appropriate key and decoded html content
    dictionary.update({num: html})


st.set_page_config(
                    page_title="Manual PDF Generator - FP",
                    page_icon=":arrow_up:"
)

# Show Fortress Logo
# header_image_html = "<img src='fortress_logo.png' class='img-fluid' width='50%'>"
# st.markdown(header_image_html, unsafe_allow_html=True)

st.title('Zoho Learn Manual HTML generator')

# Instructions
with st.expander("Instructions"):
     st.markdown(""
     "Please upload the downloaded zip file from Zoho Learn below\n\n"
     "")

# Add empty space
st.write("#")

# File uploader
st.header('Upload compressed folder of Zoho manual')
uploaded_file = st.file_uploader("Choose the zipped file", type=["zip"], accept_multiple_files=False)


if uploaded_file:
    # Get path to inline_images
    zipp = zipfile.ZipFile(uploaded_file, 'r')
    sub_dir = zipp.namelist()[0].split('/')[0]
    main_dir = uploaded_file.name.split('.zip')[0]
    file_path = main_dir +'/'+sub_dir
    # print(file_path)

    for filename in zipp.namelist():
        # Get all the contents
        if 'templates' in filename:  # and 'tables-of-contents' not in filename
            print("RUNNING...")
            f_html = zipp.open(filename)
            readHTML(f_html.read(), file_path)


    # Sort dictionary based on keys which are header section decimals
    # Iterate over sorted dictionary merging html
    # print(sorted(dictionary.items(), key=lambda x:x[0]))
    for key, value in sorted(dictionary.items(), key=lambda x:x[0]):
        empty_html = empty_html.replace('</body></html>', value + '</body></html>')

    # save merged html to disc
    with open('merged.html', 'w', encoding="utf-8") as f:
        f.write(empty_html)

    with open('merged.html', 'r', encoding="utf-8") as f:
        st.download_button('Download HTML Report', f, file_name="mergedReport.html")