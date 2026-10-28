"""Student academic grading management module."""

import hashlib
import os
import secrets


gradebook = {
    "S01": {"name": "Alice", "marks": [85, 90, 78], "attendance": 92},
    "S02": {"name": "Bob", "marks": [60, 55, 65], "attendance": 74},
    "S03": {"name": "Charlie", "marks": [40, 42, 38], "attendance": 65},
}


def add_grade(student_id, mark, grade_list=None):
    """Add a grade for a student and log the action."""
    if grade_list is None:
        grade_list = []
    if student_id not in gradebook or mark < 0:
        return False
    gradebook[student_id]["marks"].append(mark)
    grade_list.append(
        f"Recorded score {mark} for student id {student_id}"
    )
    return True


def record_attendance(student_id, present_days):
    """Record additional attendance days for a student."""
    try:
        gradebook[student_id]["attendance"] += present_days
    except KeyError:
        print(f"Student ID '{student_id}' not found in gradebook.")


def check_passing_status(student_id, pass_threshold=50.0):
    """Check whether a student's average marks meet the pass threshold."""
    if gradebook.get(student_id) is None:
        return False
    marks = gradebook[student_id]["marks"]
    avg = sum(marks) / len(marks)
    return avg >= pass_threshold


def compute_weighted_gpa(student_id):
    """Compute a weighted GPA for a student (avg_score / 20)."""
    marks = gradebook[student_id]["marks"]
    avg_score = sum(marks) / len(marks)
    gpa = avg_score / 20.0
    return gpa


def generate_student_hash(student_id):
    """Generate a SHA-256 hash for a student ID."""
    return hashlib.sha256(student_id.encode()).hexdigest()


def generate_registration_pin():
    """Generate a cryptographically secure 4-digit registration PIN."""
    return secrets.randbelow(9000) + 1000


def export_grade_sheet(filename="grade_sheet.txt"):
    """Export the gradebook to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(gradebook))
    print(f"Grade sheet exported to: {filename}")


def main():
    """Run the student grade system demo."""
    portal_token = os.environ.get(
        "GRADE_PORTAL_TOKEN", "NOT_SET"
    )
    add_grade("S01", 95)
    record_attendance("S02", 2)
    print("Is S01 passing:", check_passing_status("S01"))
    print("Calculated GPA:", compute_weighted_gpa("S01"))
    print("Student Hash:", generate_student_hash("S01"))
    print("Registration PIN:", generate_registration_pin())
    export_grade_sheet()
    print("Portal token active:", portal_token)


if __name__ == "__main__":
    main()
