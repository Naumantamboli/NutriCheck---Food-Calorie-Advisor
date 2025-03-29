import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input_prompt, image):
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        # Format image for Gemini
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return FileNotFoundError("No file uploaded")

# setup the streamlit application
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

input_prompt = """
You are an expert nutritionist. Analyze the food items in the image, calculate the total calories, 
and list the calorie count for each item. Mention if the food is healthy or unhealthy. 
If the food is unhealthy, suggest healthier alternatives from the same cuisine category.

Format:
1. Item 1 - no of calories
2. Item 2 - no of calories
---
Total calories: XYZ
Health Status: Healthy/Unhealthy
---
If unhealthy, suggest healthier food alternatives based on the cuisine.
Example:
- If unhealthy and Indian, suggest healthy Indian food.
- If unhealthy and Chinese, suggest healthy Chinese food.
"""

if submit:
    if uploaded_file:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)

        st.header("The response is")
        st.write(response)
    else:
        st.error("Please upload an image first.")
