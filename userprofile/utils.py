from datetime import date
import requests
from django.conf import settings
import re

def call_groq_api(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",  # Correct model
        "messages": [
            {"role": "system", "content": "You are a certified fitness coach and dietitian."},
            {"role": "user", "content": str(prompt)}
        ],
        "max_tokens": 1024,
        "temperature": 0.7,
    }

    response = requests.post(url, headers=headers, json=payload)

    # Log error info if request fails
    if response.status_code != 200:
        print("Status Code:", response.status_code)
        print("Headers:", response.headers)
        print("Response:", response.text)
        response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def generate_diet_prompt(user_profile):
    age = calculate_age(user_profile.date_of_birth)
    bmi = user_profile.calculate_bmi()

    prompt = f"""
    Create a 7-day personalized **diet plan** for this individual.

    Name: {user_profile.first_name} {user_profile.last_name}
    Age: {age}
    Height: {user_profile.height} cm
    Weight: {user_profile.weight} kg
    BMI: {bmi}
    Food Habits: {user_profile.food_habits}
    Smoking: {"Yes" if user_profile.smoking else "No"}
    Alcohol: {"Yes" if user_profile.alcohol else "No"}
    Workout Experience: {user_profile.workout_experience}

    ✅ Output format:
    Return the plan as a **Markdown table**.
    - Rows: Days of the week (Monday to Sunday)
    - Columns: Breakfast, Lunch, Snacks, Drinks

    Provide healthy, easy-to-make meal ideas and portions tailored to the person’s health and lifestyle.
    """
    return prompt

def generate_workout_prompt(user_profile):
    age = calculate_age(user_profile.date_of_birth)
    bmi = user_profile.calculate_bmi()

    prompt = f"""
    Create a 7-day personalized **workout plan** for this individual.

    Name: {user_profile.first_name} {user_profile.last_name}
    Age: {age}
    Height: {user_profile.height} cm
    Weight: {user_profile.weight} kg
    BMI: {bmi}
    Workout Experience: {user_profile.workout_experience}

    ✅ Output format:
    Return the plan as a **Markdown table**.
    - Rows: Days of the week (Monday to Sunday)
    - Columns: Warm-up, Strength, Cardio, Cool-down

    Ensure the plan is achievable, safe, and varied. Include brief exercise names or types under each section.
    """
    return prompt

def parse_diet_response(response_text):
    table_lines = []
    lines = response_text.strip().splitlines()
    in_table = False
    for line in lines:
        if re.match(r'^\| *Day *\|', line):
            in_table = True
        elif in_table and line.strip() == "":
            break
        if in_table:
            table_lines.append(line)

    if not table_lines or len(table_lines) < 3:
        return {}  

    # Extract headers
    headers = [h.strip().lower() for h in table_lines[0].split('|')[1:-1]]

    # Extract rows
    diet_table = {}
    for row in table_lines[2:]:  # skip header + separator
        if '---' in row:
            continue
        cells = [c.strip() for c in row.split('|')[1:-1]]
        if len(cells) != len(headers):
            continue
        day = cells[0]
        diet_table[day] = {
            headers[i]: cells[i] for i in range(1, len(headers))  # skip day column
        }

    return diet_table

def parse_workout_response(response_text):
    table_lines = []
    lines = response_text.strip().splitlines()

    # Find where the markdown table starts and ends
    in_table = False
    for line in lines:
        if re.match(r'^\| *Day *\|', line):
            in_table = True
        elif in_table and line.strip() == "":
            break
        if in_table:
            table_lines.append(line)

    if not table_lines or len(table_lines) < 3:
        return {}

    # Extract headers
    headers = [h.strip().lower() for h in table_lines[0].split('|')[1:-1]]

    # Extract rows
    workout_table = {}
    for row in table_lines[2:]:  # skip header and separator
        if '---' in row:
            continue
        cells = [c.strip() for c in row.split('|')[1:-1]]
        if len(cells) != len(headers):
            continue
        day = cells[0]
        workout_table[day] = {
            headers[i]: cells[i] for i in range(1, len(headers))
        }

    return workout_table