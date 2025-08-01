import streamlit as st

# Simulated data
comment = st.text_area("Comment")

# Confirmation trigger
if st.button("Submit Comment"):
    st.session_state.show_confirm = True

# Simulated modal/dialog
if st.session_state.get("show_confirm", False):
    with st.expander("⚠️ Confirm Submission", expanded=True):
        st.write("📝 Are you sure you want to submit this comment?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Submit"):
                st.success("✅ Comment submitted successfully!")
                st.session_state.show_confirm = False
                # Place your DB insert logic here

        with col2:
            if st.button("❌ Cancel"):
                st.warning("Submission cancelled.")
                st.session_state.show_confirm = False
