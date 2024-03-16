import streamlit as st
def show():
    # Initialize device_num
    if "device_num" not in st.session_state:
        st.session_state["device_num"] = -1

    # Dasboard of each device
    def deviceDashboard(index):
        title = "Device "+ str(index + 1)+" dashboard"
        st.title(title)
        if st.button("back"):
            st.session_state["device_num"] = -1
            
            
            
    # No device selected show main page else show the dasboard of each device
    if st.session_state.get("device_num") == -1:  
        st.title("Devices")

        num_columns = 3
        columns = st.columns(num_columns)

        # Data
        devices = [
            {'Name': 'Device 1', 'Location': 'Telemcen'},
            {'Name': 'Device 2', 'Location': 'Blida'},
            {'Name': 'Device 3', 'Location': 'Algiers'},
            {'Name': 'Device 4', 'Location': 'Oran'},
            {'Name': 'Device 5', 'Location': 'Medea'}
        ]

        # Iterate over devices
        for i, device in enumerate(devices):
            col_index = i % num_columns
            container = columns[col_index].container()
            
            # Write device information to the container
            container.title(device['Name'])
            container.write(f"Location: {device['Location']}")

            # Button to show dashboard
            button_key = f"see_more_button_{device['Name']}" #giving it a speacial key
            if container.button("See dashboard", key=button_key):
                st.session_state["device_num"] = i

    else:
        deviceDashboard(st.session_state["device_num"])




    #CSS
    with open("devices_page_Style.css") as f:
        st.markdown(
            f"""
            <style>
                {f.read()}
            </style>
            """,
            unsafe_allow_html=True
        )
