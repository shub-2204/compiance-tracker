import oracledb
import streamlit as st
def create_connection():
                    # --- Database Connection Parameters ---
        DB_USER = "wrgminsp"
        DB_PASSWORD = "inspGM@WR"
        DB_HOST = "10.3.19.4"
        DB_PORT = 1523
        DB_SID = "wrcal"
        TARGET_SCHEMA = "wrcal"
        DSN = oracledb.makedsn(DB_HOST, DB_PORT, sid=DB_SID)
        try:
            return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DSN)
        except oracledb.Error as e:
            st.markdown(f"""
            <div style='color:yellow; font-weight:bold;'>
            ❌ Database Connection Error:<br><pre>{str(e)}</pre>
           </div>""", unsafe_allow_html=True)
            return None
