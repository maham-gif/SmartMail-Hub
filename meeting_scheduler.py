import json
from datetime import datetime, timedelta

USERS = ["alice", "bob", "charlie"]
START = datetime(2025, 7, 14, 9)
END = datetime(2025, 7, 14, 17)
DURATION_MINUTES = 30
EXISTING = {
    # user: list of (start, end)
    "alice": [(START + timedelta(hours=1), START + timedelta(hours=2))],
    "bob": [],
    "charlie": [(START + timedelta(hours=2), START + timedelta(hours=2, minutes=30))]
}

def find_free_slot(users, start, end, duration):
    slot = start
    while slot + timedelta(minutes=duration) <= end:
        end_slot = slot + timedelta(minutes=duration)
        if all(not any(s < end_slot and slot < e for s, e in EXISTING[u]) for u in users):
            return slot
        slot += timedelta(minutes=15)
    return None

def schedule_meeting(attendees):
    slot = find_free_slot(attendees, START, END, DURATION_MINUTES)
    if not slot:
        print("No common slot available.")
        return
    meeting = {
        "attendees": attendees,
        "start": slot.strftime("%Y-%m-%d %H:%M"),
        "end": (slot + timedelta(minutes=DURATION_MINUTES)).strftime("%Y-%m-%d %H:%M")
    }
    print("Scheduled meeting:", meeting)
    return meeting

if __name__ == "__main__":
    print("Scheduling for alice, bob, charlie...")
    schedule_meeting(["alice", "bob", "charlie"])
