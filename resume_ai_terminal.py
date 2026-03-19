import streamlit as st
import json
import os

# ---------- CONFIG ----------
st.set_page_config(page_title="Resume AI", layout="wide")

# ---------- FILE STORAGE ----------
FILE = "resume_ai_data.json"

def load_data():
    default = {
        "name": "",
        "contact": "",
        "objective": "",
        "education": [],
        "skills": [],
        "projects": [],
        "experience": []
    }

    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                default.update(data)
        except:
            pass

    return default


def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


resume = load_data()

# ---------- SESSION STATE FIX ----------
if "generated" not in st.session_state:
    st.session_state.generated = False

# ---------- UI ----------
st.title("🤖 Personal AI Resume Builder")

# ---------- SIDEBAR AI ----------
st.sidebar.header("AI Assistant")

prompt = st.sidebar.text_input("Tell AI what to add")

if st.sidebar.button("Add via AI"):
    text = prompt.lower()

    if "skill" in text:
        resume["skills"].append(prompt)

    elif "education" in text or "college" in text:
        resume["education"].append(prompt)

    elif "project" in text:
        resume["projects"].append(prompt)

    elif "experience" in text or "intern" in text:
        resume["experience"].append(prompt)

    elif "objective" in text:
        resume["objective"] = prompt

    elif "contact" in text:
        resume["contact"] = prompt

    elif "name" in text:
        resume["name"] = prompt

    else:
        st.sidebar.warning("AI couldn't understand")

    save_data(resume)

resume_model = st.sidebar.selectbox(
    "Choose Resume Style",
    ["Professional", "Modern", "Executive"]
)

show_preview = st.sidebar.checkbox("Show Live Preview", True)

# ---------- INPUT ----------
st.header("Enter Details")

col1, col2 = st.columns(2)

with col1:
    resume["name"] = st.text_input("Full Name", resume["name"])
    resume["contact"] = st.text_input("Contact / Email", resume["contact"])

with col2:
    resume["objective"] = st.text_area("Career Objective", resume["objective"])

# ---------- ADD ITEMS ----------
st.subheader("Add Details")

edu = st.text_input("Education", key="edu")
if st.button("Add Education"):
    if edu:
        resume["education"].append(edu)

skill = st.text_input("Skill", key="skill")
if st.button("Add Skill"):
    if skill:
        resume["skills"].append(skill)

proj = st.text_input("Project", key="proj")
if st.button("Add Project"):
    if proj:
        resume["projects"].append(proj)

exp = st.text_input("Experience", key="exp")
if st.button("Add Experience"):
    if exp:
        resume["experience"].append(exp)

save_data(resume)

# ---------- LIVE PREVIEW ----------
st.header("📄 Live Resume Preview")

if show_preview:

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Basic Info")
        st.write("**Name:**", resume["name"] or "-")
        st.write("**Contact:**", resume["contact"] or "-")
        st.write("**Objective:**", resume["objective"] or "-")

    with col2:
        if resume_model == "Professional":
            st.markdown("## " + (resume["name"] or "Your Name"))
            st.write("_" + (resume["contact"] or "Contact details") + "_")
            st.write("---")
        else:
            st.subheader(resume["name"] or "Your Name")
            st.write(resume["contact"] or "Contact details")

        if resume["objective"]:
            st.markdown("### Career Objective")
            st.write(resume["objective"])

        if resume["education"]:
            st.markdown("### Education")
            for e in resume["education"]:
                st.write("•", e)

        if resume["skills"]:
            st.markdown("### Skills")
            st.write(", ".join(resume["skills"]))

        if resume["projects"]:
            st.markdown("### Projects")
            for p in resume["projects"]:
                st.write("•", p)

        if resume["experience"]:
            st.markdown("### Experience")
            for ex in resume["experience"]:
                st.write("•", ex)

else:
    st.info("Enable preview from sidebar")

# ---------- GENERATE FINAL RESUME (FIXED) ----------
st.header("🚀 Generate Final Resume")

if st.button("Generate Resume"):
    st.session_state.generated = True

if st.session_state.generated:

    st.success("✅ Resume Generated Successfully!")

    st.markdown("## 📄 Final Resume")

    st.markdown(f"# {resume['name']}")
    st.write(resume["contact"])

    st.write("---")

    if resume["objective"]:
        st.markdown("### Career Objective")
        st.write(resume["objective"])

    if resume["education"]:
        st.markdown("### Education")
        for e in resume["education"]:
            st.write("•", e)

    if resume["skills"]:
        st.markdown("### Skills")
        st.write(", ".join(resume["skills"]))

    if resume["projects"]:
        st.markdown("### Projects")
        for p in resume["projects"]:
            st.write("•", p)

    if resume["experience"]:
        st.markdown("### Experience")
        for ex in resume["experience"]:
            st.write("•", ex)

# ---------- DOWNLOAD ----------
def generate_text_resume(resume):
    text = f"{resume['name']}\n{resume['contact']}\n\n"

    text += "Career Objective\n" + resume["objective"] + "\n\n"

    text += "Education\n"
    for e in resume["education"]:
        text += f"- {e}\n"

    text += "\nSkills\n" + ", ".join(resume["skills"]) + "\n\n"

    text += "Projects\n"
    for p in resume["projects"]:
        text += f"- {p}\n"

    text += "\nExperience\n"
    for ex in resume["experience"]:
        text += f"- {ex}\n"

    return text


st.header("📥 Download Resume")

resume_text = generate_text_resume(resume)

st.download_button(
    label="Download as TXT",
    data=resume_text,
    file_name="resume.txt",
    mime="text/plain"
)

# ---------- AUTO SAVE ----------
save_data(resume)