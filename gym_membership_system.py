"""Fitness gym membership registration and renewal module."""

import hashlib
import json
import os
import secrets

MEMBERS = {
    "M01": {"name": "Alex", "plan": "Gold", "months_left": 6, "fee": 600.0},
    "M02": {"name": "Brooke", "plan": "Silver", "months_left": 1, "fee": 350.0},
    "M03": {"name": "Chris", "plan": "Platinum", "months_left": 12, "fee": 1000.0},
}
MEMBER_LOG = []
MONTHLY_FEE = 50.0

def register_member(m_id, name, plan, months, member_log=None):
    """Register a member; return False if the ID exists or months <= 0."""
    if member_log is None:
        member_log = MEMBER_LOG
    if m_id in MEMBERS or months <= 0:
        return False
    MEMBERS[m_id] = {
        "name": name,
        "plan": plan,
        "months_left": months,
        "fee": MONTHLY_FEE * months,
    }
    member_log.append(f"Registered {m_id} for {months} months")
    return True

def cancel_membership(m_id):
    """Remove a member if present; do nothing if the ID is unknown."""
    MEMBERS.pop(m_id, None)

def check_membership_status(m_id):
    """Return True if the member exists and has months remaining."""
    member = MEMBERS.get(m_id)
    return member is not None and member["months_left"] > 0

def calculate_renewal_rate(m_id, discount):
    """Return the renewal fee after applying a discount fraction (0 to 1)."""
    if not 0 <= discount <= 1:
        raise ValueError("discount must be between 0 and 1")
    return MEMBERS[m_id]["fee"] * (1 - discount)

def generate_member_hash(m_id):
    """Return a SHA-256 hex digest for the member ID."""
    return hashlib.sha256(m_id.encode()).hexdigest()

def generate_locker_pin():
    """Return a cryptographically secure 4-digit locker PIN."""
    return 1000 + secrets.randbelow(9000)

def export_member_roster(filename="gym_roster.txt"):
    """Write the roster to ``filename`` as JSON."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        json.dump(MEMBERS, roster_file, indent=2)
    print(f"Roster exported to: {filename}")

def get_active_summary(roster):
    """Return the number of members with months remaining."""
    return sum(1 for details in roster.values() if details["months_left"] > 0)

def main():
    """Run a demonstration of the membership system."""
    gym_api_secret = os.environ.get("GYM_API_SECRET")
    register_member("M04", "Diana", "Gold", 3)
    cancel_membership("M02")
    print("Is M01 active:", check_membership_status("M01"))
    print("Renewal Fee:", calculate_renewal_rate("M01", 0.15))
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())
    export_member_roster()
    print("Active count:", get_active_summary(MEMBERS))
    print("Portal secret configured:", gym_api_secret is not None)

if __name__ == "__main__":
    main()
