import streamlit as st

# simple in-memory user storage
USERS = {
    "admin@rebox.com": "rebox123"
}


def login_page():

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.title(" ReBox Platform Access")

        tab1, tab2 = st.tabs(["Login","Create Account"])

        # LOGIN TAB
        with tab1:

            with st.form("login_form"):

                email = st.text_input("Email Address")

                password = st.text_input("Password", type="password")

                submit = st.form_submit_button(
                    "Secure Login",
                    use_container_width=True
                )

                if submit:

                    if email in USERS and USERS[email] == password:

                        st.session_state["logged_in"] = True

                        st.session_state["username"] = email.split("@")[0]

                        st.success("Login Successful")

                        st.rerun()

                    else:

                        st.error("Invalid credentials")

        # SIGNUP TAB
        with tab2:

            with st.form("signup_form"):

                new_email = st.text_input("New Email")

                new_password = st.text_input("New Password", type="password")

                confirm = st.text_input("Confirm Password", type="password")

                create_btn = st.form_submit_button(
                    "Create Account",
                    use_container_width=True
                )

                if create_btn:

                    if new_password != confirm:

                        st.error("Passwords do not match")

                    elif len(new_password) < 6:

                        st.error("Password must be at least 6 characters")

                    else:

                        USERS[new_email] = new_password

                        st.success("Account Created! Please login.")

                        st.balloons()

        st.markdown("---")

        st.caption("ReBox Circular Packaging Intelligence Platform")