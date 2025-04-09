from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import names
import threading

app = Flask(__name__)
CORS(app)

def fill_form(link, count, speed):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    for i in range(count):
        driver.get(link)
        time.sleep(random.uniform(1, 2))  # simulate loading

        inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        for input_box in inputs:
            if "name" in input_box.get_attribute('aria-label').lower():
                input_box.send_keys(names.get_full_name())
            elif "age" in input_box.get_attribute('aria-label').lower():
                input_box.send_keys(str(random.randint(18, 35)))
            elif "email" in input_box.get_attribute('aria-label').lower():
                input_box.send_keys(f"user{random.randint(100,999)}@example.com")
            elif "address" in input_box.get_attribute('aria-label').lower():
                input_box.send_keys("123, Random Street, India")
            else:
                input_box.send_keys("Sample Answer")

        # select radio buttons or checkboxes randomly
        choices = driver.find_elements(By.CSS_SELECTOR, 'div[role="radio"], div[role="checkbox"]')
        clicked = set()
        for choice in choices:
            if choice not in clicked and random.random() < 0.6:
                driver.execute_script("arguments[0].click();", choice)
                clicked.add(choice)

        submit_button = driver.find_element(By.XPATH, '//span[text()="Submit"]/..')
        driver.execute_script("arguments[0].click();", submit_button)

        time.sleep(speed)

    driver.quit()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    link = data.get('link')
    count = int(data.get('count', 1))
    speed = float(data.get('speed', 2))

    thread = threading.Thread(target=fill_form, args=(link, count, speed))
    thread.start()

    return jsonify({"message": "Form submission started!"}), 200

# ✅ New route to fix 404 error
@app.route('/')
def home():
    return "FormGenie backend is running ✅"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
