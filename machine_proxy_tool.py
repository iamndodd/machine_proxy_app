import streamlit as st
import pandas as pd
from PIL import Image

# Make app full-width
st.set_page_config(layout="wide")

# Load an image from file
img = Image.open("machine_examples.png")


# background colour
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d3d3d3;  /* light gray background */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# text box colour for descriptions
def custom_box(text, bg_color="#e6f4ea", text_color="#1b4332"):
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            color: {text_color};
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# --- Data ---
data = {
    "Environmental Impact Metric": [
        "Global warming", "Stratospheric ozone depletion", "Ionizing radiation",
        "Ozone formation, Human health", "Fine particulate matter formation",
        "Ozone formation, Terrestrial ecosystems", "Terrestrial acidification",
        "Freshwater eutrophication", "Marine eutrophication",
        "Terrestrial ecotoxicity", "Freshwater ecotoxicity", "Marine ecotoxicity",
        "Human carcinogenic toxicity", "Human non-carcinogenic toxicity",
        "Land use", "Mineral resource scarcity", "Fossil resource scarcity",
        "Water consumption"
    ],
    "Units": [
        "kg CO₂ eq", "kg CFC-11 eq", "kBq Co-60 eq", "kg NOₓ eq", "kg PM10 eq",
        "kg NOₓ eq", "kg SO₂ eq", "kg P eq", "kg N eq", "kg 1,4-DCB eq",
        "kg 1,4-DCB eq", "kg 1,4-DCB eq", "kg 1,4-DCB eq", "kg 1,4-DCB eq",
        "m²a", "kg Fe eq", "kg oil eq", "m³"
    ],
    "Cat Electronics": [20.15, 1.01E-05, 1.764, 0.0646, 0.0543, 0.0667, 0.1179, 0.0273, 0.0011,
                   369.34, 15.06, 19.55, 4.19, 194.58, 0.867, 0.834, 5.263, 0.209],
    "Cat High": [8.59, 3.62E-06, 0.515, 0.0214, 0.0256, 0.0221, 0.0569, 0.0116, 0.0005,
                     253.96, 6.49, 8.12, 2.88, 52.49, 0.288, 0.284, 2.334, 0.096],
    "Cat Moderate": [5.28, 2.38E-06, 0.224, 0.0149, 0.0171, 0.0155, 0.0411, 0.0065, 0.0003,
                 155.30, 3.06, 3.84, 2.50, 29.99, 0.173, 0.197, 1.364, 0.060],
    "Cat Simple": [3.22, 9.82E-07, 0.201, 0.0080, 0.0064, 0.0086, 0.0114, 0.0019, 0.0002,
                        30.21, 0.48, 0.63, 2.40, 6.06, 0.127, 0.120, 0.790, 0.032]
}

df = pd.DataFrame(data)

# --- Category descriptions + colors ---
category_descriptions = {
    "Simple": {
        "desc": (
            "Category 1 (Simple): Objects that are mostly simple in design and made "
            "of bulky raw materials. Even if the object has some complexity, the heavy "
            "materials dominate, making the overall environmental impact mostly predictable."
        ),
        "color": "lightgreen"
    },
    "Moderate": {
        "desc": (
            "Category 2 (Moderate): Mechanical objects that sometimes use electricity, "
            "but contain very few electronic components. Examples include simple machines "
            "or hand-powered devices."
        ),
        "color": "lightblue"
    },
    "High": {
        "desc": (
            "Category 3 (High): Mechanical devices that rely more heavily on electrical "
            "parts to operate. These are not purely electronic devices but include "
            "mechanical work powered by electricity, e.g., vacuum cleaners or mixers."
        ),
        "color": "khaki"  # yellow-ish
    },
    "Electronics": {
        "desc": (
            "Category 4 (Electronics): Devices where the main function is electrical, "
            "such as TVs, computers, or phones. These are included mainly for comparison "
            "and are not part of the primary scope of this research."
        ),
        "color": "plum"  # purple-ish
    }
}


# --- Streamlit App ---
st.title("Embedded Environmental Impact Estimator For Machines and Tools")

# --- Layout with four columns ---
very_left, left, middle, right = st.columns([0.5, 1, 0.05, 2.5])  # middle column small for separator

with very_left:
    # Display the image
    st.image(img, use_container_width=True)


with left:
    # Input: float number
    st.markdown("<h2 style='font-size:20px;'>Enter a Mass (kg):</h2>", unsafe_allow_html=True)
    value = st.number_input("Mass (kg):", min_value=0.0, step=0.1, label_visibility="collapsed")

    # Dropdown: category selection
    st.markdown("<h2 style='font-size:20px;'>Select Overall Machine Complexity:</h2>", unsafe_allow_html=True)
    category = st.selectbox("Pick a category:", list(category_descriptions.keys()))

    # Determine column name from dropdown
    col_name = f"Cat {category}"

    # Show description when category selected
    info = category_descriptions[category]
    custom_box(info["desc"], info["color"])

with right:
    if value > 0:
        df["Result"] = df[f"Cat {category}"] * value
        df["Result"] = df["Result"].round(decimals=10).astype(str) + " - " + df["Units"]
        
        number_of_rows = df["Result"].count()
        content_fit_row_count = int(number_of_rows * 37.5)

        st.markdown("<h2 style='font-size:20px;'>Results:</h2>", unsafe_allow_html=True)
        st.dataframe(df[["Environmental Impact Metric", "Result"]], height=content_fit_row_count, use_container_width=True, hide_index=True)
