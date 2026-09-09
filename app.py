import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found in .env file.")
    exit()

# Create Gemini client
client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# STUDENT DATA
# --------------------------------------------------

students = {
    "STU001": {
        "name": "Ebenezer",
        "department": "Computer Science and Engineering",
        "year": "3rd Year",
        "cgpa": 7.8,
        "attendance": 82,
        "arrears": 0
    },

    "STU002": {
        "name": "John",
        "department": "Computer Science and Engineering",
        "year": "3rd Year",
        "cgpa": 6.5,
        "attendance": 68,
        "arrears": 2
    }
}


# --------------------------------------------------
# DISPLAY STUDENT INFORMATION
# --------------------------------------------------

def display_student(student):
    print("\n" + "=" * 55)
    print("             STUDENT INFORMATION")
    print("=" * 55)

    print(f"Name       : {student['name']}")
    print(f"Department : {student['department']}")
    print(f"Year       : {student['year']}")
    print(f"CGPA       : {student['cgpa']}")
    print(f"Attendance : {student['attendance']}%")
    print(f"Arrears    : {student['arrears']}")

    print("=" * 55)


# --------------------------------------------------
# STUDENT RISK ANALYSIS
# --------------------------------------------------

def risk_analysis(student):

    risk_score = 0

    if student["attendance"] < 75:
        risk_score += 1

    if student["cgpa"] < 6.5:
        risk_score += 1

    if student["arrears"] > 0:
        risk_score += 1

    if risk_score == 0:
        risk = "LOW RISK"
    elif risk_score == 1:
        risk = "MEDIUM RISK"
    else:
        risk = "HIGH RISK"

    print("\nSTUDENT RISK ANALYSIS")
    print("-" * 55)
    print(f"Risk Level : {risk}")

    if student["attendance"] < 75:
        print("⚠ Attendance is below 75%.")

    if student["cgpa"] < 6.5:
        print("⚠ CGPA needs improvement.")

    if student["arrears"] > 0:
        print(f"⚠ Student has {student['arrears']} arrear(s).")

    if risk_score == 0:
        print("✓ Student is performing well.")

    print("-" * 55)


# --------------------------------------------------
# GEMINI AI ASSISTANT
# --------------------------------------------------

def ask_ai(student, question):

    prompt = f"""
You are an AI Student Support Assistant.

Use the following student information to provide a helpful,
clear and practical answer.

Student Information:
Name: {student['name']}
Department: {student['department']}
Year: {student['year']}
CGPA: {student['cgpa']}
Attendance: {student['attendance']}%
Arrears: {student['arrears']}

Student Question:
{question}

Instructions:
1. Give personalized advice based on the student's information.
2. Keep the answer easy to understand.
3. Give practical steps whenever possible.
4. Encourage the student positively.
5. Do not make up student information.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini API Error: {e}"


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

def main():

    print("\n")
    print("=" * 55)
    print("        AI STUDENT SUPPORT ASSISTANT")
    print("=" * 55)

    student_id = input("\nEnter Student ID: ").strip().upper()

    if student_id not in students:

        print("\n❌ Student ID not found.")
        print("Available Student IDs:")
        print("STU001")
        print("STU002")
        return

    student = students[student_id]

    display_student(student)

    risk_analysis(student)

    print("\n")
    print("=" * 55)
    print("              AI STUDENT SUPPORT")
    print("=" * 55)

    print("\nYou can ask questions such as:")
    print("- How can I improve my CGPA?")
    print("- How can I improve my attendance?")
    print("- Give me a study plan.")
    print("- How can I prepare for exams?")
    print("- What should I do about my arrears?")
    print("- Give me career advice.")

    print("\nType 'exit' to close the assistant.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("\nThank you for using AI Student Support Assistant!")
            break

        if not question:
            print("Please enter a question.")
            continue

        print("\nAI Assistant: ")

        answer = ask_ai(student, question)

        print(answer)


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    main()