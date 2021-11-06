import streamlit as st
from positive_cases import pc_main
from recovery_count import rc_main
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
def set_page_title(title):
    st.sidebar.markdown(unsafe_allow_html=True, body=f"""
        <iframe height=0 srcdoc="<script>
            const title = window.parent.document.querySelector('title') \

            const oldObserver = window.parent.titleObserver
            if (oldObserver) {{
                oldObserver.disconnect()
            }} \

            const newObserver = new MutationObserver(function(mutations) {{
                const target = mutations[0].target
                if (target.text !== '{title}') {{
                    target.text = '{title}'
                }}
            }}) \

            newObserver.observe(title, {{ childList: true }})
            window.parent.titleObserver = newObserver \

            title.text = '{title}'
        </script>" />
    """)
set_page_title('Covid 19 data analysis')
st.sidebar.write('Hello! Thanks for visiting this project.')
st.sidebar.write('Now, please close this sidebar and continue to view the output')
st.title('Covid 19 analysis and forecasting')
st.header('Forecasting the future pandemic based on the data of overall India and the data of Andhra Pradesh')
option=st.radio('Select here',['Daily positive cases count','Daily recovery count'])
if option=='Daily positive cases count':
    pc_main()
if option=='Daily recovery count':
    rc_main()
