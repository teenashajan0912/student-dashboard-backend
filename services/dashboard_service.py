from query.student_query import fetch_students

async def get_dashboard_service(db):

    students = fetch_students(db)

    summary = {
        "Low": {"Male": 0, "Female": 0, "Avg_Attendance": 0, "Avg_Hours_Studied": 0, "count": 0},
        "Medium": {"Male": 0, "Female": 0, "Avg_Attendance": 0, "Avg_Hours_Studied": 0, "count": 0},
        "High": {"Male": 0, "Female": 0, "Avg_Attendance": 0, "Avg_Hours_Studied": 0, "count": 0},
    }

    for s in students:

        if s.Exam_Score <= 50:
            category = "Low"
        elif s.Exam_Score <= 75:
            category = "Medium"
        else:
            category = "High"

        summary[category]["count"] += 1

        if s.Gender == "Male":
            summary[category]["Male"] += 1
        else:
            summary[category]["Female"] += 1

        summary[category]["Avg_Attendance"] += s.Attendance
        summary[category]["Avg_Hours_Studied"] += s.Hours_Studied

    result = []

    for key, val in summary.items():

        count = val["count"] if val["count"] > 0 else 1

        result.append({
            "Performance": key,
            "Male": val["Male"],
            "Female": val["Female"],
            "Avg_Attendance": val["Avg_Attendance"] / count,
            "Avg_Hours_Studied": val["Avg_Hours_Studied"] / count,
        })

    return result

async def physical_activity_service(db):

    students = fetch_students(db)

    activity_count = {}

    for s in students:

        activity = (
            s.Physical_Activity
            or "Unknown"
        )

        activity_count[activity] = (
            activity_count.get(activity, 0) + 1
        )

    result = [
        {
            "name": k,
            "value": v
        }
        for k, v in activity_count.items()
    ]

    return result