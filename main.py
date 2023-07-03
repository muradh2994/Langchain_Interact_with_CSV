import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
#from tempfile import NamedTemporaryFile
import os

class TemporaryFileContext:
    def __enter__(self):
        self.temp_file = open("Tempfile.csv", "wb")
        return self.temp_file

    def __exit__(self, exc_type, exc_value, traceback):
        self.temp_file.close()
        os.remove("Tempfile.csv")

def main():

    load_dotenv()

    st.set_page_config(page_title="Ask your CV 📈 ")
    st.header("Ask your CSV")
    
    #read your file
    user_csv = st.file_uploader("Upload your CSV", type="csv")

    if user_csv is not None:
        
        with TemporaryFileContext() as f: # Create temporary file
            f.write(user_csv.getvalue()) # Save uploaded contents to file
            #f.flush()
            llm = OpenAI(temperature=0)
            user_question = st.text_input("Ask any question about your CSV:")
            agent = create_csv_agent(llm,f.name,verbose=True)

        if user_question is not None:
            response = agent.run(user_question)
            st.write(response)


if __name__=="__main__":
    main()