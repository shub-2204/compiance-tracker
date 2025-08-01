import streamlit as st
import oracledb
from dotenv import load_dotenv
import os
import hashlib
import random
import smtplib
from email.message import EmailMessage
from SecGM import loggedinSECGM
from conn  import create_connection
from inbox import inbox

# --- Oracle Instant Client Configuration ---
oracledb.init_oracle_client(lib_dir= r"C:\Oracle\instantclient-basic-windows.x64-23.8.0.25.04\instantclient_23_8")

# Session state defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "desig_code" not in st.session_state:
    st.session_state.desig_code = ""
if "history_view" not in st.session_state:
    st.session_state.history_view = False
if "selected_inspectionid" not in st.session_state:
    st.session_state.selected_inspectionid = None
if "tab" not in st.session_state:
    st.session_state.tab = "📥 Inbox"
    # ------------------- LOGIN / SIGNUP -------------------    
def login_user(username, password):
    try:
        hashed = hash_password(password)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DESIGNATION , Desig_code FROM usermgmt WHERE username = :1 AND password = :2", (username, hashed))
      #  print(username,hashed)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
     #   print("resulet is" ,result)
        if result:
            designation = result[0]
            desig_code = result[1]
      #      print("resulet is" ,result)
            return True, designation, desig_code  # return both
        else:
            return False, "Invalid username or password", None  # message is error like 'Invalid username or password'
    
    except Exception as e:
        st.markdown(
            f"""<div style='color:yellow; font-weight:bold;'>
            ❌ Database Connection Error:<br>{e}
            </div>""",
            unsafe_allow_html=True
        )
        return None

def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()


def login_signup_screen():


    # Set page config
    st.set_page_config(page_title="Indian Railways Login", layout="centered")

    # Apply custom CSS
    st.markdown(r"""
            <style>
        .stApp {
           #background: linear-gradient(to right, #ffa833 50%, #9ae3f5 50%);
            background-image: url('https://as2.ftcdn.net/v2/jpg/06/49/21/83/1000_F_649218365_AAsj7PZAwU3LZdN1RfmMVBQeziZQxAsF.jpg');
            background-size: 105% 102%;
            animation: gradientBG 15s ease infinite;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333333;
            padding: 20px;
        }

        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

                
        .login-title {
            font-size: 32px;
            font-weight: bold;
            color: #003366;
            text-align: center;
            margin: 30px 0;
        }

        .login-button {
            background-color: #003366;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 5px;
            width: 100%;
            margin-top: 15px;
            cursor: pointer;
            font-weight: bold;
            font-size: 18px;
        }

        .login-button:hover {
            background-color: #005fa3;
        }

        .custom-checkbox {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 15px;
            margin-top: 12px;
            color: #003366;
        }
    </style>
    """, unsafe_allow_html=True)

    # Create the styled login box
    with st.container():
        st.markdown("""
        <div class="login-box">
            <div style="text-align: center;">
                <img src="https://images.seeklogo.com/logo-png/31/1/indian-railways-logo-png_seeklogo-310214.png" width="200">
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="login-title" style="color: white; text-align: center;">INDIAN RAILWAY LOGIN</div>', unsafe_allow_html=True)


        # Streamlit widgets inside styled container
        username = st.text_input("", placeholder="User ID", key="login_user", label_visibility="collapsed")
        password = st.text_input("", placeholder="Password", type="password", key="login_pass", label_visibility="collapsed")

        st.markdown("""
            <style>
            /* Try all possible label paths for checkbox */
            label, .stCheckbox label, .stCheckbox div, div[data-testid="stCheckbox"] > div {
                color: white !important;
                font-size: 16px !important;bold;
            }
            </style>
        """, unsafe_allow_html=True)
        remember = st.checkbox("Remember Me")

        login_clicked = st.button("Login", key="login_btn", use_container_width=True)

        # Login logic
        if login_clicked:
            login_result = login_user(username, password)

            if isinstance(login_result, tuple):  # successful login or invalid password
                success, designation, desig_code = login_result
               

                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = designation  # message contains role here
                    st.session_state.desig_code = desig_code
                    st.session_state.remember_me = remember
                    st.rerun()
                else:
                    st.error(f"❌ Unsuccessfull login")  # message is error like 'Invalid username or password'
            else:
                 # Database connection failure returned `None`
                 st.markdown(
                  """<div style='color:yellow; font-weight:bold;'>
                  ❌ Unable to connect to the database. Please contact IT support.
                  </div>""",
                 unsafe_allow_html=True
        )

        st.markdown('<div class="footer">© 2025 Indian Railways | IT Division</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    def send_otp_email(email, username):
        otp = str(random.randint(100000, 999999))
        st.session_state.generated_otp = otp
        st.session_state.otp_user = username


        msg = EmailMessage()
        msg.set_content(f"Your OTP to reset your password is: {otp}")
        msg["Subject"] = "Indian Railways Password Reset OTP"
        msg["From"] = "INDIAN RAILWAYS <shubhamchauhan2204@gmail.com>"
        msg["To"] = email

        try:
            load_dotenv("email.env")  # Load environment variables from .env file
            # Read credentials
            EMAIL_USER = os.getenv("EMAIL_USER")
            EMAIL_PASS = os.getenv("EMAIL_PASS")  # Make sure this is correct
          #  print(EMAIL_USER, EMAIL_PASS)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                # Load .env file
            
                smtp.login(EMAIL_USER, EMAIL_PASS)  # ← this was missing
                smtp.send_message(msg)
            return True
        except Exception as e:
            st.markdown(
            f"""<div style='color:yellow; font-weight:bold;'>
            ❌ EMAIL SEND Error:<br>{e}
            </div>""",
            unsafe_allow_html=True
            )   
            return False

    st.markdown("""
        <style>
        /* Expander container */
        details {
            border: 2px solid #006658;
            border-radius: 10px;
            padding: 10px;

            color: #006658;
            margin-top: 10px;
        }

        /* Expander summary line */
        summary {
            font-size: 18px;
            font-weight: bold;
            background-color: #664a00;
            color: white;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            outline: none;
        }

        /* When expander is open */
        details[open] summary {
            background-color: #0059b3;
        }

        /* Hover effect */
        summary:hover {
            background-color: #664400;
        }
        </style>
        """, unsafe_allow_html=True)
    with st.expander("Forgot Password?"):
        username_forgot = st.text_input("Enter your username", key="forgot_username")
        if st.button("Send OTP", key="send_otp_btn"):
            conn = create_connection()
            if conn is None:
                st.error("❌ Failed to connect to the database.")
            else:
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        SELECT email FROM usermgmt 
                        WHERE LOWER(TRIM(username)) = LOWER(:username)
                    """, {"username": username_forgot.strip()})
                    result = cur.fetchone()
                    if result:
                        email = result[0]
                #        print(email) # Debugging line to check email
                        success = send_otp_email(email, username_forgot)
                        if success:
                            st.success(f"OTP sent to {email}")
                            st.session_state.otp_sent = True
                            st.session_state.otp_user = username_forgot
                        else:
                            st.error("❌ Failed to send OTP.")
                    else:
                        st.error("❌ Username not found. Please check spelling or case.")
                except Exception as e:
                    st.error(f"❌ Database Error: {str(e)}")
                finally:
                    cur.close()
                    conn.close()
   
    if st.session_state.get("otp_sent"):
        entered_otp = st.text_input("Enter OTP sent to your email")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Reset Password"):
            if entered_otp.strip() == st.session_state.get("generated_otp", ""):
                conn = create_connection()
                if conn is None:
                    st.error("❌ Failed to connect to the database.")
                else:
                    try:
                        cur = conn.cursor()
                        cur.execute("UPDATE usermgmt SET password=:1 WHERE username=:2",
                                    (hash_password(new_pass), st.session_state.otp_user))
                        conn.commit()
                        st.success("✅ Password updated. You can now login.")
                        del st.session_state["otp_sent"]
                        del st.session_state["otp_user"]
                        del st.session_state["generated_otp"]
                    except Exception as e:
                        st.error(f"❌ Database Error: {str(e)}")
                    finally:
                        cur.close()
                        conn.close()
            else:
                st.error("Invalid OTP.")


def main():
        
      #  print("Session state desig_code is", st.session_state.desig_code)   
      #  print("Session state username is", st.session_state.username)
      #  print("Session state role is", st.session_state.role)
        desig_codes = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,25}
        if st.session_state.desig_code in desig_codes:
            inbox()  # <-- call your imported function
        elif st.session_state.desig_code == 24:
            loggedinSECGM()  # <-- call your imported function
        else:
            st.error("Unauthorized user role!")


# Entry Point
if not st.session_state.logged_in:
    login_signup_screen()
else:
    main()