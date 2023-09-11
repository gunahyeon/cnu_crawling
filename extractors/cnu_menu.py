from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime


def extract_menu(language):
    menu_data = {}
    results = []
    chrome_options = webdriver.ChromeOptions()        
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")    
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)

    base_url = "https://dorm.cnu.ac.kr/html/kr/sub03/sub03_0304.html"
    browser.get(f"{base_url}")


    today_day = datetime.now().strftime(" %d").replace(" 0", "")
    # today_weekday = datetime.now().strftime("%a")

    soup = BeautifulSoup(browser.page_source, "html.parser")

    menu_table = soup.find("table", class_="diet_table")
    menu_list = menu_table.find("tbody", recursive=False)
    menus = menu_list.find_all("tr", recursive=False)

    for menu in menus:
        days = menu.select_one("td:nth-of-type(1)").get_text()
        morning = menu.select_one("td:nth-of-type(2)").get_text()
        lunch = menu.select_one("td:nth-of-type(3)").get_text()
        dinner = menu.select_one("td:nth-of-type(4)").get_text()

        if today_day.strip() in days:
            menu_data = {
                "days" : days,
                "morning" : morning,
                "lunch" : lunch,
                "dinner" : dinner
            }
            results.append(menu_data)

    result = []
    for entry in results:
        day_info = {'days': entry['days']}
        for meal_time in ['morning', 'lunch', 'dinner']:
            if meal_time in entry:
                splits = entry[meal_time].split("\n\n")
                
                if language == 'kor':
                    kor_menus = [menu for menu in splits if not all(char.isascii() for char in menu)]
                    day_info[f'{meal_time}_kor'] = "\n\n".join(kor_menus)

                if language == 'eng':
                    eng_menus = [menu for menu in splits if all(char.isascii() for char in menu)]
                    day_info[f'{meal_time}_eng'] = "\n\n".join(eng_menus)
                
        result.append(day_info)        

    browser.quit()
    return result



