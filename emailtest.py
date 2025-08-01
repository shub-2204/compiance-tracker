import smtplib
from email.message import EmailMessage



#load_dotenv()
EMAIL_USER = "shubhamchauhan2204@gmail.com"
EMAIL_PASS = "zkybhmoankoosxvt"

msg = EmailMessage()
msg.set_content("Test email")
msg["Subject"] = "Test"
msg["From"] = "INDIAN RAILWAYS <shubhamchauhan2204@gmail.com>"
msg["To"] = "<shubhamchauhan2204@gmail.com>"

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")


         cols = st.columns([1.5, 1.5, 1.5, 3, 12])
            headers = ["Inspection ID", "Note Date", "Compliance Date", "Subject", "Details"]
            for col, header in zip(cols, headers):
                col.markdown(f"**{header}**")

            # Rows
            for record in records:
                inspectionid, note_date, compliance_date, subject, details = record
                cols = st.columns([1.5, 1.5, 1.5, 3, 12])

                cols[0].write(inspectionid)
                cols[1].write(note_date.strftime('%Y-%m-%d'))
                cols[2].write(compliance_date.strftime('%Y-%m-%d'))
                cols[3].write(subject)
                
                with cols[4].expander("🔍 View"):
                    st.write(details if details else "No details provided.")
