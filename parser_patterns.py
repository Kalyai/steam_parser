from selenium.common import NoSuchElementException, ElementClickInterceptedException, TimeoutException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from bluegems import tier1, tier2, tier3
from chrome import driver_init

def create_file(url, find_patterns):
    itemname = url.split('/')[-1].split('%20')
    gunname = itemname[0] + '-' + itemname[1]
    skinname = itemname[3] + '-' + itemname[4]
    wear = itemname[5].replace('%28', '') + '-' + itemname[6].replace('%29', '') if len(itemname) > 6 else itemname[
        5].replace('%28', '').replace('%29', '')
    filename = f'{gunname}_{skinname}_{wear}'

    with open(f'patterns_info/{filename}.txt', 'w') as file:
        file.write(f'top1: 490, top2: 148 69 704\n')
        for tier, patterns in find_patterns.items():
            file.write(f'Тиер {tier}\n')
            for pattern, price_list in patterns.items():
                file.write(f'{pattern}: {price_list}\n')


def click_button(driver, by_type, identifier, delay=10):
    try:
        button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((by_type, identifier)))
        button.click()
        return True

    except (ElementClickInterceptedException, TimeoutException):
        print(f"Не удалось нажать на кнопку {identifier}. Повтор через 1 секунду")
        time.sleep(1)
        return False

def parsing(url):
    driver = driver_init()
    driver.get(url)
    find_patterns = {1: {}, 2: {}, 3: {}}
    page = 1
    file_created = False

    def select_100_items(driver):
        # Открыть меню для выбора 100 предметов
        while not click_button(driver, By.ID, "ui-id-1-button"):
            pass

        # Выбрать 100 предметов
        while not click_button(driver, By.ID, "ui-id-8"):
            pass

    select_100_items(driver)
    print(f"Выбрано 100 предметов")

    while True:
        time.sleep(3)
        try:
            driver.find_element(By.CSS_SELECTOR, "a.sih_button.next_page.disabled")

        except NoSuchElementException:
            pass
        else: break

        try:
            driver.find_element(By.CLASS_NAME, "sih_label.sih_label_warning")

        except NoSuchElementException:
            pass
        else:
            print("Ошибка стим 429 (слишком частный запрос)")
            time.sleep(5)
            driver.quit()
            time.sleep(15)
            parsing(url)
            break

        # Убеждаемся, что элементы подгрузились
        try:
            print(f'Страница {page} Обрабатывается')
            WebDriverWait(driver, 60).until(
                lambda d: len([s.text for s in d.find_elements(By.CLASS_NAME, "itemseed") if s.text != '']) == 100
            )
            WebDriverWait(driver, 60).until(
                lambda d: len([p.text for p in
                               d.find_elements(By.CSS_SELECTOR, "div.market_listing_right_cell.market_listing_their_price")
                               if p.text != '']) == 100
            )

            # Сбор данных
            seeds = driver.find_elements(By.CLASS_NAME, "itemseed")
            prices = driver.find_elements(By.CSS_SELECTOR, "div.market_listing_right_cell.market_listing_their_price")

            for seed, price in zip(seeds, prices):
                seed_val = seed.text.split(':')[1].strip()
                tier = 1 if int(seed_val) in tier1 else 2 if int(seed_val) in tier2 else 3 if int(
                    seed_val) in tier3 else None
                if tier:
                    find_patterns[tier].setdefault(seed_val, []).append(price.text)

            if len(find_patterns[1]) >= 5 and len(find_patterns[2]) >= 5 and len(find_patterns[3]) >= 5:
                file_created = True
                create_file(url, find_patterns)
                break

            page += 1
            click_button(driver, By.CSS_SELECTOR, "a.sih_button.next_page")

        except StaleElementReferenceException:
            print("Ошибка StaleElementReferenceException - старый элемент не найден, пробуем спарсить страницу заново")
            time.sleep(1)

        except TimeoutException:
            print("Ошибка TimeoutException - страница не загрузилась, пробуем спарсить страницу заново")
            time.sleep(1)

        except Exception as e:
            print(f"Новая ошибка: {e}, пробуем спарсить страницу заново")
            time.sleep(1)

    # Печать данных по паттернам
    if not file_created:
        create_file(url, find_patterns)

    for tier, patterns in find_patterns.items():
        print(f'Тиер {tier}')
        for pattern, price_list in patterns.items():
            print(f'{pattern}: {price_list}')

    # Закрытие драйвера
    driver.quit()
