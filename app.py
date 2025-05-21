from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

@app.route('/search-images', methods=['POST'])
def search_images():
    words = request.json.get('words', [])
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    results = {}

    for word in words:
        driver.get(f"https://www.google.com/search?tbm=isch&q={word}")
        time.sleep(2)
        imgs = driver.find_elements("tag name", "img")[1:6]
        urls = [img.get_attribute('src') for img in imgs if img.get_attribute('src')]
        results[word] = urls

    driver.quit()
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
