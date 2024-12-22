import streamlit as st
import os
import requests
import PyPDF2
import google.generativeai as genai
from googletrans import Translator
from streamlit_lottie import st_lottie
from dotenv import load_dotenv
import json  # Ensure json is imported

# Load environment variables
load_dotenv()

# Set page configuration with a custom theme
st.set_page_config(
    page_title="Smart ATS",
    page_icon=":briefcase:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Configure the Google Gemini model with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the translator
translator = Translator()

def load_lottieurl(url: str):
    """
    Load a Lottie animation from a URL.
    """
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def gemini_response(input_text):
    """
    Generate a response from the Google Gemini model based on the input prompt.
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    """
    Extract text from an uploaded PDF file.
    """
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text + "\n"
    return text

def translate_text(text, dest_language):
    """
    Translate text to the specified language using Google Translate.
    """
    if dest_language == 'en':
        return text
    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return text

# Sidebar with language selection and contact information
languages = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh-cn': 'Chinese (Simplified)',
    'hi': 'Hindi',
    # Add more languages as needed
}

st.sidebar.title("Language Selection")
selected_lang_code = st.sidebar.selectbox(
    "Choose your language:",
    list(languages.keys()),
    format_func=lambda x: languages[x]
)

st.sidebar.title("Contact Us")
st.sidebar.info("""
If you have any questions or feedback, please reach out to us at [ayushjhindal07@gmail.com](mailto:ayushjhindal07@gmail.com).
""")

# Main Interface with Header Lottie Animation
lottie_url_header = "https://assets7.lottiefiles.com/packages/lf20_0yfsb3a1.json"  # Replace with your Lottie animation URL
lottie_header = load_lottieurl(lottie_url_header)
if lottie_header:
    st_lottie(lottie_header, height=200, key="header_animation")

st.title(translate_text("Smart ATS", selected_lang_code))
st.markdown(translate_text("**Optimize Your Resume for Job Applications**", selected_lang_code))

# Tabs for navigation
tab1, tab2, tab3 = st.tabs([
    translate_text("Home", selected_lang_code),
    translate_text("Features", selected_lang_code),
    translate_text("About", selected_lang_code)
])

with tab1:
    st.header(translate_text("Welcome to Smart ATS", selected_lang_code))
    st.write(translate_text("Your one-stop solution for resume optimization.", selected_lang_code))

    # Expander for additional information
    with st.expander(translate_text("See how it works", selected_lang_code)):
        how_it_works_content = f"""
            **Welcome to Smart ATS!**

            Smart ATS is designed to help you optimize your resume and improve your chances of getting noticed by employers. Here's how it works:

            1. **Upload Your Resume**: Upload your resume in PDF format using the upload button provided.

            2. **Paste the Job Description**: Copy and paste the job description of the position you're applying for into the text area.

            3. **Select a Feature**: Choose from a variety of features to analyze and enhance your resume:

               - **Skill Gap Analysis**: Identifies missing skills in your resume compared to the job description.
               - **Actionable Recommendations**: Provides specific suggestions on how to improve your resume.
               - **Keyword Optimization**: Highlights important keywords from the job description and shows how to incorporate them into your resume.
               - **ATS Compliance Check**: Checks your resume for Applicant Tracking System (ATS) compatibility issues.
               - **Cover Letter Generator**: Generates a personalized cover letter based on your resume and the job description.
               - **Detailed Match Analysis**: Provides an in-depth analysis of how well your resume matches the job description, including strengths, weaknesses, and overall match percentage.

            4. **Run the Analysis**: Click the "Run" button to execute the selected feature. The application will process your inputs and provide results.

            5. **View and Download Results**: Review the output displayed on the screen. You can also download the results for future reference.

            **Behind the Scenes**

            - **Advanced AI Models**: Smart ATS utilizes the Google Gemini AI model to generate insightful analyses and recommendations tailored to your resume and the job description.

            - **Multilingual Support**: The application supports multiple languages. If your resume or job description is in a different language, Smart ATS will translate it to ensure accurate analysis.

            - **User-Friendly Interface**: The intuitive design, animations, and progress indicators provide a seamless experience while using the application.

            **Why Use Smart ATS?**

            - **Improve Your Resume**: Get expert advice on how to enhance your resume to better align with job requirements.

            - **Increase Interview Chances**: By optimizing your resume and cover letter, you increase the likelihood of passing through ATS filters and catching the recruiter's attention.

            - **Save Time**: Quickly generate personalized cover letters and receive actionable feedback without spending hours researching.
            """
        st.markdown(translate_text(how_it_works_content, selected_lang_code))

    # Add a Lottie animation in the Home tab
    lottie_url_home = "https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json"  # Replace with your Lottie animation URL
    lottie_home = load_lottieurl(lottie_url_home)
    if lottie_home:
        st_lottie(lottie_home, height=300, key="home_animation")



with tab2:
    st.header(translate_text("Features", selected_lang_code))

    # Layout using columns for Job Description and Resume Upload
    col1, col2 = st.columns([2, 1])

    with col1:
        jd_label = translate_text("Paste the Job Description", selected_lang_code)
        jd = st.text_area(jd_label, height=300)

    with col2:
        resume_label = translate_text("Upload Your Resume", selected_lang_code)
        uploaded_file = st.file_uploader(
            resume_label,
            type="pdf",
            help=translate_text("Please upload your resume in PDF format", selected_lang_code)
        )
        if uploaded_file is not None:
            st.success(translate_text("Resume Uploaded Successfully", selected_lang_code))
            # Optionally, display a preview or first page of the resume
            # with open("temp_resume.pdf", "wb") as f:
            #     f.write(uploaded_file.getbuffer())
            # st.pdf("temp_resume.pdf")

    # Feature selection dropdown
    feature_options = [
        "Skill Gap Analysis",
        "Actionable Recommendations",
        "Keyword Optimization",
        "ATS Compliance Check",
        "Cover Letter Generator",
        "Detailed Match Analysis",
        "Craft New Resume"
    ]

    feature_options_translated = [translate_text(option, selected_lang_code) for option in feature_options]

    selected_feature = st.selectbox(
        translate_text("Select a Feature to Perform:", selected_lang_code),
        feature_options_translated
    )

    execute_button = st.button(translate_text("Run", selected_lang_code))

    if execute_button:
        if uploaded_file is not None and jd.strip() != "":
            # Initialize progress bar
            progress_bar = st.progress(0)
            progress_bar.progress(10)

            resume_text = input_pdf_text(uploaded_file)

            # Translate resume and job description to English if necessary
            if selected_lang_code != 'en':
                with st.spinner(translate_text("Translating documents...", selected_lang_code)):
                    resume_text_translated = translate_text(resume_text, 'en')
                    jd_translated = translate_text(jd, 'en')
            else:
                resume_text_translated = resume_text
                jd_translated = jd

            progress_bar.progress(30)

            # Feature 1: Skill Gap Analysis
            input_prompt1 = f"""
            You are an expert career consultant specializing in skill gap analysis.

            **Instructions:**

            1. **Extract key skills and qualifications from the job description.**
            2. **Extract skills and qualifications from the resume.**
            3. **Compare the two lists, considering synonyms, related terms, and different expressions of the same skills or qualifications.**
            4. **Identify and list only those skills and qualifications that are truly missing from the resume and are not present in any form.**
            5. **Identify if any skill and qualifications are related in any other form as well like may be the skill is mentioned in Plural form in resume but singular in Job Description.**
            6. **Check their project as well how they worked on that and with which skills and stacks and consider those skills as well while comparing it with Job Description.**

            **Important Notes:**

            - **When comparing, consider that the same skill may be described differently.**
            - **Do not list a skill as missing if it is present in the resume, even if phrased differently.**
            - **Focus on the meaning and context of the skills, not just the exact wording.**
            - **Do not add any fake information or experiences.**

            **Example:**

            *Job Description Skills:*
            - Machine Learning
            - Data Visualization (e.g., Tableau)
            - Project Management
            - LLM

            *Resume Skills:*
            - Proficient in machine learning algorithms
            - Experienced with Tableau for data visualization
            - Managed multiple data science projects
            - LLMs

            *Missing Skills:*
            - None

            **Resume:**
            {resume_text_translated}

            **Job Description:**
            {jd_translated}

            **Provide the missing skills and qualifications in a bullet-point list, ensuring that any skill listed is genuinely absent from the resume.**
            """

            # Feature 2: Actionable Recommendations
            input_prompt2 = f"""
            You are a professional career advisor.

            **Instructions:**

            - Review the resume and job description thoroughly.
            - Provide actionable recommendations on how the candidate can improve their resume to better match the job description.
            - **For each recommendation, specify the section or bullet point in the resume where the change should be made.**
            - Focus on:

              - Enhancing existing content.
              - Rephrasing statements to include relevant keywords from the job description.
              - Highlighting relevant experiences and achievements already present in the resume.
              - Addressing any weaknesses or gaps by suggesting how to better present existing information.

            - Do not suggest adding any fake experiences or qualifications.
            - Do not recommend removing any relevant content.

            **Resume:**
            {resume_text_translated}

            **Job Description:**
            {jd_translated}

            **Provide your recommendations in a numbered list, clearly indicating where changes should be made.**
            """

            # Feature 3: Keyword Optimization
            input_prompt3 = f"""
            You are an expert in resume optimization for ATS systems.

            **Instructions:**

            1. **Extract important keywords and phrases from the job description, including synonyms and related terms.**
            2. **Analyze the resume to identify which of these keywords are missing or not prominently featured, considering different expressions of the same concepts.**
            3. **Suggest where and how the candidate can naturally incorporate the missing or underrepresented keywords into their existing resume content.**
            4. **For each suggestion, specify the exact section or bullet point in the resume for incorporation.**

            **Important Notes:**

            - **Do not suggest adding any fake experiences or skills.**
            - **Focus on rephrasing or enhancing current content.**
            - **Ensure the suggestions are integrated seamlessly and naturally.**

            **Resume:**
            {resume_text_translated}

            **Job Description:**
            {jd_translated}

            **Provide your suggestions in detail, indicating the resume sections where keywords can be added or emphasized.**
            """

            # Feature 4: ATS Compliance Checker
            input_prompt4 = f"""
            You are an expert in Applicant Tracking Systems (ATS) compliance.

            **Instructions:**

            - Analyze the resume's formatting and structure to ensure it is ATS-friendly.
            - Check for:

              - Use of complex layouts, graphics, or images.
              - Use of tables, columns, headers, footers, or text boxes.
              - Inappropriate fonts, font sizes, or styles.
              - Use of special characters or symbols.
              - Missing or mislabeled section headings.
              - Incorrect file format (ensure it's in a standard format like .docx or .pdf).
              - Consistency in formatting throughout the document.
              - Any embedded objects or links.

            - **For each issue identified, provide a clear recommendation on how to fix it.**

            **Resume:**
            {resume_text_translated}

            **Provide your analysis and recommendations in a clear, concise manner, organized by issue.**
            """

            # Feature 5: Cover Letter Generator
            input_prompt5 = f"""
            You are a professional cover letter writer.

            **Instructions:**

            - Based solely on the information provided in the resume, write a personalized cover letter tailored to the job description.
            - **Do not introduce any new skills, experiences, or qualifications not present in the resume.**
            - Highlight the candidate's relevant skills and experiences that align with the job requirements.
            - Explain why the candidate is a good fit for the position.
            - Ensure the tone is professional and engaging.

            **Important Notes:**

            - **Avoid generic statements; make the cover letter specific to the job description and the candidate's background.**
            - **Do not include any fake or exaggerated information.**

            **Resume:**
            {resume_text_translated}

            **Job Description:**
            {jd_translated}

            **Provide the cover letter below.**
            """

            # Feature 7: Detailed Match Analysis Report
            input_prompt7 = f"""
            You are an expert in resume analysis.

            **Instructions:**

            - Analyze the candidate's resume against the job description.
            - **When comparing, consider synonyms, related terms, and different expressions of the same skills or experiences.**
            - **Ensure that skills or experiences present in the resume but phrased differently are correctly identified as matches.**
            - The report should include:

              - **Overall percentage match**, justified by your analysis.
              - **Scores for the following sections** (out of 100), with brief justifications:
                - Skills.
                - Experience.
                - Education.
                - Keywords.
              - **Strengths**: Highlight areas where the candidate strongly aligns with the job requirements.
              - **Weaknesses**: Identify any genuine gaps or areas lacking in the resume.
              - **Recommendations for improvement**: Suggest how the candidate can enhance their resume, focusing on rephrasing or emphasizing existing content.

            - Do not include any fake information.

            **Resume:**
            {resume_text_translated}

            **Job Description:**
            {jd_translated}

            **Provide the report in a structured format, using headings and bullet points for clarity.**
            """

            # Feature 8: Craft New Resume (New Feature)
            input_prompt8 = f"""
                        You are an expert resume writer.

                        **Instructions:**

                        - Review the candidate's resume and the provided job description.
                        - **Enhance the resume by incorporating relevant keywords and improving grammatical structure to better align with the job description.**
                        - **Do not add any new skills, experiences, or qualifications not present in the original resume.**
                        - **Do not remove any existing content.**
                        - Ensure that the resume remains truthful and accurately represents the candidate's qualifications.
                        - **Focus on rephrasing sentences to include important keywords from the job description and improving overall readability**

                        **Resume:**
                        {resume_text_translated}

                        **Job Description:**
                        {jd_translated}

                        **Provide the updated resume below with improved keyword integration and grammar.**
                        """

            # Map the selected feature to the corresponding prompt and subheader
            feature_prompt_mapping = {
                "Skill Gap Analysis": (input_prompt1, "Skill Gap Analysis"),
                "Actionable Recommendations": (input_prompt2, "Actionable Recommendations"),
                "Keyword Optimization": (input_prompt3, "Keyword Optimization Suggestions"),
                "ATS Compliance Check": (input_prompt4, "ATS Compliance Report"),
                "Cover Letter Generator": (input_prompt5, "Generated Cover Letter"),
                "Detailed Match Analysis": (input_prompt7, "Detailed Match Analysis Report"),
                "Craft New Resume": (input_prompt8, "Crafted Resume")
            }

            # Get the original feature name based on the selected translated feature
            try:
                selected_feature_original = feature_options[feature_options_translated.index(selected_feature)]
            except ValueError:
                st.error(translate_text("Selected feature is not recognized.", selected_lang_code))
                selected_feature_original = None

            if selected_feature_original:
                prompt, subheader = feature_prompt_mapping.get(selected_feature_original, ("", ""))

                if prompt and subheader:
                    with st.spinner(translate_text("Processing...", selected_lang_code)):
                        # Update progress bar
                        progress_bar.progress(80)
                        response = gemini_response(prompt)
                        # Update progress bar
                        progress_bar.progress(100)

                    # Clear progress bar
                    progress_bar.empty()

                    # Translate the response back to the selected language if necessary
                    if selected_lang_code != 'en':
                        try:
                            response_translated = translate_text(response, selected_lang_code)
                        except Exception as e:
                            st.error(f"Translation failed: {e}")
                            response_translated = response
                        subheader_translated = translate_text(subheader, selected_lang_code)
                        st.subheader(subheader_translated)
                        st.write(response_translated)
                    else:
                        st.subheader(subheader)
                        st.write(response)

                    # Provide download option for the response
                    st.download_button(
                        label=translate_text("Download Result", selected_lang_code),
                        data=response.encode('utf-8'),
                        file_name='result.txt',
                        mime='text/plain',
                    )

                else:
                    st.error(translate_text("Selected feature is not supported.", selected_lang_code))
            else:
                st.error(translate_text("Selected feature is not recognized.", selected_lang_code))
        else:
            st.warning(translate_text("Please upload both the resume and job description.", selected_lang_code))

with tab3:
    st.header(translate_text("About", selected_lang_code))
    st.write(translate_text("Learn more about Smart ATS and how it can help you.", selected_lang_code))

    # Expander for FAQs
    with st.expander(translate_text("Frequently Asked Questions", selected_lang_code)):
        faq_content = f"""
            **Q1: How does the Smart ATS work?**

            **A1:** Smart ATS leverages advanced AI technology to analyze your resume in comparison with the job description you provide. By using natural language processing and machine learning models, it understands the content of both documents, identifies key skills and qualifications, and provides tailored feedback. The features include skill gap analysis, actionable recommendations, keyword optimization, ATS compliance checking, cover letter generation, and detailed match analysis. The application translates documents if necessary and presents results in a user-friendly interface with options to download the outputs.

            **Q2: Is my data secure?**

            **A2:** Yes, your data is secure. Smart ATS does not store or share your resume, job description, or any personal information. The documents you upload are used only temporarily for analysis during your session and are not saved on any servers. We prioritize your privacy and ensure that all data processing complies with applicable data protection regulations.

            **Q3: What file formats are supported for resume upload?**

            **A3:** Currently, Smart ATS supports PDF files for resume uploads to ensure consistent formatting and accurate text extraction. We are working on expanding support to other formats like DOCX in future updates.

            **Q4: How does the Skill Gap Analysis work?**

            **A4:** The Skill Gap Analysis feature compares the skills listed in your resume against those required in the job description. It identifies any missing or underrepresented skills and provides a bullet-point list of these gaps, helping you understand areas where your resume can be improved to better align with the job requirements.

            **Q5: Can I use Smart ATS multiple times?**

            **A5:** Yes, you can use Smart ATS as many times as you need. Whether you're applying for multiple jobs or revising your resume for different positions, Smart ATS is here to assist you in optimizing your documents each time.

            **Q6: Does Smart ATS improve my chances of getting an interview?**

            **A6:** While Smart ATS provides valuable insights and optimizations to enhance your resume and cover letter, ultimately, securing an interview also depends on various factors such as your experience, the job market, and the employer's specific needs. However, by aligning your documents more closely with job descriptions and ensuring ATS compatibility, Smart ATS can significantly improve your chances of passing initial screenings.

            **Q7: How accurate are the recommendations provided by Smart ATS?**

            **A7:** Smart ATS utilizes cutting-edge AI models to provide accurate and relevant recommendations based on the information you provide. However, it's always a good practice to review the suggestions to ensure they accurately reflect your skills and experiences.

            **Q8: Can Smart ATS be used for any industry?**

            **A8:** Yes, Smart ATS is designed to be versatile and can be used across various industries. Whether you're in technology, healthcare, finance, or any other field, Smart ATS can help optimize your resume to meet the specific requirements of different job descriptions.

            **Q9: How do I get started with Smart ATS?**

            **A9:** Getting started is easy! Simply navigate to the "Features" tab, upload your resume in PDF format, paste the job description you're targeting, select the feature you'd like to use, and click "Run". Smart ATS will process your inputs and provide actionable insights to enhance your resume and cover letter.

            **Q10: Can I customize the cover letter generated by Smart ATS?**

            **A10:** Absolutely! The Cover Letter Generator provides a personalized draft based on your resume and the job description. You can further customize this cover letter to better reflect your unique voice and any additional details you'd like to include.
            """
        st.markdown(translate_text(faq_content, selected_lang_code))

    # Add a Lottie animation in the About tab
    lottie_url_about = "https://assets5.lottiefiles.com/packages/lf20_jtbfg2nb.json"  # Replace with your Lottie animation URL
    lottie_about = load_lottieurl(lottie_url_about)
    if lottie_about:
        st_lottie(lottie_about, height=200, key="about_animation")



# Footer
def footer():
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        color: #262730;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>Developed by Ayush Jhindal | © 2024 All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

footer()