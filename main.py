import os
import pathlib
import time

from playwright.sync_api import sync_playwright

URL = "https://newsyle.com/2PrsL2gY?utm_creative=MP1041_IT_qua_celebacreo-9_it_img_1080x1080&utm_campaign=17.12+IT+TESToff%2Bcreo+-+Quantum+AI+Pixel+34_Fr+%281041%29&utm_source=fb&utm_placement=Facebook_Desktop_Feed&campaign_id=120236181170220192&adset_id=120236181170300192&ad_id=120236181170270192&adset_name=25%2B+advantage&fbpixel=783728971351643&sub_id_16=5368&utm_medium=paid&utm_id=120236181170220192&utm_content=120236181170270192&utm_term=120236181170300192"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
ROOT_FOLDER = pathlib.Path(__file__).parent
EXT_PATH = str(ROOT_FOLDER / "singlefile-extension-chromium")
PROXY_CONFIG = {
    "server": "http://residential.swiftproxy.io:9000",
    "username": "mtwfarmbot-country-it",
    "password": "2fd3edfd-d855-4627-9ccf-b4ea9bf6b5d3",
}

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir="./user_data_dir",
        headless=False,  # MUST be false
        downloads_path="./snapshots",
        accept_downloads=True,
        args=[
            f"--disable-extensions-except={EXT_PATH}",
            f"--load-extension={EXT_PATH}",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            f"--user-agent={USER_AGENT}",
        ],
        # proxy=PROXY_CONFIG,
    )

    page = browser.new_page()
    page.goto(URL, wait_until="networkidle")
    page.evaluate("""
        chrome.runtime.sendMessage('cfgkglpohbeemchjciegabidljjmnidf', 'save-page');
    """)
    while not os.listdir("./snapshots"):
        time.sleep(1)
    for file in os.listdir("./snapshots"):
        os.rename(f"./snapshots/{file}", f"./snapshots/{file}.zip")
        print(file)
