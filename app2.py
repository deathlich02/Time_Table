import streamlit as st
import pandas as pd
import io


subject_data = {
    # CSE Subjects
    "Semantic Web": pd.read_excel("P4-Semantic Web.xlsx"),
    "Machine Learning (PE-4)": pd.read_excel("P4-Machine Learning.xlsx"),
    "Quantum Comp Practice (PE-4)": pd.read_excel("P4-Quantum Computing Practice and Applications.xlsx"),
    "Text Analytics (PE-3)": pd.read_excel("P3-Text Analytics.xlsx"),
    "Quantum Info Theory (PE-3)": pd.read_excel("P3-Quantum Information Theory .xlsx"),
    "Computer Vision (PE-3)": pd.read_excel("P3-Computer Vision.xlsx"),
    "Distributed Systems": pd.read_excel("4.Distributed Systems.xlsx"),
    "Deep Learning": pd.read_excel("3.Deep Learning.xlsx"),
    "Cloud Computing": pd.read_excel("1.Cloud Computing.xlsx"),
    "Blockchain Tech": pd.read_excel("2.Block Chain Technology.xlsx"),

    # CYS Subjects , some i havent filled cus i dindnt get the data
    "Ethereum Smart Contract": pd.DataFrame(),
    "Neural Computation and Applications": pd.DataFrame(),
    "Social Network Analysis": pd.DataFrame(),
    "Semantic Web (CYS)": pd.DataFrame(),
    "Cyber Law and Ethics": pd.DataFrame(),
    "AI in Cyber Security": pd.DataFrame(),
    "Software Engineering": pd.read_excel(
        "VII CY Semester Program elective-Student List_Ason_7July.xlsx",
        sheet_name="IT_4061-Software engineering"
    ).rename(columns={"Reg no": "registration number"})[["registration number"]],
    "Database and Application Security": pd.read_excel(
        "VII CY Semester Program elective-Student List_Ason_7July.xlsx",
        sheet_name="IT_4060-Database and App Sec"
    ).rename(columns={"Reg no": "registration number"})[["registration number"]],
    "Ethical Hacking and Cyber Security": pd.read_excel(
        "VII CY Semester Program elective-Student List_Ason_7July.xlsx",
        sheet_name="IT_4024-ETHICAL HACKING "
    ).rename(columns={"Reg no": "registration number"})[["registration number"]],
    "Generative AI and Applications": pd.read_excel(
        "VII CY Semester Program elective-Student List_Ason_7July.xlsx",
        sheet_name="IT_4451-Generative AI and App"
    ).rename(columns={"Reg no": "registration number"})[["registration number"]],
    "Pattern Classification": pd.DataFrame()
}

#Time tables, did this manually couldn't figure out how to scan the pdf
cse_layout = {
    "Mon": ["", "","Break", "", "", "Lunch", "PE-4", "DS", "Break", "CC", "CV/TA"],
    "Tue": ["BCT", "DL", "Break", "CC", "HONS", "Lunch", "OE", "", "Break", "", ""],
    "Wed": ["", "", "Break", "HONS", "QIT", "Lunch", "DS", "CV/TA", "Break", "BCT", "DL"],
    "Thu": ["PE-4", "CC", "Break","CV/TA","DS", "Lunch", "HONS", "QIT", "Break", "", ""],
    "Fri": ["", "", "Break", "QIT", "HONS", "Lunch", "BCT", "DL", "Break", "PE-4", ""]
}

cys_layout = {
    "Mon": ["PE-3", "SE","Break", "", "", "Lunch", "HONS", "DAS", "Break", "GENAI", ""],
    "Tue": ["HONS", "PE-3", "Break", "DAS", "PE-4", "Lunch", "OE", "", "Break", "", ""],
    "Wed": ["SE", "GENAI", "Break", "EHCS", "", "Lunch", "PE-3", "DAS", "Break", "PE-4", ""],
    "Thu": ["", "", "Break","","", "Lunch", "EHCS", "GENAI", "Break", "SE", "HONS"],
    "Fri": ["HONS", "PE-4", "Break", "EHCS", "", "Lunch", "", "", "Break", "", ""]
}

#mapping that shi
cse_map = {
    "PE-4": ["Semantic Web", "Machine Learning (PE-4)", "Quantum Comp Practice (PE-4)"],
    "PE-3": ["Text Analytics (PE-3)", "Quantum Info Theory (PE-3)", "Computer Vision (PE-3)"],
    "CV/TA": ["Text Analytics (PE-3)", "Computer Vision (PE-3)"],
    "QIT": ["Quantum Info Theory (PE-3)"],
    "HONS": ["Systems and Network Security"],
    "OE": ["Social Networks"],
    "DS": ["Distributed Systems"],
    "DL": ["Deep Learning"],
    "CC": ["Cloud Computing"],
    "BCT": ["Blockchain Tech"]
}

cys_map = {
    "PE3": ["Ethereum Smart Contract", "Cyber Law and Ethics", "Social Network Analysis", "Pattern recognition"],
    "PE4": ["Semantic Web (CYS)", "Neural Computation and Applications", "Blockchain for Business", "AI in Cyber Security"],
    "HONS": ["Pattern Classification"],
    "SE": ["Software Engineering"],
    "DAS": ["Database and Application Security"],
    "GENAI": ["Generative AI and Applications"],
    "EHCS": ["Ethical Hacking and Cyber Security"],
    "OE": ["Pattern Classification"]
}

#the only thing that was easy to do
def get_subjects(regno, subject_data):
    regno = str(regno).strip().upper()
    subjects = []
    for subject, df in subject_data.items():
        if not df.empty:
            df.columns = df.columns.str.strip().str.lower()
            if "registration number" in df.columns:
                regnos = df["registration number"].apply(lambda x: str(int(x)) if pd.notna(x) else "").str.strip().str.upper()
                if regno in regnos.values:
                    subjects.append(subject)
    return subjects


def format_pdf_daywise_table(timetable_dict, abbreviation_map, enrolled_subjects):
    col_headers = [
        "Day", "9:00–9:50", "9:50–10:40", "Break-1",
        "10:50–11:40", "11:40–12:30", "Lunch",
        "1:00–1:50", "1:50–2:40", "Break-2",
        "2:50–3:40", "3:40–4:30"
    ]

    result = []
    for day, slots in timetable_dict.items():
        row = [day]
        for slot in slots:
            if slot.lower() in ["break", "lunch"]:
                row.append(slot.title())
            elif slot in abbreviation_map:
                match = next((s for s in abbreviation_map[slot] if s in enrolled_subjects), "")
                row.append(match)
            elif slot in enrolled_subjects:
                row.append(slot)
            else:
                row.append("")
        if len(row) > len(col_headers):
            row = row[:len(col_headers)]
        elif len(row) < len(col_headers):
            row += [""] * (len(col_headers) - len(row))
        result.append(row)

    return pd.DataFrame(result, columns=col_headers)

def generate_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Timetable')
        writer.save()
    output.seek(0)
    return output


st.title("\U0001F4C3 Personalized Timetable Generator")

section = st.selectbox("Select your section:", ["CSE-A&B", "CYS-A"])
regno = st.text_input("Enter your Registration Number")

if section and regno:
    timetable = cse_layout if section == "CSE-A&B" else cys_layout
    abbreviation_map = cse_map if section == "CSE-A&B" else cys_map

    subjects = get_subjects(regno, subject_data)

    if subjects:
        st.success("✅ Subjects Found:")
        st.write(subjects)

        final_df = format_pdf_daywise_table(timetable, abbreviation_map, subjects)
        st.dataframe(final_df)

        excel_file = generate_excel(final_df)
        st.download_button(
            label="\U0001F4C5 Download Timetable as Excel",
            data=excel_file,
            file_name=f"{regno}_timetable.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No subjects found for this registration number.")