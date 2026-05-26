
import requests
import secrets
import string
import os
import logging
import http.client

# Enable HTTP debugging
http.client.HTTPConnection.debuglevel = 1

# Set up logging
logging.basicConfig(filename='test.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Read API configuration from utils/api.py
API_BASE_URL = os.environ.get("API_BASE_URL")
INSTANCE = os.environ.get("XANO_INSTANCE", "x8ki-letl-twmt")
BASE_URL = API_BASE_URL.rstrip("/") if API_BASE_URL else f"https://{INSTANCE}.n7.xano.io/api"

GROUP_ENDPOINTS = {
    "auth": "W7Js3LqF",
    "subjects": "22fejpGr",
    "academic_tasks": "ixTSf5fW",
}

GROUPS = {
    group: f"{BASE_URL}:{endpoint}"
    for group, endpoint in GROUP_ENDPOINTS.items()
}

def generate_random_string(length=10):
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

def main():
    # --- Test Data ---
    random_part = generate_random_string()
    test_user = {
        "name": f"Test User {random_part}",
        "email": f"testuser_{random_part}@example.com",
        "password": "password123"
    }
    auth_token = None

    headers = {"Content-Type": "application/json"}

    # 1. Sign up a new user
    logging.info(f"1. Signing up new user: {test_user['email']}")
    try:
        signup_url = f"{GROUPS['auth']}/signup"
        resp = requests.post(signup_url, json=test_user)
        resp.raise_for_status()
        data = resp.json()
        auth_token = data.get("authToken", data.get("auth_token"))
        if auth_token:
            logging.info("   -> Signup successful.")
            headers["Authorization"] = f"Bearer {auth_token}"
        else:
            logging.error(f"   -> Signup failed: 'authToken' not in response: {data}")
            return
    except requests.exceptions.RequestException as e:
        logging.error(f"   -> Signup failed: {e}")
        if e.response:
            logging.error(f"   -> Response: {e.response.text}")
        return

    # 2. Log in with the new user
    logging.info(f"2. Logging in as: {test_user['email']}")
    try:
        login_url = f"{GROUPS['auth']}/login"
        login_payload = {"email": test_user["email"], "password": test_user["password"]}
        resp = requests.post(login_url, json=login_payload)
        resp.raise_for_status()
        data = resp.json()
        auth_token = data.get("authToken", data.get("auth_token"))
        if auth_token:
            logging.info("   -> Login successful.")
            headers["Authorization"] = f"Bearer {auth_token}"
        else:
            logging.error(f"   -> Login failed: 'authToken' not in response: {data}")
            return
    except requests.exceptions.RequestException as e:
        logging.error(f"   -> Login failed: {e}")
        if e.response:
            logging.error(f"   -> Response: {e.response.text}")
        return

    # 3. Create a new subject
    logging.info("3. Creating a new subject")
    subject_id = None
    try:
        subjects_url = f"{GROUPS['subjects']}/subjects"
        subject_payload = {
            "name": f"Test Subject {random_part}",
            "teacher": "Dr. Test",
            "semester": "2026/2"
        }
        resp = requests.post(subjects_url, headers=headers, json=subject_payload)
        resp.raise_for_status()
        data = resp.json()
        subject_id = data.get("id")
        if subject_id:
            logging.info(f"   -> Subject created successfully (ID: {subject_id}).")
        else:
            logging.error(f"   -> Subject creation failed: 'id' not in response: {data}")
            return
    except requests.exceptions.RequestException as e:
        logging.error(f"   -> Subject creation failed: {e}")
        if e.response:
            logging.error(f"   -> Response: {e.response.text}")
        return

    # 4. Create a new academic task
    logging.info("4. Creating a new academic task")
    try:
        tasks_url = f"{GROUPS['academic_tasks']}/academic_tasks"
        task_payload = {
            "title": f"Test Task {random_part}",
            "subject_id": subject_id,
            "due_date": "2026-12-31T23:59:59Z",
            "status": "Pendente",
            "priority": "Média"
        }
        resp = requests.post(tasks_url, headers=headers, json=task_payload)
        resp.raise_for_status()
        data = resp.json()
        task_id = data.get("id")
        if task_id:
            logging.info(f"   -> Task created successfully (ID: {task_id}).")
        else:
            logging.error(f"   -> Task creation failed: 'id' not in response: {data}")
            return
    except requests.exceptions.RequestException as e:
        logging.error(f"   -> Task creation failed: {e}")
        if e.response:
            logging.error(f"   -> Response: {e.response.text}")
        return

    logging.info("\n✅ All API tests passed!")
    print("Test finished. Check test.log for results.")

if __name__ == "__main__":
    main()
