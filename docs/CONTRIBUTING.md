

# Contributing to FairoTrials Validators

Thank you for your interest in contributing to **FairoTrials Validators**!  
This project is part of the **POSE Phase I** educational and research prototype to promote transparency and traceability in clinical trials.  

We welcome small contributions that improve clarity, usability, or educational value.

---

## 1. Cloning the Repository

```bash
git clone https://github.com/mattvassar-ux/fairotrials-validators.git
cd fairotrials-validators
````

---

## 2. Setting Up the Environment

You can run the validators either with **Python** or **Docker**.

### 🐍 Python Setup

1. Ensure you have **Python 3.10+** installed.
2. Install the package locally:

```bash
pip install -e .
```

3. Verify installation:

```bash
fairo --help
```

### 🐳 Docker Setup

If you prefer Docker:

```bash
docker build -t fairotrials-validators .
docker run --rm fairotrials-validators fairo --help
```

---

## 3. Running All Validators

Each validator can be executed from the command line. Example:

```bash
fairo-fair-meta
fairo-fdaaa
fairo-accessible
fairo-outcomes
fairo-harms
fairo-linkage
fairo-data-sharing
```

Alternatively, you can run the main CLI to execute multiple validators in sequence:

```bash
fairo
```

Output CSV files will be created in the current directory.

---

## 4. Contributing via Issues and Pull Requests

We welcome:

* Bug reports
* Documentation improvements
* Simple code or test enhancements

### To contribute:

1. **Open an issue** describing your suggestion or bug.
2. **Create a new branch** for your fix or feature.
3. **Submit a pull request** (PR) linking to the issue.

Make sure your PR passes all tests before submission.

---

## 5. Educational and Research Context

This repository is a **prototype developed under POSE Phase I**.
Its purpose is **educational** — to demonstrate minimal viable validators for transparency in clinical trials.
While the code is functional, it is **not intended for production use**.

---

## 6. Testing Your Changes

We use **pytest** for testing. To run all tests:

```bash
pytest
```

Please ensure all tests pass before creating a pull request.

---

## Thank You!

Your contributions help make clinical trial transparency tools more accessible and understandable for the research community.


