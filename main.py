import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from decorator import logger

driver = webdriver.Chrome()

url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
driver.get(url)

vacancy_urls = []

vacancy_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/vacancy/") and not(contains(@href, "advanced")) and not(contains(@href, "map"))]')

for link in vacancy_links:
    vacancy_urls.append(link.get_attribute('href'))

vacancies = []

@logger('scraping.log')  # Декорируем функцию логгером, указываем путь к файлу 'scraping.log'
def scrape_vacancy(vacancy_url):
    driver.get(vacancy_url)
    company = driver.find_element(By.CSS_SELECTOR, ".vacancy-company-name").text
    try:
        salary_element = driver.find_element(By.CSS_SELECTOR, ".vacancy-salary")
        salary = salary_element.text.strip()
    except NoSuchElementException:
        salary = "Не указано"
    try:
        city_element = driver.find_element(By.CSS_SELECTOR, ".vacancy-company-address-text")
        city = city_element.text.strip()
    except NoSuchElementException:
        city = "Не указан"
    description = driver.find_element(By.CSS_SELECTOR, ".vacancy-description").text
    if "Django" in description and "Flask" in description:
        vacancies.append({
            "url": vacancy_url,
            "company": company,
            "city": city,
            "salary": salary
        })

for vacancy_url in vacancy_urls:
    scrape_vacancy(vacancy_url)

driver.quit()

with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

print("Информация о подходящих вакансиях успешно записана в vacancies.json")
