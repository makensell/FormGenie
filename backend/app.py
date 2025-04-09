from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
import time
import names
import string

app = Flask(__name__)
CORS(app)

# Generate random email, age, and address
def generate_email(name):
    domains = ["@gmail.com", "@yahoo.com", "@outlook.com"]
    return name.lower().replace(" ", "") + str(random.randint(10, 999)) + random.choice(domains)

def generate_age():
    return str(random.randint(18, 45))

def generate_address():
    streets = ["MG Road", "Park Street", "Brigade Road", "Linking Road", "Hilltop Area"]
    cities = ["Delhi", "Bangalore", "Mumbai", "Hyderabad", "Chennai"]
    return f"{random.randint(101, 999)}, {random.choice(streets)}, {random.choice(cities)}"

def get_random_delay(speed):
    if speed == "fast":
        return random.uniform(0.5, 1)
    elif speed == "medium":
        return random.uniform(1.5, 2.5)
    else:  # slow
        return random.uniform(3, 4)

@app.route('/fill-form', methods=['POST'])
def fill_form():
    data = request.get_json()
    form_link = data.get("formLink")
    response_count = int(data.get("responseCount", 1))
    speed = data.get("speed", "medium")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")

    for _ in range(response_count):
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(form_link)
        time.sleep(get_random_delay(speed))

        questions = driver.find_elements(By.CSS_SELECTOR, "div[role='list'] > div")
        for q in questions:
            try:
                # Text inputs (name, age, etc.)
                input_field = q.find_element(By.CSS_SELECTOR, "input[type='text']")
                label = q.text.lower()

                if "name" in label:
                    value = names.get_full_name()
                elif "email" in label:
                    name_for_email = names.get_first_name()
                    value = generate_email(name_for_email)
                elif "age" in label:
                    value = generate_age()
                elif "address" in label:
                    value = generate_address()
                else:
                    value = "Sample Answer"

                input_field.send_keys(value)
                time.sleep(get_random_delay(speed))

            except:
                try:
                    # Multiple choice options
                    options = q.find_elements(By.CSS_SELECTOR, "div[role='radio']")
                    if options:
                        weights = [0.6, 0.3, 0.1] + [0.05] * (len(options) - 3)
                        choice = random.choices(options, weights=weights[:len(options)], k=1)[0]
                        driver.execute_script("arguments[0].click();", choice)
                        time.sleep(get_random_delay(speed))
                except:
                    pass

        try:
            submit_btn = driver.find_element(By.XPATH, "//span[text()='Submit']/ancestor::div[@role='button']")
            driver.execute_script("arguments[0].click();", submit_btn)
            time.sleep(2)
        except:
            driver.quit()
            return jsonify({"message": "Form submission failed. Could not find the submit button."}), 500

        driver.quit()

    return jsonify({"message": "<span class='text-light-cyan-400 font-semibold'>😁 Form filled successfully </span>"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
