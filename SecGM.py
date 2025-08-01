import os
import random
import streamlit as st
from datetime import date ,timedelta 
from pathlib import Path
from conn  import create_connection

# Directory for storing uploaded files
UPLOAD_DIR = os.path.abspath("DGM-G/uploads/files")
#Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

def loggedinSECGM(): 
            # Ensure upload directory exists
            Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
            # Set page config
            st.set_page_config(page_title="Compliance Tracker", layout="wide")

                    # Initialize session state for tab and submission
            if "tab" not in st.session_state:
                st.session_state.tab = "🏠 Home"
            if "submission_success" not in st.session_state:
                st.session_state.submission_success = False
            if "submission_data" not in st.session_state:
                st.session_state.submission_data = None

            # Add Logout Button in Sidebar
            if st.sidebar.button("🚪 Logout", key="logout_btn"):
                # Clear session state
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.role = ""
                st.session_state.desig_code = ""
                # Rerun to redirect to login screen
                st.rerun()

            # Sidebar Navigation
            st.sidebar.title("📋 Menu")
            st.session_state.tab = st.sidebar.radio("Go to", ["🏠 Home", "📌 Current Compliance", "✅ Closed Compliance"], key="sidebar_tab")

            # Custom CSS Styling
            st.markdown("""
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
                    .stButton > button {
                        background-color: #003366;
                        color: white;
                        font-weight: bold;
                        padding: 8px 20px;
                        border-radius: 6px;
                    }
                    .stButton > button:hover {
                        background-color: #005599;
                    }
                </style>
            """, unsafe_allow_html=True)

            #greet here
            # First add Font Awesome to your app
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
            display_role = role.upper()  if role else "GUEST" # Proper capitalization
            greeting_text = f"👋 Hello, {display_role}"
            st.markdown(f"""<div style=
                             'color: orange;font-weight: bold;font-size: 20px;'>
                             {greeting_text}</div>""",
                             unsafe_allow_html=True
                    )

            

            # Page Title
            st.markdown("<div class='main-title'>Western Railways</div>", unsafe_allow_html=True)
            st.markdown("<div class='sub-title'>Compliance Tracker</div>", unsafe_allow_html=True)

            # Tab logic
            if st.session_state.tab == "🏠 Home":
                if not st.session_state.submission_success:
                    note_type = st.selectbox("🚆 Select Inspection Note Type", [ "-- Select Note Type --",  # Placeholder option
                                                                                "INSPECTION NOTE", "MINUTES OF MEETING",],key="note_type")

                    fields = [
                        "-- Select Authority --",  # Placeholder option
                        "PRINCIPAL CHIEF PERSONNEL OFFICER - PCPO",
                        "PRINCIPAL CHIEF MEDICAL OFFICER - PCMD",
                        "PRINCIPAL CHIEF MECHANICAL ENGINEER - PCME", 
                        "PRINCIPAL CHIEF ELECTRICAL ENGINEER - PCEE",
                        "PRINCIPAL CHIEF SIGNAL AND TELECOM ENGINEER - PCSTE",
                        "PRINCIPAL CHIEF ENGINEER - PCE",
                        "PRINCIPAL FINANCIAL ADVISER - PFA",
                        "PRINCIPAL CHIEF COMMERCIAL MANAGER - PCCM",
                        "PRINCIPAL CHIEF MATERIAL MANAGER - PCMM",
                        "PRINCIPAL CHIEF OPERATING MANAGER - PCOM",
                        "DIVISIONAL RAILWAY MANAGER, MUMBAI- DRMBCT",
                        "DIVISIONAL RAILWAY MANAGER, ADI- DRMADI",
                        "DIVISIONAL RAILWAY MANAGER, RTM- DRMRTM",
                        "DIVISIONAL RAILWAY MANAGER, BVP- DRMBVP",
                        "DIVISIONAL RAILWAY MANAGER, BRC- DRMBRC",
                        "DIVISIONAL RAILWAY MANAGER, RJT- DRMBCT",
                        "CHIEF PUBLIC RELATION OFFICER- CPRO",
                        "CHIEF ACCOUNTS OFFICER - CONST- CAO/C",
                        "CHIEF ACCOUNTS OFFICER - RSP- CAO/RSP",
                        "CHIEF ACCOUNTS OFFICER -ADI CONST- CAO/C/ADI",
                        "PRINCIPAL CHIEF SECURITY OFFICER - PCSO",
                        "SENIOR DEPUTY GENERAL MANAGER - SDGM",
                        "DEPUTY GENERAL MANAGER - DGMG"
                    ]
                    selected_field = st.selectbox("📋 Select Authority", fields,key="selected_field")

                    subject = st.text_input(
                        "📑 Enter Subject", 
                        placeholder="Enter the subject of the compliance note...",
                        key="subject"
                    )


                    text_input = st.text_area(
                        "📝 Enter Compliance Details (Max 2000 words)", 
                        placeholder="Type detailed compliance notes here...",
                        height=250,
                        key="text_input"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        Note_Date = st.date_input(
                            "📅 Select Note/MOM Date",
                            value=None,  # Blank by default
                            #value=date.today(),
                            min_value=date(2000, 1, 1),
                            max_value=date.today(),
                            key="note_date"
                        )

                    with col2:
                        compliance_date = st.date_input(
                            "📅 Select Compliance Date",
                            value=None,  # Blank by default
                            min_value=date(2000, 1, 1),
                            max_value=date.today() + timedelta(days=365),  # Allow future dates up to 1 year
                            key="compliance_date"
                        )

                    uploaded_file = st.file_uploader(
                    "📎 Attach File (PDF only, max 600KB)",
                        type=["pdf"],
                        key="compliance_file")
                        
                    if st.button("Submit",key="submit_btn"):
                        word_count = len(text_input.split())
                        if word_count > 2000:
                            st.warning(f"⚠️ Too many words! You entered {word_count} words. Limit is 1000.")
                        elif selected_field == "-- Select Field --":
                            st.warning("⚠️ Please select a valid field before submitting.")     
                        elif note_type == "-- Select Note Type --":
                            st.warning("⚠️ Please select a valid n note type before submitting.")  
                        elif not subject.strip():
                            st.warning("⚠️ Please enter a valid subject.")  
                        elif uploaded_file and uploaded_file.size > 600 * 1024:  # 600KB limit
                            st.warning("⚠️ File size exceeds 600KB. Please upload a smaller PDF file.")
                        else:   
                                #Generate unique inspection note ID
                                if note_type == "INSPECTION NOTE":  
                                    inspectionid = f"IN{date.today().strftime('%Y%m%d')}{random.randint(100, 999)}"
                                elif note_type == "MINUTES OF MEETING":
                                    inspectionid = f"MOM{date.today().strftime('%Y%m%d')}{random.randint(10, 99)}"
                                #create connection to Oracle database
                                conn = create_connection()
                                if conn is None:
                                    st.error("❌ Failed to connect to the database. Please try again.")
                                else:
                                    cursor = None
                                    try:
                                        cursor=conn.cursor()
                                        #save uploaded file to disk if uploaded
                                        if uploaded_file is not None:
                                            file_name = uploaded_file.name
                                            safe_file_name = f"{inspectionid}_{file_name}"
                                            file_path = os.path.join(UPLOAD_DIR, safe_file_name)
                                            print("File path is", file_path)
                                            try:
                                                with open(file_path, "wb") as f:
                                                    f.write(uploaded_file.read())
                                                st.success(f"✅ File saved to: {file_path}")
                                            except Exception as e:
                                                st.error(f"❌ Failed to save file: {e}")
                                        else:
                                            safe_file_name = ''
                                            file_path = ''

                                        authcode = None
                                        if selected_field == "PRINCIPAL CHIEF PERSONNEL OFFICER - PCPO":
                                            authcode = 1
                                        elif selected_field == "PRINCIPAL CHIEF MEDICAL OFFICER - PCMD":
                                            authcode = 2    
                                        elif selected_field == "PRINCIPAL CHIEF MECHANICAL ENGINEER - PCME":
                                            authcode = 3    
                                        elif selected_field == "PRINCIPAL CHIEF ELECTRICAL ENGINEER - PCEE":
                                            authcode = 4
                                        elif selected_field == "PRINCIPAL CHIEF SIGNAL AND TELECOM ENGINEER - PCSTE":
                                            authcode = 5
                                        elif selected_field == "PRINCIPAL CHIEF ENGINEER - PCE":
                                            authcode = 6
                                        elif selected_field == "PRINCIPAL FINANCIAL ADVISER - PFA":             
                                            authcode = 7
                                        elif selected_field == "PRINCIPAL CHIEF COMMERCIAL MANAGER - PCCM":         
                                            authcode = 8
                                        elif selected_field == "PRINCIPAL CHIEF MATERIAL MANAGER - PCMM":
                                            authcode = 9    
                                        elif selected_field == "PRINCIPAL CHIEF OPERATING MANAGER - PCOM":
                                            authcode = 10
                                        elif selected_field == "DIVISIONAL RAILWAY MANAGER, MUMBAI- DRMBCT":
                                            authcode = 11
                                        elif selected_field == "DIVISIONAL RAILWAY MANAGER, ADI- DRMADI":
                                            authcode = 12
                                        elif selected_field == "DIVISIONAL RAILWAY MANAGER, RTM- DRMRTM":
                                            authcode = 13
                                        elif selected_field == "DIVISIONAL RAILWAY MANAGER, BVP- DRMBVP":
                                            authcode = 14
                                        elif selected_field == "DIVISIONAL RAILWAY MANAGER, BRC- DRMBRC":
                                            authcode = 15
                                        elif selected_field == "DIVISIONAL RAILWAY MANAGER, RJT- DRMBCT":
                                            authcode = 16   
                                        elif selected_field == "CHIEF PUBLIC RELATION OFFICER- CPRO":
                                            authcode = 17   
                                        elif selected_field == "CHIEF ACCOUNTS OFFICER - CONST- CAO/C":
                                            authcode = 18   
                                        elif selected_field == "CHIEF ACCOUNTS OFFICER - RSP- CAO/RSP":
                                            authcode = 19
                                        elif selected_field == "CHIEF ACCOUNTS OFFICER -ADI CONST- CAO/C/ADI":
                                            authcode = 20   
                                        elif selected_field == "PRINCIPAL CHIEF SECURITY OFFICER - PCSO":
                                            authcode = 21
                                        elif selected_field == "SENIOR DEPUTY GENERAL MANAGER - SDGM":
                                            authcode = 22
                                        elif selected_field == "DEPUTY GENERAL MANAGER - DGMG":
                                            authcode = 23       
                                            
                                            # Ensure file size is within limit
                                            #if len(file_data) > 600 * 1024:
                                            #    st.warning("⚠️ File size exceeds 600KB. Please upload a smaller PDF file.")
                                            #    return
                                        # Insert data into compliance_notes table
                                        cursor.execute("""
                                                INSERT INTO compliance (
                                                    inspectionid,note_type, authority, marked_to, subject, details, note_date, compliance_date,
                                                    created_by,last_marked_by,file_name , file_path,status
                                                ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9,:10,:11, :12,:13)
                                            """, (
                                                    inspectionid,
                                                    note_type,
                                                    selected_field,
                                                    authcode,  # Use authcode for authority
                                                    subject.strip(),
                                                    text_input.strip()[:4000],  # Truncate to fit VARCHAR2(4000)
                                                    Note_Date,
                                                    compliance_date,
                                                    st.session_state.username,
                                                    st.session_state.username,
                                                    safe_file_name,
                                                    file_path,
                                                    'OPEN'  # Default status
                                                    'SECGM'


                                            ))
                                        conn.commit()  # Commit the transaction
                                        # Set submission data for dialog
                                      #  print("Submission data is", inspectionid, note_type, selected_field, subject, word_count, Note_Date, compliance_date)
                                        st.session_state.submission_data = {
                                            "inspectionid": inspectionid,
                                            "note_type": note_type,
                                            "authority": selected_field,
                                            "subject": subject,
                                            "word_count": word_count,
                                            "note_date": Note_Date,
                                            "compliance_date": compliance_date,
                                            "created_by": st.session_state.username
                                        }
                                        st.session_state.submission_success = True
                                        st.rerun()  # Rerun to show success message
                                        # Display summary in dialog
                                    except Exception as e:
                                        st.error(f"❌ Database Error: {str(e)}")
                                        if file_path and os.path.exists(file_path):
                                            os.remove(file_path)
                                    finally:
                                        cursor.close()
                                        conn.close()

                else:
                   #  st.session_state.submission_success:                        
                #if st.session_state.get('submission_success', False):
                        with st.container():
                            st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
                            st.success("✅ Submission Successful! Data and file saved.")
                            st.markdown("---")
                            st.subheader("🔎 Summary")
                            data = st.session_state.submission_data
                            st.write(f"- **Inspection ID:** {data['inspectionid']}")
                            st.write(f"- **Note Type:** {data['note_type']}")
                            st.write(f"- **Authority:** {data['authority']}")
                            st.write(f"- **Subject:** {data['subject']}")
                            st.write(f"- **Details Length:** {data['word_count']} words")
                            st.write(f"- **Note Date:** {data['note_date'].strftime('%Y-%m-%d')}")
                            st.write(f"- **Compliance Date:** {data['compliance_date'].strftime('%Y-%m-%d')}")
                            st.write(f"- **Created By:** {data['created_by']}")
                            
                            if st.button("OK", key="ok_btn"):
                                # Clear all relevant state
                                keys_to_clear = [
                                    "note_type", "selected_field", "subject", "text_input", 
                                    "note_date", "compliance_date", "compliance_file",
                                    "submission_success", "submission_data"
                                ]

                                
                                for key in keys_to_clear:
                                    if key in st.session_state:
                                        del st.session_state[key]
                                # Explicitly reset widget states
                               # st.session_state.note_type = "-- Select Note Type --"
                              #  st.session_state.selected_field = "-- Select Authority --"
                              #  st.session_state.subject = ""
                              #  st.session_state.text_input = ""
                              #  st.session_state.note_date = date.today()
                              #  st.session_state.compliance_date = date.today()
                             #   st.session_state.compliance_file = None
                             #   st.session_state.submission_success = False
                              #  st.session_state.submission_data = None
                             #   # Debug session state after clearing
                              #  print("Session state after reset:", dict(st.session_state))
                            #    print("Form state cleared")
                                st.session_state.tab = "🏠 Home"
                            
                                st.rerun()
                            #st.session_state.submission_success = None    
                            st.markdown("</div>", unsafe_allow_html=True)     
                                                

                    
                                #    with st.container():
                                 #       st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
                                 #       st.success("✅ Submission Successful! Data and file saved.")
                                #        st.markdown("---")
                                 #       st.subheader("🔎 Summary")
                                #        data = st.session_state.submission_data
                                 #       st.write(f"- **Inspection ID:** {data['inspectionid']}")
                                 #       st.write(f"- **Note Type:** {data['note_type']}")
                                #        st.write(f"- **Authority:** {data['authority']}")
                                #        st.write(f"- **Subject:** {data['subject']}")
                                 #       st.write(f"- **Details Length:** {data['word_count']} words")
                                #        st.write(f"- **Note Date:** {data['note_date']}")
                                 #       st.write(f"- **Compliance Date:** {data['compliance_date']}")
                                #        st.write(f"- **Created By:** {data['created_by']}")
                                #        if st.button("OK", key="ok_btn"):
                                #            # Clear form inputs and submission state
                                #            for key in ["note_type", "selected_field", "subject", "text_input", "note_date", "compliance_date", "compliance_file"]:
                                #                if key in st.session_state:
                                #                    del st.session_state[key]
                                #            st.session_state.submission_success = False
                                 #           st.session_state.submission_data = None
                                 #           st.session_state.tab = "🏠 Home"
                                 #           st.rerun()
                                 #       st.markdown("</div>", unsafe_allow_html=True)
                                #except Exception as e:
                                #                 st.error(f"❌ Database Error: {str(e)}")
                                #finally:
                                #          cursor.close()
                                #          conn.close()

            elif st.session_state.tab == "📌 Current Compliance":
                st.subheader("📌 Current Compliance Entries")
                st.info("🛠️ Display current (open) compliance issues here. You can connect this to a database or file system to show actual records.")

            elif st.session_state.tab == "✅ Closed Compliance":
                st.subheader("✅ Closed Compliance Records")
                st.success("📂 Show historical records of resolved compliance notes here.")