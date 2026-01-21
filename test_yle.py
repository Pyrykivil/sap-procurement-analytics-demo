import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json

def test_yle_basic():
    """Testaa Yle.fi-nettisivun perusominaisuuksia (HTTP-pyynnöt)"""
    
    print("\n" + "=" * 60)
    print("PERUS TESTIT - HTTP-PYYNNÖT")
    print("=" * 60)
    
    url = "https://yle.fi"
    
    try:
        # Testi 1: Sivuston saavutettavuus
        print("\n[Testi 1] Tarkistetaan sivuston saavutettavuus...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✓ Sivusto on saavutettavissa (Status: {response.status_code})")
        else:
            print(f"✗ Sivusto antoi virheen (Status: {response.status_code})")
            return
        
        # Testi 2: Sivun latausaika
        print("\n[Testi 2] Mitataan sivun latausaika...")
        start_time = time.time()
        response = requests.get(url, timeout=10)
        load_time = time.time() - start_time
        print(f"✓ Sivun latausaika: {load_time:.2f} sekuntia")
        
        # Testi 3: HTML-sisällön analyysi
        print("\n[Testi 3] Analysoidaan HTML-sisältöä...")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tarkista otsikko
        title = soup.find('title')
        if title:
            print(f"✓ Sivun otsikko: {title.string}")
        
        # Tarkista pääotsikoita (h1)
        h1_tags = soup.find_all('h1')
        if h1_tags:
            print(f"✓ Löydettiin {len(h1_tags)} pääotsikoita")
        
        # Tarkista linkkejä
        links = soup.find_all('a')
        print(f"✓ Löydettiin {len(links)} linkkiä")
        
        # Testi 4: Kuvan lataus
        print("\n[Testi 4] Tarkistetaan kuvia...")
        images = soup.find_all('img')
        print(f"✓ Löydettiin {len(images)} kuvaa")
        
        # Testi 5: Meta-tiedot
        print("\n[Testi 5] Tarkistetaan meta-tietoja...")
        meta_tags = soup.find_all('meta')
        print(f"✓ Löydettiin {len(meta_tags)} meta-tagia")
        
        description = soup.find('meta', attrs={'name': 'description'})
        if description:
            print(f"✓ Sivun kuvaus: {description.get('content', 'N/A')[:100]}...")
        
        print("\n✓ Perus testit valmis!")
        
    except requests.exceptions.Timeout:
        print("✗ Virhe: Pyyntö aikakatkesi (timeout)")
    except requests.exceptions.ConnectionError:
        print("✗ Virhe: Yhteyttä ei voida muodostaa")
    except Exception as e:
        print(f"✗ Virhe: {str(e)}")


def test_yle_selenium():
    """Testaa Yle.fi-nettisivun interaktiivisia ominaisuuksia (Selenium)"""
    
    print("\n" + "=" * 60)
    print("SELENIUM TESTIT - INTERAKTIIVISET TESTIT")
    print("=" * 60)
    
    url = "https://yle.fi"
    driver = None
    
    try:
        # Alusta Chrome-selain
        print("\n[Testi 1] Alustetaan Chrome-selain...")
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("✓ Chrome-selain avattu")
        
        # Avaa sivusto
        print("\n[Testi 2] Avataan Yle.fi sivusto...")
        start_time = time.time()
        driver.get(url)
        load_time = time.time() - start_time
        print(f"✓ Sivusto ladattu Seleniumilla: {load_time:.2f} sekuntia")
        
        # Odota sivun latautumista
        print("\n[Testi 3] Odotetaan sivun latautumista...")
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
            print("✓ Sivu latautunut onnistuneesti")
        except Exception as e:
            print(f"✗ Sivun latautuminen epäonnistui: {e}")
        
        # Tarkista sivun otsikko
        print("\n[Testi 4] Tarkistetaan sivun otsikko...")
        page_title = driver.title
        print(f"✓ Sivun otsikko: {page_title}")
        
        # Etsi ja tarkista linkkejä
        print("\n[Testi 5] Etsitään linkkejä...")
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"✓ Löydettiin {len(links)} linkkiä")
        
        # Etsi artikkelit
        print("\n[Testi 6] Etsitään artikkeleita...")
        articles = driver.find_elements(By.TAG_NAME, "article")
        print(f"✓ Löydettiin {len(articles)} artikkelia/sisältöä")
        
        # Näytä sivun korkeus
        print("\n[Testi 7] Mitataan sivun dimensioita...")
        window_size = driver.get_window_size()
        print(f"✓ Selaimen koko: {window_size['width']}x{window_size['height']} px")
        
        # Tarkista JavaScript-virheitä konsolista
        print("\n[Testi 8] Tarkistetaan konsolia...")
        logs = driver.get_log('browser')
        errors = [log for log in logs if log['level'] == 'SEVERE']
        if errors:
            print(f"✗ Löydettiin {len(errors)} JavaScript-virhettä:")
            for error in errors[:3]:  # Näytä vain 3 ensimmäistä
                print(f"  - {error['message'][:80]}")
        else:
            print("✓ Ei merkittäviä JavaScript-virheitä")
        
        # Tee screenshot
        print("\n[Testi 9] Otetaan screenshot...")
        driver.save_screenshot("yle_screenshot.png")
        print("✓ Screenshot tallennettu: yle_screenshot.png")
        
        print("\n✓ Selenium testit valmis!")
        
    except Exception as e:
        print(f"✗ Virhe Selenium-testeissä: {str(e)}")
    finally:
        if driver:
            driver.quit()
            print("\n✓ Selain suljettu")


def performance_test():
    """Suorituskykytestit"""
    
    print("\n" + "=" * 60)
    print("SUORITUSKYKY TESTIT")
    print("=" * 60)
    
    url = "https://yle.fi"
    
    try:
        print("\n[Testi 1] Mitataan useita latauksia...")
        load_times = []
        
        for i in range(5):
            start_time = time.time()
            response = requests.get(url, timeout=10)
            load_time = time.time() - start_time
            load_times.append(load_time)
            print(f"  Lataus {i+1}: {load_time:.3f}s")
        
        avg_time = sum(load_times) / len(load_times)
        min_time = min(load_times)
        max_time = max(load_times)
        
        print(f"\n✓ Keskimääräinen latausaika: {avg_time:.3f}s")
        print(f"✓ Nopein lataus: {min_time:.3f}s")
        print(f"✓ Hitain lataus: {max_time:.3f}s")
        
        # Tarkista vastausten koot
        print("\n[Testi 2] Mitataan vastausten koko...")
        response = requests.get(url, timeout=10)
        size_bytes = len(response.content)
        size_mb = size_bytes / (1024 * 1024)
        print(f"✓ Sivun koko: {size_bytes} tavua ({size_mb:.2f} MB)")
        
    except Exception as e:
        print(f"✗ Virhe suorituskykytestissä: {str(e)}")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("YLE.FI LAAJENNUSSARJA TESTAUS")
    print("=" * 60)
    
    # Suorita testit
    test_yle_basic()
    
    # Kysy käyttäjältä haluaako Selenium-testit
    print("\n" + "-" * 60)
    try:
        response = input("\nHaluatko suorittaa Selenium-testit? (K/E): ").strip().lower()
        if response in ['k', 'yes', 'y']:
            test_yle_selenium()
        else:
            print("Selenium-testit ohitettiin")
    except:
        print("Selenium-testit ohitettiin")
    
    # Suorita suorituskykytestit
    performance_test()
    
    print("\n" + "=" * 60)
    print("✓ KAIKKI TESTIT SUORITETTU")
    print("=" * 60)

