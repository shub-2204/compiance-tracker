import streamlit as st
from conn import create_connection
from streamlit_modal import Modal   
import time # For a small delay if needed for visual feedback

import streamlit.components.v1 as components
def get_user_authority(desig_code):
    """Map desig_code to authority name."""
    authority_map = {
        1: "PRINCIPAL CHIEF PERSONNEL OFFICER - PCPO",
        2: "PRINCIPAL CHIEF MEDICAL OFFICER - PCMD",
        3: "PRINCIPAL CHIEF MECHANICAL ENGINEER - PCME",
        4: "PRINCIPAL CHIEF ELECTRICAL ENGINEER - PCEE",
        5: "PRINCIPAL CHIEF SIGNAL AND TELECOM ENGINEER - PCSTE",
        6: "PRINCIPAL CHIEF ENGINEER - PCE",
        7: "PRINCIPAL FINANCIAL ADVISER - PFA",
        8: "PRINCIPAL CHIEF COMMERCIAL MANAGER - PCCM",
        9: "PRINCIPAL CHIEF MATERIAL MANAGER - PCMM",
        10: "PRINCIPAL CHIEF OPERATING MANAGER - PCOM",
        11: "DIVISIONAL RAILWAY MANAGER, MUMBAI - DRMBCT",
        12: "DIVISIONAL RAILWAY MANAGER, ADI - DRMADI",
        13: "DIVISIONAL RAILWAY MANAGER, RTM - DRMRTM",
        14: "DIVISIONAL RAILWAY MANAGER, BVP - DRMBVP",
        15: "DIVISIONAL RAILWAY MANAGER, BRC - DRMBRC",
        16: "DIVISIONAL RAILWAY MANAGER, RJT - DRMRJT",
        17: "CHIEF PUBLIC RELATION OFFICER - CPRO",
        18: "CHIEF ACCOUNTS OFFICER - CONST - CAO/C",
        19: "CHIEF ACCOUNTS OFFICER - RSP - CAO/RSP",
        20: "CHIEF ACCOUNTS OFFICER - ADI CONST - CAO/C/ADI",
        21: "PRINCIPAL CHIEF SECURITY OFFICER - PCSO",  
        22: "SENIOR DEPUTY GENERAL MANAGER - SDGM",
        23: "DEPUTY GENERAL MANAGER - DGMG",
        25: "GENERAL MANAGER - GM"
    }
    return authority_map.get(int(desig_code), None)
def history_page(inspectionid):
    #st.session_state[f"show_confirm_{inspectionid}"]= False
    """Display history for a specific inspectionid and allow adding comments."""
    # Custom CSS for history section (combined with inbox CSS)
    print("Session state desig_code is", st.session_state.desig_code)
    st.markdown(
        """
        <link 
            rel="stylesheet" 
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
        >
        <style>
            .main-title {
                font-size: 48px;
                color: #003366;
                text-align: center;
                font-weight: bold;
            }
            .sub-title {
                font-size: 24px;
                color: #555;
                text-align: center;
                margin-bottom: 30px;
            }
            .inbox-container {
                max-width: 1200px;
                margin: 0 auto;
                word-wrap: break-word;
            }
            .history-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            .history-table th, .history-table td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
                min-width: 100px; /* Ensure minimum width for cells */
                word-break: break-word; /* Handle long text */
            }
            .history-table th {
                background-color: #f2f2f2;
                font-weight: bold;
                font-size: 28px;
                color: #003366;
            }
            .history-table td {
                font-size: 18px;
                color: #333;
            }
            .comment-box {
                margin-top: 20px;
                padding: 24px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
                position: relative;
            }
            .comment-header {
                font-weight: 700;
                color: #003366;
                font-size: 28px;
                margin-bottom: 16px;
            }
            .stButton > button {
                background: linear-gradient(45deg, #004080, #00cc99);
                color: white;
                font-weight: bold;
                font-size: 18px;
                padding: 10px 24px;
                border-radius: 12px;
                border: none;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                background: linear-gradient(45deg, #ff6200, #ffaa00);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
                transform: scale(1.05);
            }
            .button-container {
                position: absolute;
                bottom: 10px;
                right: 10px;
            }
            div[data-testid="stExpander"] {
                width: 100%;
                min-height: 150px;
                margin-bottom: 20px;
                padding: 16px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            div[data-testid="stExpanderDetails"] {
                padding: 24px !important;
                background-color: white !important;
                border-left: 1px solid #e1e1e1 !important;
                border-right: 1px solid #e1e1e1 !important;
                border-bottom: 1px solid #e1e1e1 !important;
                border-radius: 0 0 4px 4px !important;
                margin-top: -8px !important;
                margin-bottom: 12px !important;
                min-height: 200px;
                position: relative;
            }
            .inbox-id {
                font-weight: 800;
                color: #005288;
                font-size: 28px;
            }
            .inbox-subject {
                font-weight: 700;
                color: #003366;
                font-size: 28px;
                margin-top: 12px;
            }
            .inbox-desc {
                font-weight: 700;
                color: #003366;
                font-size: 24px;
                margin-top: 12px;
            }
            .inbox-date {
                font-size: 24px;
                color: #888;
                margin-top: 12px;
            }
            .inbox-details {
                margin-top: 8px;
                font-size: 18px;
                color: #333;
                line-height: 1.6;
                font-weight: normal;
            }
            div[data-testid="stExpanderDetails"] .stButton > button {
                background: linear-gradient(45deg, #004080, #00cc99);
                color: white;
                font-weight: bold;
                font-size: 18px;
                padding: 10px 24px;
                border-radius: 12px;
                border: none;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            }
            div[data-testid="stExpanderDetails"] .stButton > button:hover {
                background: linear-gradient(45deg, #ff6200, #ffaa00);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
                transform: scale(1.05);
            }
            @media (max-width: 768px) {
                .main-title {
                    font-size: 36px;
                }
                .sub-title {
                    font-size: 20px;
                }
                .history-table th {
                    font-size: 22px;
                }
                .history-table td {
                    font-size: 16px;
                    padding: 8px;
                }
                .comment-header {
                    font-size: 22px;
                }
                .inbox-id, .inbox-subject, .inbox-desc {
                    font-size: 22px;
                }
                .inbox-date, .inbox-details {
                    font-size: 18px;
                }
                .inbox-container {
                    max-width: 100%;
                }
                .stButton > button {
                    font-size: 16px;
                    padding: 8px 20px;
                }
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(f"<style>div[data-testid='stExpander'] details summary p{{font-size: 1.2rem;}}</style>", unsafe_allow_html=True)

    # Greeting
    role = st.session_state.get("role", "").strip()
    #
    # authority = get_user_authority(st.session_state.desig_code)
    display_role = role.upper() if role else "GUEST"
    st.markdown(
        f"""<div style='color: orange; font-weight: bold; font-size: 20px;'>
        👋 Hello, {display_role}</div>""",
        unsafe_allow_html=True
    )

    # Page Title
    st.markdown("<div class='main-title'>Western Railways</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Compliance History</div>", unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("📋 Menu")
    if st.sidebar.button("🚪 Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.desig_code = ""
        st.session_state.history_view = False
        st.session_state.selected_inspectionid = None
        st.rerun()
    if st.sidebar.button("📥 Back to Inbox", key=f"back_to_inbox_{inspectionid}"):
        st.session_state.history_view = False
        st.session_state.selected_inspectionid = None
        st.session_state[f"show_confirm_{inspectionid}"] = False
        st.rerun()

    # Content
    with st.container():
        st.markdown(f"<div class='inbox-container'>", unsafe_allow_html=True)
        st.subheader(f"📜 History for Inspection ID: {inspectionid}")

        # Fetch history from compliance_hist
        conn = create_connection()
        if conn is None:
            st.error("❌ Failed to connect to the database.")
            return

        cursor = None
        try:
            cursor = conn.cursor()
            query = """
                SELECT  history_id, comment_notes, record_timestamp, comment_by, current_status
                FROM compliance_hist
                WHERE inspectionid = :inspectionid
                ORDER BY record_timestamp DESC
            """
            cursor.execute(query, {"inspectionid": inspectionid})
            history_records = cursor.fetchall()
            print("Fetched history records:", history_records)  # Debugging line
           #print("executed query:", query)    
            if not history_records:
                st.info("ℹ️ No history records found for this inspection ID.")
            else:
                # Display history in a table
                st.markdown("""
                    <table class='history-table'>
                        <tr>
                            <th>From User</th>
                            <th>Current Status</th>
                            <th>Date-Recieved</th>
                            <th>Date-Action taken</th>
                            <th>Comments</th>
                        </tr>
                    """, unsafe_allow_html=True)
                for record in history_records:
                    insp_id, comment,record_timestamp, comment_by, Status = record
                    st.markdown(
                        f"""<table class='history-table'>
                        <tr>
                            <td>{insp_id}</td>
                            <td>{Status if Status else 'N/A'}</td>
                            <td>{record_timestamp.strftime('%Y-%m-%d')}</td>
                            <td>{get_user_authority(comment_by)}</td>
                            <td>{comment}</td>
                        </tr>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown("</table>", unsafe_allow_html=True)

            # Comment input form
            st.markdown("<div class='comment-box'>", unsafe_allow_html=True)
            st.markdown("<div class='comment-header'>Add New Comment</div>", unsafe_allow_html=True)
            comment = st.text_area("Comment", placeholder="Enter your comment here", key=f"comment_{inspectionid}")
         
            st.markdown("<div class='comment-header'>Status</div>", unsafe_allow_html=True)
            if st.session_state.desig_code == 25 :
              comment_type = st.selectbox("Status", ["Please Select-","CLOSED","RECOMPLIANCE"], key=f"status_{inspectionid}")
            else:
              comment_type = st.selectbox("Status", ["SELECT FROM DROPDOWN","PARTIAL COMPLIANCE","FULL COMPLIANCE","NON COMPLIANCE"], key=f"status_{inspectionid}")

            st.markdown("<div class='button-container'>", unsafe_allow_html=True)
            # Submit button with confirmation
            if st.button("Submit Comment", key=f"submit_comment_button_{inspectionid}"):
                if comment_type == "Please Select-" or comment_type == "SELECT FROM DROPDOWN":
                    st.error("❌ Please select a valid status.")
                if not comment.strip():
                            st.error("❌ Comment cannot be empty.")
                elif len(comment.strip()) > 4000:
                            st.error("❌ Comment too long.")
                else:
                    st.session_state[f"show_confirm_{inspectionid}"] = True
                 

            if st.session_state.get(f"show_confirm_{inspectionid}", False):
                with st.expander("⚠️ Confirm Submission", expanded=True):
                    st.write("📝 Are you sure you want to submit this comment?")
                    col1, col2 = st.columns(2)
                    confirm_clicked = cancel_clicked = False

                    with col1:
                        confirm_clicked = st.button("✅ Yes, Submit", key=f"confirm_submit_{inspectionid}")
                    with col2:
                        cancel_clicked = st.button("❌ Cancel", key=f"cancel_submit_{inspectionid}")

                    if confirm_clicked:

                            try:
                                cursor.execute("""
                                    INSERT INTO compliance_hist (history_id, inspectionid, comment_notes, current_status, comment_by,record_timestamp)
                                    VALUES (compliance_hist_seq.NEXTVAL, :inspectionid, :comment_notes, :current_status, :comment_by, SYSTIMESTAMP)
                                """, {
                                    "inspectionid": inspectionid,
                                    "comment_notes": comment,
                                    "current_status": comment_type,
                                    "comment_by": st.session_state.desig_code
                                
                                })
                            except Exception as e:
                                st.error(f"❌ Database Error1: {str(e)}")
                            try:
                                if st.session_state.desig_code != 25:      
                             
                                    # Update compliance table for non-GM users
                                    cursor.execute("""
                                        UPDATE compliance 
                                        SET authority = :authority,
                                            marked_to = '25',
                                            last_marked_by = :last_marked_by,
                                            current_status = :current_status,
                                            record_timestamp = SYSTIMESTAMP
                                        WHERE inspectionid = :inspectionid
                                    """, {
                                        "authority":get_user_authority('25'), 
                                        "last_marked_by": st.session_state.desig_code,
                                        "current_status": comment_type,
                                        "inspectionid": inspectionid
                                    })
                                else:
                                   
                                    cursor.execute("""
                                           select last_marked_by from compliance where inspectionid = :inspectionid order by record_timestamp desc
                                            """, {"inspectionid": inspectionid}) 
                                    last_marked_by = cursor.fetchone()
                                    if last_marked_by:
                                        last_marked_by = last_marked_by[0]
                                        authority_curr = get_user_authority(last_marked_by)                         
                                    print(last_marked_by, "last marked by")
                                    cursor.execute("""
                                        UPDATE compliance 
                                        SET authority = :authority_curr, 
                                            marked_to = :last_marked_by,
                                            last_marked_by = :last_marked_by,
                                            current_status = :current_status,
                                            record_timestamp = SYSTIMESTAMP
                                        WHERE inspectionid = :inspectionid
                                    """, {
                                        "inspectionid": inspectionid,
                                        "last_marked_by": last_marked_by,
                                        "current_status": comment_type,
                                        "authority_curr": authority_curr
                                    })
                                # Commit the changes
                                conn.commit()
                                st.success("✅ Comment added successfully.")
                                time.sleep(1)
                                st.session_state[f"show_confirm_{inspectionid}"] = False
                                st.session_state.history_view = False  # Redirect to inbox
                                st.session_state.selected_inspectionid = None
                         
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Database Error2: {str(e)}")

                    if cancel_clicked:
                        st.session_state[f"show_confirm_{inspectionid}"] = False
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown(
                            "<div style='text-align:center; color:#d97706; font-weight:bold; font-size:20px;'>⚠️ Submission cancelled.</div>",
                            unsafe_allow_html=True
                        )
                        time.sleep(1)
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Database Error0: {str(e)}")
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
        st.markdown("</div>", unsafe_allow_html=True)
