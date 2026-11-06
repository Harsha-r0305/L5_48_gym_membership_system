# Issues Found – gym_membership_system.py

Rows are ordered by severity (high/medium first). Line numbers refer to the original file.
Tool IDs are the codes you should expect to see in your own reports; confirm them against your `*_report.txt` files.

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| `eval()` on caller-supplied string | Security (Bandit B307, High-risk) | 34-35 | `calculateRenewalRate` runs `eval(discount_expr)`, so any string passed in executes as arbitrary Python. | Removed `eval`. Function now takes a numeric `discount` (0-1) and computes `fee * (1 - discount)`, with range validation. |
| Shell command built from input (`os.system`) | Security (Bandit B605 / B607) | 56 | `os.system("echo ... " + filename)` allows shell injection via `filename` and starts a process via a partial path. | Replaced with `print(f"Roster exported to: {filename}")`. |
| Hardcoded secret | Security (Bandit B105) | 70 | `gym_api_secret = "GYM_CLOUD_PORTAL_SECRET_2026"` is committed to source control. It is also printed to the console at line 79. | Read from env var `GYM_API_SECRET`; the program only reports whether it is configured and never prints the value. |
| Weak hash (MD5) | Security (Bandit B324) | 42 | `hashlib.md5` is broken for security use. | Switched to `hashlib.sha256`. |
| Insecure random for PIN | Security (Bandit B311) | 46 | `random.randint` is predictable and unsuitable for a locker PIN. | Use `secrets.randbelow(9000) + 1000`. |
| Mutable default argument | Bug (Pylint W0102) | 14 | `member_log=[]` is created once and shared across every call. | Default to `None`; fall back to a module-level `MEMBER_LOG`. |
| Bare `except:` that swallows errors | Bug / Style (Pylint W0702, Flake8 E722) | 24-27 | Catches everything, including `KeyboardInterrupt`, and hides failures. | Replaced try/del/except with `MEMBERS.pop(m_id, None)`. |
| Unspecified file handling | Bug (Pylint R1732, W1514) | 52-55 | `open()` without `with`, so the file leaks if `write` fails; no encoding. | Use `with open(..., encoding="utf-8")` and `json.dump`. |
| Unused import `math` | Quality (Pylint W0611, Flake8 F401) | 5 | Imported but never used. | Removed. |
| Unused variable `locker_deposit` | Quality (Pylint W0612, Flake8 F841) | 30 | Assigned but never used. | Removed. |
| Comparison to `None` with `==` | Style (Flake8 E711, Pylint C0121) | 31 | Should use identity check. | Use `member is not None`. |
| Redundant `if/else: return True/False` | Quality (Pylint R1703 / R1705) | 33-37 | Four lines to return a boolean expression. | `return member is not None and member["months_left"] > 0`. |
| Redefined outer name `members` | Quality (Pylint W0621) | 61 | Parameter shadows the global `members`. | Parameter renamed `roster`; global renamed `MEMBERS`. |
| Unused loop variable `m` | Quality (Pylint W0612) | 63 | Key from `.items()` never used. | Iterate `.values()` via `sum(...)`. |
| camelCase function names | Style (Pylint C0103) | 13, 21, 28, 34 | Not PEP 8 snake_case. | Renamed `register_member`, `cancel_membership`, `check_membership_status`, `calculate_renewal_rate`. |
| Module-level constant naming | Style (Pylint C0103) | 7 | `members` global should be UPPER_CASE. | Renamed `MEMBERS`. |
| Missing docstrings | Quality (Pylint C0116) | all functions | No function docstrings. | Added one-line docstrings. |
| `%` string formatting | Style (Pylint C0209) | 17 | Old-style formatting. | f-string. |
| `main()` runs on import | Quality | 82 | Importing the module runs the demo. | Added `if __name__ == "__main__":` guard. |
| Missing blank lines / long lines | Style (Flake8 E302, E305, E501) | throughout | Functions not separated by two blank lines; long dict literals. | Applied PEP 8 spacing and wrapped long lines (commit 3). |

## Logic problems no tool will flag (worth mentioning if asked to present)

1. **Fee ignores the plan.** `register_member` always charges `50.0 * months`, so Diana (Gold, 3 months) pays 150.0 while Alex (Gold, 6 months) pays 600.0. Fees are not consistent with plan tiers. I did not change this because the intended tier prices are not defined anywhere. The fix would be a `PLAN_RATES` dict.
2. **No validation of plan names or unknown member IDs.** `calculate_renewal_rate("M99", ...)` raises a raw `KeyError`.
3. **`registerMember`'s log was lost** in the original unless the caller kept the shared mutable default alive; it is now an explicit module log.
