from django.shortcuts import render
from .models import AdmissionResult

from accounts.models import (
    Student,
    CBSEAcademicDetails,
    KeralaAcademicDetails,
    Extracurricular,
    CoursePreference
)

# =========================
# STREAM SCORE LOGIC
# =========================
def get_stream_score(student, course):

    cbse = CBSEAcademicDetails.objects.filter(student=student).first()
    kerala = KeralaAcademicDetails.objects.filter(student=student).first()

    grade_map = {
        "A+": 95, "A": 85,
        "B+": 75, "B": 65,
        "C+": 55, "C": 45,
        "D+": 35, "D": 25,
    }

    if course in ["Computer Science", "Bio-Mathematics"]:

        if cbse:
            return cbse.science + cbse.maths

        elif kerala:
            return (
                grade_map.get(kerala.physics, 0) +
                grade_map.get(kerala.chemistry, 0) +
                grade_map.get(kerala.biology, 0) +
                grade_map.get(kerala.mathematics, 0)
            )

    elif course == "Commerce":

        if cbse:
            return cbse.maths + cbse.social_science

        elif kerala:
            return (
                grade_map.get(kerala.mathematics, 0) +
                grade_map.get(kerala.social_science, 0)
            )

    elif course == "Humanities":

        if cbse:
            return cbse.social_science

        elif kerala:
            return grade_map.get(kerala.social_science, 0)

    return 0


# =========================
# MAIN CALCULATION
# =========================
def calculate_results(request=None):

    AdmissionResult.objects.all().delete()

    students = Student.objects.all()

    for student in students:

        bonus_mark = 0
        academic_score = 0

        cbse = CBSEAcademicDetails.objects.filter(
            student=student
        ).first()

        kerala = KeralaAcademicDetails.objects.filter(
            student=student
        ).first()

        # skip if no academic data
        if not cbse and not kerala:
            print(f"SKIPPED: {student.student_id} {student.name}")
            continue

        # academic score
        if cbse:
            academic_score = (cbse.total / 600) * 100
        else:
            academic_score = (kerala.total / 1000) * 100

        # extracurricular
        extra = Extracurricular.objects.filter(
            student=student
        ).first()

        if extra:

            if extra.sports_national:
                bonus_mark += 15
            elif extra.sports_state:
                bonus_mark += 10
            elif extra.sports_district:
                bonus_mark += 5

            if extra.youth_national:
                bonus_mark += 15
            elif extra.youth_state:
                bonus_mark += 10
            elif extra.youth_district:
                bonus_mark += 5

            if extra.ncc_nss_spc:
                bonus_mark += 5

        bonus_mark = min(bonus_mark, 20)

        # preferences
        preference = CoursePreference.objects.filter(
            student=student
        ).first()

        if not preference:
            print(f"NO PREFERENCE: {student.name}")
            continue

        courses = [
            preference.pref1,
            preference.pref2,
            preference.pref3
        ]

        # create results
        for i, course in enumerate(courses):

            if not course:
                continue

            stream_score = get_stream_score(student, course)

            final_score = academic_score + bonus_mark + stream_score

            AdmissionResult.objects.update_or_create(
                student=student,
                course=course,
                defaults={
                    "preference_order": i + 1,
                    "index_mark": academic_score,
                    "bonus_mark": bonus_mark,
                    "stream_score": stream_score,
                    "final_score": final_score,
                    "rank": 0,
                    "allotted": False
                }
            )

    # =========================
    # RANKING
    # =========================
    for course in [
        "Computer Science",
        "Bio-Mathematics",
        "Commerce",
        "Humanities"
    ]:

        results = AdmissionResult.objects.filter(
            course=course
        ).order_by(
            'preference_order',
            '-final_score',
            '-stream_score',
            '-bonus_mark',
            'student'
        )

        rank = 1

        for result in results:
            result.rank = rank
            result.save()
            rank += 1

    # =========================
    # ALLOTMENT (ONE STUDENT ONE SEAT)
    # =========================
    allotted_students = set()

    all_results = AdmissionResult.objects.all().order_by(
        'preference_order',
        'rank'
    )

    for result in all_results:

        sid = result.student.student_id

        if sid in allotted_students:
            continue

        result.allotted = True
        result.save()

        allotted_students.add(sid)

    print("CALCULATION COMPLETE ✔")

    if request:
        return render(request, 'calculation_done.html')


# =========================
# RANK LIST VIEW
# =========================
def rank_list(request):

    selected_course = request.GET.get('course')

    results = AdmissionResult.objects.filter(
        allotted=True
    )

    if selected_course:
        results = results.filter(course=selected_course)

    results = results.order_by('course', 'rank')

    return render(
        request,
        'rank_list.html',
        {
            'results': results,
            'selected_course': selected_course
        }
    )