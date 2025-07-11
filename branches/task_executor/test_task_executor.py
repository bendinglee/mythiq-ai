from branches.task_executor.list_builder import build_checklist
from branches.task_executor.reminder_engine import generate_reminder
from branches.task_executor.summary_generator import summarize_text

def test_task_engine():
    reminder = generate_reminder("Meet with AI team at 2PM")
    checklist = build_checklist("Install Flask,Test route,Deploy endpoint")
    summary = summarize_text("AI is evolving rapidly. Large models are scaling. Feedback loops are essential.", "highlight")

    assert reminder["success"], "❌ Reminder failed"
    assert len(checklist["checklist"]) == 3, "❌ Checklist length mismatch"
    assert summary["style"] == "highlight", "❌ Summary style error"

    print("✅ Task Executor test passed.")

if __name__ == "__main__":
    test_task_engine()
