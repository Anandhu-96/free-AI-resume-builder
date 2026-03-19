import json
import os

FILE = "resume_data.json"

# ---------- LOAD / SAVE ----------
def load_resume():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            pass

    return {
        "name": "",
        "contact": "",
        "objective": "",
        "education": [],
        "skills": [],
        "projects": [],
        "experience": []
    }


def save_resume(resume):
    with open(FILE, "w") as f:
        json.dump(resume, f, indent=4)


# ---------- DISPLAY ----------
def show_resume(resume):
    print("\n" + "="*50)
    print("📄 LIVE RESUME")
    print("="*50)

    print("\nName:", resume["name"])
    print("Contact:", resume["contact"])

    print("\nCareer Objective:")
    print(resume["objective"])

    print("\nEducation:")
    for e in resume["education"]:
        print(" -", e)

    print("\nSkills:")
    for s in resume["skills"]:
        print(" -", s)

    print("\nProjects:")
    for p in resume["projects"]:
        print(" -", p)

    print("\nExperience:")
    for ex in resume["experience"]:
        print(" -", ex)


# ---------- FINAL GENERATE ----------
def generate_resume(resume):
    print("\n" + "="*60)
    print("🚀 FINAL GENERATED RESUME")
    print("="*60)

    print(f"\n{resume['name']}")
    print(resume["contact"])
    print("-"*50)

    if resume["objective"]:
        print("\nCAREER OBJECTIVE")
        print(resume["objective"])

    if resume["education"]:
        print("\nEDUCATION")
        for e in resume["education"]:
            print("•", e)

    if resume["skills"]:
        print("\nSKILLS")
        print(", ".join(resume["skills"]))

    if resume["projects"]:
        print("\nPROJECTS")
        for p in resume["projects"]:
            print("•", p)

    if resume["experience"]:
        print("\nEXPERIENCE")
        for ex in resume["experience"]:
            print("•", ex)


# ---------- AI UNDERSTAND ----------
def ai_update(prompt, resume):
    text = prompt.lower()

    if "name" in text:
        resume["name"] = prompt.replace("name", "").strip()

    elif "contact" in text or "email" in text:
        resume["contact"] = prompt

    elif "objective" in text:
        resume["objective"] = prompt

    elif "education" in text or "college" in text:
        resume["education"].append(prompt)

    elif "skill" in text:
        resume["skills"].append(prompt)

    elif "project" in text:
        resume["projects"].append(prompt)

    elif "experience" in text or "intern" in text:
        resume["experience"].append(prompt)

    else:
        print("⚠️ AI couldn't understand. Try keywords like skill, project, education.")


# ---------- MAIN PROGRAM ----------
resume = load_resume()

print("🤖 PERSONAL AI RESUME BUILDER (TERMINAL)")
print("Type 'help' for options")

while True:

    print("\nOptions:")
    print("1. Add via AI prompt")
    print("2. Manual entry")
    print("3. Show resume")
    print("4. Generate final resume")
    print("5. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":
        prompt = input("👉 Enter prompt: ")
        ai_update(prompt, resume)
        save_resume(resume)

    elif choice == "2":
        print("\nManual Entry")

        resume["name"] = input("Name: ") or resume["name"]
        resume["contact"] = input("Contact: ") or resume["contact"]
        resume["objective"] = input("Objective: ") or resume["objective"]

        edu = input("Add Education: ")
        if edu:
            resume["education"].append(edu)

        skill = input("Add Skill: ")
        if skill:
            resume["skills"].append(skill)

        proj = input("Add Project: ")
        if proj:
            resume["projects"].append(proj)

        exp = input("Add Experience: ")
        if exp:
            resume["experience"].append(exp)

        save_resume(resume)

    elif choice == "3":
        show_resume(resume)

    elif choice == "4":
        generate_resume(resume)

    elif choice == "5":
        print("Exiting...")
        break

    else:
        print("Invalid choice, try again.")