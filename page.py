import streamlit as st
import json
import os

# ---------- FILE STORAGE ----------
FILE = "resume_ai_data.json"

def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError
            # Keep default keys so UI always works.
            default = {
                "name": "",
                "contact": "",
                "objective": "",
                "education": [],
                "skills": [],
                "projects": [],
                "experience": []
            }
            default.update(data)
            return default
        except (json.JSONDecodeError, ValueError, OSError):
            return {
                "name": "",
                "contact": "",
                "objective": "",
                "education": [],
                "skills": [],
                "projects": [],
                "experience": []
            }
    else:
        return {
            "name": "",
            "contact": "",
            "objective": "",
            "education": [],
            "skills": [],
            "projects": [],
            "experience": []
        }

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

resume = load_data()

# ---------- UI ----------
st.set_page_config(page_title="Personal Resume AI", layout="wide")

st.title("🤖 Personal AI Resume Builder")

st.sidebar.header("AI Assistant")

prompt = st.sidebar.text_input("Tell AI what to add (Example: Add Python skill)")

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

resume_model = st.sidebar.selectbox("Choose resume model", ["Professional", "Modern", "Executive"], index=0)
show_preview = st.sidebar.checkbox("Show live preview window", value=True)

# ---------- FORM INPUT ----------
st.header("Enter Details")

resume["name"] = st.text_input("Full Name", resume["name"])
resume["contact"] = st.text_input("Contact / Email / LinkedIn", resume["contact"])
resume["objective"] = st.text_area("Career Objective", resume["objective"])

edu = st.text_input("Add Education")
if st.button("Add Education"):
    resume["education"].append(edu)

skill = st.text_input("Add Skill")
if st.button("Add Skill"):
    resume["skills"].append(skill)

proj = st.text_input("Add Project")
if st.button("Add Project"):
    resume["projects"].append(proj)

exp = st.text_input("Add Experience")
if st.button("Add Experience"):
    resume["experience"].append(exp)

save_data(resume)

# ---------- LIVE PREVIEW ----------
st.header("📄 Live Resume Preview")

if show_preview:
    preview_box = st.expander("Open live preview window", expanded=True)
    with preview_box:
        col1, col2 = st.columns([1,2])
        with col1:
            st.markdown("**Name**")
            st.write(resume["name"] or "(not entered)")
            st.markdown("**Contact**")
            st.write(resume["contact"] or "(not entered)")
            st.markdown("**Objective**")
            st.write(resume["objective"] or "(not entered)")
        with col2:
            if resume_model == "Professional":
                st.markdown("### " + (resume["name"] or "Your Name"))
                st.write("_" + (resume["contact"] or "Contact details...") + "_")
                st.write("---")
                st.markdown("**Career Objective**")
                st.write(resume["objective"] or "Add your objective to preview...")
                if resume["education"]:
                    st.markdown("**Education**")
                    for e in resume["education"]:
                        st.write("•", e)
                if resume["skills"]:
                    st.markdown("**Key Skills**")
                    st.write(" • ".join(resume["skills"]))
                if resume["projects"]:
                    st.markdown("**Projects**")
                    for p in resume["projects"]:
                        st.write("•", p)
                if resume["experience"]:
                    st.markdown("**Experience**")
                    for ex in resume["experience"]:
                        st.write("•", ex)
            else:
                st.subheader(resume["name"] or "Your Name")
                st.write(resume["contact"] or "Contact details...")
                st.markdown("**Career Objective**")
                st.write(resume["objective"] or "Add your objective to preview...")
                if resume["education"]:
                    st.markdown("**Education**")
                    for e in resume["education"]:
                        st.write("•", e)
                if resume["skills"]:
                    st.markdown("**Skills**")
                    st.write(", ".join(resume["skills"]))
                if resume["projects"]:
                    st.markdown("**Projects**")
                    for p in resume["projects"]:
                        st.write("•", p)
                if resume["experience"]:
                    st.markdown("**Experience**")
                    for ex in resume["experience"]:
                        st.write("•", ex)
else:
    st.info("Enable 'Show live preview window' from the sidebar to view the resume preview.")

# ---------- AUTO SAVE ----------
save_data(resume)