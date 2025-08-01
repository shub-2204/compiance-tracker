import streamlit as st
from conn import create_connection
from history import history_page    

def inbox():
    # Set page config
    st.set_page_config(page_title="Compliance Tracker - Inbox", layout="wide")

    # Check if user is logged in
    if not st.session_state.get("logged_in", False):
        st.error("❌ Please log in to access the inbox.")
        return
    # Render history page if history_view is True
    if st.session_state.history_view and st.session_state.selected_inspectionid:
        history_page(st.session_state.selected_inspectionid)
        return
    
    # Initialize session state for tab
    if "tab" not in st.session_state:
        st.session_state.tab = "📥 Inbox"

    # Sidebar Navigation
    st.sidebar.title("📋 Menu")
    st.session_state.tab = st.sidebar.radio("Go to", ["📥 Inbox",  "✅ Search Compliance"], key="sidebar_tab")

    # Custom CSS Styling
    st.markdown("""
        <style>
            .main-title {
                top: 200px;
                font-size: 48px;
                color: #003366;
                text-align: Left;
                font-weight: bold;
            }
            .sub-title {
                font-size: 24px;
                color: #555;
                text-align: center;
                margin-bottom: 30px;
            }
                /* Global button styling (for all st.buttons) */
            button[kind="secondary"] {
                background-color: #003366 !important;
                color: white !important;
                font-weight: bold !important;
                padding: 10px 24px !important;
                border-radius: 6px !important;
                border: none !important;
            }

            button[kind="secondary"]:hover {
                background-color: #005599 !important;
            }
            /* Inbox-specific styles */    
                .inbox-row {
                border-bottom: 3px solid #eee;
                padding: 12px;
                transition: background-color 0.2s ease;
                cursor: pointer;
                font-size: 1.8em;
            }
            .inbox-row:hover {
                background-color: #f3f7fa;
            }
            .inbox-id {
                font-weight: 800;
                color: #005288;
                size: 1.8em;
            }            
            .inbox-subject {
                font-weight: 700;
                color: #003366;
                font-size: 1.5em;
            }
            .inbox-desc {
                font-weight: 700;
                color: #003366;
                font-size: 1.3em;
            }
            .inbox-date {
                font-size: 1.4em;
                color: #003366;
            }
            .inbox-details {
                margin-top: 8px;
                font-size: 1.1em;
                color: #333;
                line-height: 1.6;
                font-weight: normal;
                background-color: #f9f9f9;      
                padding: 12px;
                border-radius: 6px;
            }
            /* Expander summary font size */
            div[data-testid='stExpander'] details summary p {
                font-size: 1.2rem;
            }
           
        </style>
    """, unsafe_allow_html=True)

    # Greeting
    st.markdown(
        """
        <link 
            rel="stylesheet" 
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
        >
        """,
        unsafe_allow_html=True
    )
    role = st.session_state.get("role", "").strip()
    display_role = role.upper() if role else "GUEST"
    greeting_text = f"👋 Hello, {display_role}"
    st.markdown(
        f"""<div style='color: orange; font-weight: bold; font-size: 20px;'>
        {greeting_text}</div>""",
        unsafe_allow_html=True
    )

    # Page Title
    st.markdown("<div class='main-title'>WESTERN RAILWAY</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Compliance Inbox</div>", unsafe_allow_html=True)

    # Logout Button in Sidebar
    if st.sidebar.button("🚪 Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.desig_code = ""
        st.session_state.tab = "🏠 Home"
        st.rerun()

    # Tab logic
    if st.session_state.tab == "📥 Inbox":
        st.subheader("📥 Compliance Inbox")
        username = st.session_state.get("username", "")
        desig_code = st.session_state.get("desig_code", "")

        if not username or not desig_code:
            st.error("❌ User information missing. Please log in again.")
            return

        # Fetch data from compliance_notes
        conn = create_connection()
        if conn is None:
            st.error("❌ Failed to connect to the database. Please try again.")
            return

        cursor = None
        try:
            cursor = conn.cursor()
            query = """
                SELECT inspectionid, note_date, compliance_date, subject, details, last_marked_by
                FROM compliance
                WHERE marked_to = :desig_code
                ORDER BY note_date DESC
            """
            cursor.execute(query, {"desig_code": desig_code})
            records = cursor.fetchall()

            if not records:
                st.info("ℹ️ No compliance records found for you.")
                return
            #st.subheader("📥 Compliance Inbox")

            # Header
            st.markdown("""
            <style>
            
            """, unsafe_allow_html=True)
            
            
            st.markdown(f"<style>div[data-testid='stExpander'] details summary p{{font-size: 1.2rem;}}</style>", unsafe_allow_html=True)

            # 📥 Title
            #st.subheader("📬 Compliance Inbox")

            # 📋 Inbox-style list
            for record in records:
                inspectionid, note_date, compliance_date, subject, details, last_marked_by = record
                expander_title = (
                                    f"{inspectionid} | {subject} | "
                                    f"🗓️ {note_date.strftime('%Y-%m-%d')} | "
                                    f"📅 {compliance_date.strftime('%Y-%m-%d')} | "
                                    f"👤 From: {last_marked_by}"
                                )
               
                with st.container():
                       
                    with st.expander(expander_title):
                            st.markdown(f"""
                                <div class='inbox-container'>
                                <div class='inbox-id'>{inspectionid}</div>
                                <hr style="border: 1px solid #ccc; margin: 12px 0;">
                                <div class='inbox-subject'>SUBJECT: {subject}</div>
                                <hr style="border: 1px solid #ccc; margin: 12px 0;">
                                <div class='inbox-date'>🗓️ InspectionNote/MOM Date: {note_date.strftime('%Y-%m-%d')} | Compliance: {compliance_date.strftime('%Y-%m-%d')}</div>
                                 <hr style="border: 1px solid #ccc; margin: 12px 0;">
                                <div class='inbox-desc'>📝 DESCRPTION IN DETAIL</div>
                                <hr style="border: 1px solid #ccc; margin: 6px 0;">
                                <div class='inbox-details'>{details}</div>
                            </div>
                        """, unsafe_allow_html=True)
                            st.markdown("""
                                            <style>
                                                div[data-testid="stButton"] > button {
                                                    background-color: #003366 !important;
                                                    color: white !important;
                                                    font-weight: bold !important;
                                                    padding: 8px 20px !important;
                                                    border-radius: 6px !important;
                                                    border: none !important;
                                                }
                                                div[data-testid="stButton"] > button:hover {
                                                    background-color: #005599 !important;
                                                }
                                            </style>
                                        """, unsafe_allow_html=True)
                            if st.session_state.desig_code == 25:
                                if st.button("CHECK COMPLIANCE", key=f"view_history_{inspectionid}", help="Click to view history and add comments"):
                                    st.session_state.history_view = True
                                    st.session_state.selected_inspectionid = inspectionid
                                    st.rerun()
                            else:
                                if st.button("GIVE COMPLIANCE", key=f"view_history_{inspectionid}", help="Click to view history and add comments"):
                                    st.session_state.history_view = True
                                    st.session_state.selected_inspectionid = inspectionid
                                    st.rerun()
                            st.markdown("</div>", unsafe_allow_html=True)  # Close the flex container
        except Exception as e:
            st.error(f"❌ Database Error: {str(e)}")
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    elif st.session_state.tab == "🏠 Home":
        st.subheader("🏠 Home")
        st.info("🛠️ Redirecting to compliance submission page...")
        st.session_state.tab = "🏠 Home"
        st.rerun()

    elif st.session_state.tab == "📌 Sent Compliance":
        st.subheader("📌 Current Compliance Entries")
        st.info("🛠️ Display current (open) compliance issues here.")

   