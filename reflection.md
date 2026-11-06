# Reflection

> The handout PDF you shared does not list the four reflection questions, so I used the standard ones for this lab. Replace the headings with your instructor's exact wording if it differs.

**1. Which issues were the easiest and hardest to fix?**
The easiest were the mechanical ones: removing the unused `math` import and `locker_deposit`, replacing `== None` with `is not None`, and adding blank lines and docstrings. The hardest was `eval(discount_expr)`. Simply deleting it would have broken the feature, so I had to change the function's interface to take a numeric discount and update the caller. The mutable default argument was also subtle, because the code "worked" until the list was shared across calls, and I had to decide where the log should live.

**2. Did the tools report any false positives or issues you disagreed with?**
Mostly the findings were accurate. Pylint's naming rule (C0103) flagged module-level `members` as a constant, which is debatable for a dictionary that is mutated at runtime, but I followed the convention for consistency. Bandit's hardcoded-secret check (B105) is heuristic and name-based, so it can miss secrets with innocuous variable names. Importantly, none of the tools noticed that every new member is charged `50 * months` regardless of plan. That bug only showed up from running the program and reading the output.

**3. How would you integrate static analysis into a real workflow?**
Run Flake8 and Pylint as a pre-commit hook for fast feedback, and run Bandit plus Pylint in CI (e.g. GitHub Actions) so a pull request fails on high-severity findings or when the Pylint score drops below a threshold such as 9.5. Developers would also run the tools in their editor so problems are caught while typing rather than at review time.

**4. What tangible improvements did static analysis bring to the code?**
Security: no code execution via `eval`, no shell injection, no secret in source or output, a modern hash, and a secure PIN generator. Reliability: no shared mutable state, files closed properly, and specific error handling instead of silently swallowed exceptions. Maintainability: consistent naming, docstrings, no dead code, and an importable module. The tools do not replace testing or code review, but they remove a whole class of problems cheaply and consistently.
