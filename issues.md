# Issues Identified by Static Analysis Tools

## Issue Table

| # | Issue | Type | Tool | Line(s) | Severity | Description | Fix Approach |
|---|-------|------|------|---------|----------|-------------|--------------|
| 1 | Use of `eval()` | Security (B307) | Bandit | 44 | Medium | `eval(gpa_expr)` executes arbitrary code passed as a string argument, allowing potential code injection attacks. | Removed `eval()` entirely; computed GPA directly as `avg_score / 20.0` using safe arithmetic. |
| 2 | Weak MD5 hash | Security (B324) | Bandit | 49 | High | `hashlib.md5()` is a weak, collision-prone hashing algorithm unsuitable for security purposes. | Replaced with `hashlib.sha256()`, a cryptographically stronger hash function. |
| 3 | Shell injection via `os.system()` | Security (B605) | Bandit | 60 | High | `os.system("echo ... " + filename)` passes user-controlled input to a shell, enabling command injection. | Replaced `os.system()` call with a safe `print()` statement—no shell needed just to display a message. |
| 4 | Hardcoded password/token | Security (B105) | Bandit | 64 | Low | `portal_token = "ADMIN_GRADE_PORTAL_TOKEN_2026"` embeds a sensitive credential directly in source code. | Replaced with `os.environ.get("GRADE_PORTAL_TOKEN", "NOT_SET")` to read the token from an environment variable. |
| 5 | Insecure pseudo-random generator | Security (B311) | Bandit | 53 | Low | `random.randint()` uses a non-cryptographic PRNG, unsuitable for generating security-sensitive PINs. | Replaced with `secrets.randbelow()` from the `secrets` module, which is cryptographically secure. |
| 6 | Bare `except` / try-except-pass | Bug (B110, W0702, E722) | Bandit, Pylint, Flake8 | 26 | Low | `except: pass` silently swallows all exceptions (including `KeyboardInterrupt`, `SystemExit`), hiding bugs. | Changed to `except KeyError:` with an informative error message via `print()`. |
| 7 | Mutable default argument | Bug (W0102) | Pylint | 15 | Warning | `grade_list=[]` is shared across all calls—appended items persist between invocations. | Changed default to `None` and initialized a new list inside the function body. |
| 8 | Unused variable `grace_marks` | Code Quality (W0612, F841) | Pylint, Flake8 | 31 | Warning | `grace_marks = 5.0` is assigned but never used, indicating dead code or an incomplete feature. | Removed the unused variable. |
| 9 | Unused variable `avg_score` in `compute_weighted_gpa` | Code Quality (W0612, F841) | Pylint, Flake8 | 43 | Warning | `avg_score` was computed but not referenced in the `eval()` expression's local scope (only visible to `eval`). | After removing `eval()`, `avg_score` is now used directly in the GPA calculation. |
| 10 | Unused import `json` | Code Quality (W0611, F401) | Pylint, Flake8 | 6 | Warning | The `json` module was imported but never used anywhere in the code. | Removed the import statement. |
| 11 | `None` comparison with `==` | Style (C0121, E711) | Pylint, Flake8 | 32 | Convention | `== None` should be `is None` per PEP 8; `is` checks identity, which is correct for singletons. | Changed to `is None`. |
| 12 | Function name `addGrade` not snake_case | Style (C0103) | Pylint | 15 | Convention | Python naming convention (PEP 8) requires `snake_case` for function names. | Renamed to `add_grade`. |
| 13 | Missing docstrings | Style (C0116) | Pylint | 15,23,30,41,48,52,56,63 | Convention | All eight functions lacked docstrings, reducing readability and maintainability. | Added descriptive docstrings to every function. |
| 14 | %-formatting instead of f-string | Style (C0209) | Pylint | 19 | Convention | Old-style `%` string formatting; f-strings are more readable and preferred in modern Python. | Converted to an f-string. |
| 15 | Simplifiable if-else return | Refactor (R1703, R1705) | Pylint | 35-38 | Refactor | `if cond: return True else: return False` can be simplified to `return cond`. | Simplified to `return avg >= pass_threshold`. |
| 16 | File opened without `with` / missing encoding | Refactor (R1732, W1514) | Pylint | 57 | Refactor | `open()` without a `with` block risks resource leaks; missing `encoding` parameter uses platform default. | Wrapped in `with open(..., encoding="utf-8") as file:`. |
| 17 | Lines too long (>79 chars) | Formatting (E501) | Flake8 | 19, 34 | Style | Two lines exceeded the PEP 8 recommended 79-character limit. | Reformatted the lines to fit within 79 characters. |
| 18 | Missing final newline | Formatting (C0304, W292) | Pylint, Flake8 | 75 | Style | File did not end with a newline character, violating POSIX convention. | Added a trailing newline. |
| 19 | `main()` called at module level | Design | Manual | 75 | Logic | `main()` runs on import—makes the module non-importable as a library without side effects. | Wrapped in `if __name__ == "__main__":` guard. |

