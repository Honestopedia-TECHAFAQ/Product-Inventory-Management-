import streamlit as st
import pandas as pd
import requests

# Function to fetch data from Google Sheets API
def fetch_data(sheet_id):
    api_key = 'AIzaSyC1RHav3wTQqoMgx6jlcwiAbfJn_3k28UQ'
    # Fetch all data from the first sheet
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}?key={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the sheet metadata to get the sheet ID and range
            sheet_info = response.json()
            sheet_title = sheet_info['sheets'][0]['properties']['title']
            sheet_range = f"{sheet_title}"

            # Fetch data from the sheet dynamically
            data_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{sheet_range}?key={api_key}"
            data_response = requests.get(data_url)

            if data_response.status_code == 200:
                data = data_response.json().get('values', [])
                return data
            else:
                st.error(f"Error fetching data: {data_response.status_code} - {data_response.text}")
                return None
        else:
            st.error(f"Error fetching sheet info: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

# Sidebar options
page_options = ['Dashboard', 'Products', 'Settings', 'Help']

# Render sidebar
selected_page = st.sidebar.selectbox('Select Page', page_options)

# Render selected page
if selected_page == 'Dashboard':
    st.title('Dashboard')
    st.write('This is the dashboard page.')
    st.info('Navigate to the "Products" page to view and manage your data.')

elif selected_page == 'Products':
    st.title('Products')
    st.write('This is the products page.')

    # Input field for Google Sheet ID
    sheet_id = st.text_input('Enter Google Sheet ID:', value='1qq7vJyjsptOOhgGZowXJ00O6GZ6KzFHRT7D3AYwNuIY', help='Enter the ID of your Google Sheet.')
    
    if st.button('Fetch Data'):
        if sheet_id:
            with st.spinner('Fetching data...'):
                # Fetch data from Google Sheets API
                data = fetch_data(sheet_id)
                if data:
                    if len(data) > 1:
                        df = pd.DataFrame(data[1:], columns=data[0])
                        
                        # Display summary cards
                        st.subheader('Summary')
                        # Dynamically handle columns for summary metrics if they exist
                        if 'Company Name' in df.columns and 'Country' in df.columns:
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Total Companies", df['Company Name'].nunique())
                            col2.metric("Total Products", df.shape[0])
                            col3.metric("Countries Represented", df['Country'].nunique())

                        # Search and filter options
                        st.subheader('Search and Filter')
                        search_text = st.text_input('Search by text:')
                        country_filter = st.selectbox('Filter by country:', ['All'] + sorted(df['Country'].unique().tolist()) if 'Country' in df.columns else ['All'])

                        # Filter data based on search and filter inputs
                        if search_text:
                            df = df[df.apply(lambda row: search_text.lower() in row.astype(str).str.lower().to_string(), axis=1)]
                        
                        if country_filter != 'All' and 'Country' in df.columns:
                            df = df[df['Country'] == country_filter]
                        
                        # Display data table
                        st.subheader('Data Table')
                        st.dataframe(df)
                    else:
                        st.warning('No data found in the specified sheet.')
        else:
            st.warning('Please enter a Google Sheet ID.')

elif selected_page == 'Settings':
    st.title('Settings')
    st.write('This is the settings page.')
    st.info('Settings can be configured here.')

elif selected_page == 'Help':
    st.title('Help')
    st.write('This is the help page.')
    st.info('Get assistance with using this app here.')

# Add footer or additional info
st.sidebar.write("This app fetches data from Google Sheets and displays it in a user-friendly manner. Use the 'Products' page to view and filter your data.")
