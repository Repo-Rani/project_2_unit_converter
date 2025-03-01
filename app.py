import streamlit as st
from forex_python.converter import CurrencyRates
import google.generativeai as genai

st.markdown("""
    <style>
    .main {
        background-color: #E3F2FD;
        color: #0D47A1;
        padding: 20px;
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #1565C0;
    }
    .stButton>button {
        background-color: #1976D2;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0D47A1;
    }
    .sidebar .sidebar-content {
        background-color: #0D47A1;
        color: #FFFFFF;
    }
    .footer {
        text-align: center;
        padding: 10px;
        font-size: 0.9em;
        color: #666666;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Title with a Unique Name
st.markdown(
    """
    <h1 style='text-align: center; font-family: "Georgia", serif; font-size: 2.5em;'>
        🧙‍♂️ ConvertMagic: Your Ultimate Unit Converter 🪄
    </h1>
    """,
    unsafe_allow_html=True
)

# Sidebar for Selecting Unit Type with Emojis
unit_type = st.sidebar.radio(
    "Select Conversion Type:",
    [
        "📏 Length Converter",
        "⚖ Weight Converter",
        "🌡 Temperature Converter",
        "🧴 Volume Converter",
        "⏰ Time Converter",
        "📐 Area Converter",
        "💵 Currency Converter",
        "💾 Data Storage Converter",
        "🚗 Speed Converter",
        "📊 Pressure Converter",
        "⚡ Energy Converter",
        "🤖 Chatbot"  # Added Chatbot option
    ]
)

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Initialize session state for chatbot
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Reusable Conversion Function
def convert_units(amount, from_unit, to_unit, unit_dict):
    return amount * (unit_dict[to_unit] / unit_dict[from_unit])

# Configure Gemini AI
try:
    genai.configure(api_key="AIzaSyBQR4jToPMN-s4B_5_VLCREa8Zwm_Z2pN8") 
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    print(f"Error configuring Gemini AI: {str(e)}")

# Function to chat with Gemini
def chat_with_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Chatbot Section
if unit_type == "🤖 Chatbot":
    st.markdown("### 🤖 Chat with Gemini AI")
    
    # Input for user prompt
    user_prompt = st.text_input("Enter your message:")
    
    if st.button("Send"):
        if user_prompt:
            # Get response from Gemini
            response = chat_with_gemini(user_prompt)
            
            # Save to chat history
            st.session_state['chat_history'].append(f"You: {user_prompt}")
            st.session_state['chat_history'].append(f"Gemini: {response}")
    
    # Display chat history
    if st.session_state['chat_history']:
        st.markdown("### Chat History")
        for message in st.session_state['chat_history']:
            st.write(message)

# Length Converter
elif unit_type == "📏 Length Converter":
    st.markdown("<h2>📏 Length Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of length such as kilometers, meters, centimeters, and more.")

    length_units = {
        "Kilometre": 1000,
        "Metre": 1,
        "Centimetre": 0.01,
        "Millimetre": 0.001,
        "Micrometre": 0.000001,
        "Nanometre": 0.000000001,
        "Mile": 1609.34,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254,
        "Nautical Mile": 1852
    }

    amount = st.number_input("Enter length:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Length):", list(length_units.keys()))
    to_unit = st.selectbox("To (Length):", list(length_units.keys()))

    if st.button("Convert Length"):
        result = convert_units(amount, from_unit, to_unit, length_units)
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Weight Converter
elif unit_type == "⚖ Weight Converter":
    st.markdown("<h2>⚖ Weight Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of weight such as kilograms, grams, pounds, and ounces.")

    weight_units = {
        "Kilogram": 1,
        "Gram": 0.001,
        "Pound": 0.453592,
        "Ounce": 0.0283495
    }

    amount = st.number_input("Enter weight:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Weight):", list(weight_units.keys()))
    to_unit = st.selectbox("To (Weight):", list(weight_units.keys()))

    if st.button("Convert Weight"):
        result = convert_units(amount, from_unit, to_unit, weight_units)
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Temperature Converter
elif unit_type == "🌡 Temperature Converter":
    st.markdown("<h2>🌡 Temperature Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of temperature such as Celsius, Fahrenheit, and Kelvin.")

    temperature_formulas = {
        ("Celsius", "Fahrenheit"): lambda x: (x * 9/5) + 32,
        ("Celsius", "Kelvin"): lambda x: x + 273.15,
        ("Fahrenheit", "Celsius"): lambda x: (x - 32) * 5/9,
        ("Fahrenheit", "Kelvin"): lambda x: (x - 32) * 5/9 + 273.15,
        ("Kelvin", "Celsius"): lambda x: x - 273.15,
        ("Kelvin", "Fahrenheit"): lambda x: (x - 273.15) * 9/5 + 32,
    }

    amount = st.number_input("Enter temperature:", format="%.2f")
    from_unit = st.selectbox("From (Temperature):", ["Celsius", "Fahrenheit", "Kelvin"])
    to_unit = st.selectbox("To (Temperature):", ["Celsius", "Fahrenheit", "Kelvin"])

    if st.button("Convert Temperature"):
        if from_unit == to_unit:
            result = amount
        else:
            result = temperature_formulas[(from_unit, to_unit)](amount)
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Volume Converter
elif unit_type == "🧴 Volume Converter":
    st.markdown("<h2>🧴 Volume Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of volume such as liters, milliliters, gallons, and more.")

    volume_units = {
        "Litre": 1,
        "Millilitre": 0.001,
        "Gallon": 3.78541,
        "Quart": 0.946353,
        "Pint": 0.473176,
        "Cup": 0.24,
        "Fluid Ounce": 0.0295735
    }

    amount = st.number_input("Enter volume:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Volume):", list(volume_units.keys()))
    to_unit = st.selectbox("To (Volume):", list(volume_units.keys()))

    if st.button("Convert Volume"):
        result = convert_units(amount, from_unit, to_unit, volume_units)
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Time Converter
elif unit_type == "⏰ Time Converter":
    st.markdown("<h2>⏰ Time Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of time such as seconds, minutes, hours, days, and more.")

    time_units = {
        "Second": 1,
        "Minute": 60,
        "Hour": 3600,
        "Day": 86400,
        "Week": 604800,
        "Month": 2628000,
        "Year": 31536000
    }

    amount = st.number_input("Enter time:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Time):", list(time_units.keys()))
    to_unit = st.selectbox("To (Time):", list(time_units.keys()))

    if st.button("Convert Time"):
        result = convert_units(amount, from_unit, to_unit, time_units)
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Area Converter
elif unit_type == "📐 Area Converter":
    st.markdown("<h2>📐 Area Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of area such as square meters, square kilometers, square feet, and more.")

    area_units = {
        "Square Metre": 1,
        "Square Kilometre": 1000000,
        "Square Foot": 0.092903,
        "Acre": 4046.86,
        "Hectare": 10000
    }

    amount = st.number_input("Enter area:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Area):", list(area_units.keys()))
    to_unit = st.selectbox("To (Area):", list(area_units.keys()))

    if st.button("Convert Area"):
        result = convert_units(amount, from_unit, to_unit, area_units)
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Currency Converter
elif unit_type == "💵 Currency Converter":
    st.markdown("<h2>💵 Currency Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different currencies using real-time exchange rates.")

    c = CurrencyRates()
    currencies = ["USD", "EUR", "GBP", "JPY", "INR", "AUD", "CAD", "CHF", "CNY", "NZD"]
    amount = st.number_input("Enter amount:", min_value=0.0, format="%.2f")
    from_currency = st.selectbox("From (Currency):", currencies)
    to_currency = st.selectbox("To (Currency):", currencies)

    if st.button("Convert Currency"):
        try:
            result = c.convert(from_currency, to_currency, amount)
            st.success(f"{amount} {from_currency} = {result:.4f} {to_currency}")
            st.session_state['history'].append(f"{amount} {from_currency} = {result:.4f} {to_currency}")
        except Exception as e:
            st.error(f"Error: {str(e)}. Please check your internet connection or try again later.")

# Data Storage Converter
elif unit_type == "💾 Data Storage Converter":
    st.markdown("<h2>💾 Data Storage Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of data storage such as bytes, kilobytes, megabytes, and more.")

    data_units = {
        "Byte": 1,
        "Kilobyte": 1024,
        "Megabyte": 1024**2,
        "Gigabyte": 1024**3,
        "Terabyte": 1024**4,
        "Petabyte": 1024**5
    }

    amount = st.number_input("Enter data size:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Data Storage):", list(data_units.keys()))
    to_unit = st.selectbox("To (Data Storage):", list(data_units.keys()))

    if st.button("Convert Data Storage"):
        result = convert_units(amount, from_unit, to_unit, data_units)
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Speed Converter
elif unit_type == "🚗 Speed Converter":
    st.markdown("<h2>🚗 Speed Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of speed such as kilometers per hour, miles per hour, and meters per second.")

    speed_units = {
        "Kilometre per hour": 1,
        "Metre per second": 0.277778,
        "Mile per hour": 1.60934,
        "Foot per second": 0.3048
    }

    amount = st.number_input("Enter speed:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Speed):", list(speed_units.keys()))
    to_unit = st.selectbox("To (Speed):", list(speed_units.keys()))

    if st.button("Convert Speed"):
        result = convert_units(amount, from_unit, to_unit, speed_units)
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Pressure Converter
elif unit_type == "📊 Pressure Converter":
    st.markdown("<h2>📊 Pressure Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of pressure such as Pascal, Bar, PSI, and more.")

    pressure_units = {
        "Pascal": 1,
        "Bar": 100000,
        "PSI": 6894.76,
        "Atmosphere": 101325
    }

    amount = st.number_input("Enter pressure:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Pressure):", list(pressure_units.keys()))
    to_unit = st.selectbox("To (Pressure):", list(pressure_units.keys()))

    if st.button("Convert Pressure"):
        result = convert_units(amount, from_unit, to_unit, pressure_units)
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Energy Converter
elif unit_type == "⚡ Energy Converter":
    st.markdown("<h2>⚡ Energy Converter</h2>", unsafe_allow_html=True)
    st.write("Convert between different units of energy such as Joules, Calories, and Kilowatt-hours.")

    energy_units = {
        "Joule": 1,
        "Calorie": 4.184,
        "Kilowatt-hour": 3600000,
        "Electronvolt": 1.60218e-19
    }

    amount = st.number_input("Enter energy:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From (Energy):", list(energy_units.keys()))
    to_unit = st.selectbox("To (Energy):", list(energy_units.keys()))

    if st.button("Convert Energy"):
        result = convert_units(amount, from_unit, to_unit, energy_units)
        st.success(f"{amount} {from_unit} = {result:.4f} {to_unit}")
        st.session_state['history'].append(f"{amount} {from_unit} = {result:.4f} {to_unit}")

# Display History
if st.session_state['history']:
    st.sidebar.markdown("### Conversion History")
    for item in st.session_state['history']:
        st.sidebar.write(item)

# Save and Load History
if st.sidebar.button("Save History to File"):
    with open("conversion_history.txt", "w") as file:
        for item in st.session_state['history']:
            file.write(item + "\n")
    st.sidebar.success("History saved to conversion_history.txt")

if st.sidebar.button("Load History from File"):
    try:
        with open("conversion_history.txt", "r") as file:
            st.session_state['history'] = file.read().splitlines()
        st.sidebar.success("History loaded from conversion_history.txt")
    except FileNotFoundError:
        st.sidebar.error("No history file found.")

# Clear History Button
if st.sidebar.button("Clear History"):
    st.session_state['history'] = []

# Reset Button
if st.button("Reset"):
    st.session_state['history'] = []  # Clear history
    st.rerun()  # Refresh the app

# Footer with Amazing Text and Styling
st.markdown("<div class='footer'>Made with ❤ by <strong>Rani Abdul Sattar</strong> | Powered by Streamlit & Python</div>", unsafe_allow_html=True)