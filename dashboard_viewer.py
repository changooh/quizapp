import streamlit as st

def main():
    st.set_page_config(
        page_title="Dashboard Viewer",
        page_icon="📊",
        layout="wide"
    )

    # Initialize session state
    if 'show_dashboard' not in st.session_state:
        st.session_state.show_dashboard = False
    if 'iframe_url' not in st.session_state:
        st.session_state.iframe_url = ""

    # Main title
    st.title("📊 Dashboard Viewer")

    # Show input page or dashboard based on state
    if not st.session_state.show_dashboard:
        show_input_page()
    else:
        show_dashboard_page()

def show_input_page():
    """Display the input page with URL field"""
    st.markdown("### Enter Dashboard URL")
    st.markdown("Please enter the iframe URL of the dashboard you want to display:")

    # Input field for iframe URL
    iframe_url = st.text_input(
        "Dashboard iframe URL:",
        placeholder="https://example.com/dashboard/embed",
        help="Enter the complete iframe URL for your dashboard"
    )

    # Submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Show Dashboard", type="primary", use_container_width=True):
            if iframe_url.strip():
                st.session_state.iframe_url = iframe_url.strip()
                st.session_state.show_dashboard = True
                st.rerun()
            else:
                st.error("Please enter a valid URL")

    # Example URLs section
    with st.expander("📝 Example URLs"):
        st.markdown("""
        Here are some example iframe URLs you can try:
        - `https://public.tableau.com/views/WorldIndicators/GDPpercapita?:embed=yes&:display_count=yes&:showVizHome=no`
        - `https://app.powerbi.com/view?r=eyJrIjoiYWJjZGVmZ2gtaWprbC1tbm9wLXFyc3QtdXZ3eHl6MTIzNCIsInQiOiJjMGExMjM0NS02Nzg5LTEwYWItYmNkZS1lZmdoaWprbG1ub3AifQ%3D%3D`
        - `https://datastudio.google.com/embed/reporting/abc123/page/xyz789`
        """)

def show_dashboard_page():
    """Display the dashboard page with embedded iframe"""
    # Back button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back", help="Go back to URL input"):
            st.session_state.show_dashboard = False
            st.rerun()

    with col2:
        st.markdown(f"**Dashboard URL:** `{st.session_state.iframe_url}`")

    st.markdown("---")

    # Display the embedded dashboard
    try:
        # Create iframe HTML
        iframe_html = f"""
        <iframe
            src="{st.session_state.iframe_url}"
            width="100%"
            height="800"
            frameborder="0"
            style="border: 1px solid #ddd; border-radius: 5px;">
        </iframe>
        """

        # Display the iframe
        st.components.v1.html(iframe_html, height=820)

    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Please check if the URL is correct and accessible.")

        # Option to go back
        if st.button("Try Another URL"):
            st.session_state.show_dashboard = False
            st.rerun()

if __name__ == "__main__":
    main()
