
# Lab 04 — Build a Tiny Validator

## Goal
Implement one simple rule using the template and write a unit test.

## Steps
1. Copy `validators/template_validator.py` → `validators/title_presence_validator.py`
2. Edit `REQUIRED_FIELDS = ["trial_id","title"]` and inside `validate_record()` add:
   ```python
   title_ok = bool(rec.get("title"))
   row["has_title"] = title_ok
   if not title_ok:
       notes.append("missing_title")
   ```
3. Create `tests/test_title_presence_validator.py` by copying the template test and adjusting the import/filenames.
4. Run the test:
   ```powershell
   python -m pytest -q
   ```
