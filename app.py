from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

# Chromeのオプション設定
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')

DRIVER_PATH = './chromedriver'

class APP(object):


    def __init__(self, URL, ID, PASSWORD, ID_INPUT, PASSWORD_INPUT, LOGIN_BUTTON, IPO_URL, TORIHIKI_PASSWORD):
        self.URL = URL
        self.ID = ID
        self.PASSWORD = PASSWORD
        self.ID_INPUT = ID_INPUT
        self.PASSWORD_INPUT = PASSWORD_INPUT
        self.LOGIN_BUTTON = LOGIN_BUTTON
        self.IPO_URL = IPO_URL
        self.TORIHIKI_PASSWORD = TORIHIKI_PASSWORD

     
    def login(self):
        # ブラウザの起動
        driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)

        # Webページにアクセスする
        driver.get(self.URL)

        # ロード完了後まで5秒待つ
        driver.implicitly_wait(10)

        # ユーザーネームの入力
        element = driver.find_element_by_css_selector(self.ID_INPUT)
        element.send_keys(self.ID)

        # パスワードの入力
        element = driver.find_element_by_css_selector(self.PASSWORD_INPUT)
        element.send_keys(self.PASSWORD)

        # ログインボタンの押下
        element = driver.find_element_by_css_selector(self.LOGIN_BUTTON)
        element.click()

        # 国内株式→IPO・POを押下
        driver.get(self.IPO_URL)

    # SBI証券のIPOの申込みする関数
    def SBI_IPO_APPLY(self):

        # login関数の呼び出し
        self.login()

        # 新規上場株式ブックビルディング / 購入意思表示ボタンを押下
        element = driver.find_element_by_css_selector('#main > div:nth-child(11) > div > div > a > img')
        element.click()

        for i in range(10):
            driver.implicitly_wait(10)
            # 申込ボタンを探索
            element = None
            try:
                element = driver.find_element_by_xpath('//img[@alt=\"申込\"]')
            except NoSuchElementException:
                print('申込可能銘柄なし')
                driver.quit()
                sys.exit()

            # 申込ボタンを押下
            element.click()

            # 銘柄名取得・表示
            name_element = driver.find_element_by_css_selector('body > table > tbody > tr > td > table:nth-child(1) > tbody > tr > td\
                 > table:nth-child(3) > tbody > tr:nth-child(1) > td > form > table:nth-child(7) > tbody > tr > td > div > font > b')
            print(name_element.text)

            # 申込件数を入力
            suryo_element = driver.find_element_by_css_selector('body > table > tbody > tr > td > table:nth-child(1) > tbody > tr > td\
                 > table:nth-child(3) > tbody > tr:nth-child(1) > td > form > table:nth-child(21) > tbody > tr > td > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(3) > td')
            suryo = re.search(r'\d+株', suryo_element.text).group()[0:-1]   # "（売買単位/100株）"から株数のみを取得
            driver.find_element_by_name('suryo').send_keys(suryo)

            # ストライクプライスにチェック
            driver.find_element_by_id('strPriceRadio').click()

            # 取引パスワードを入力
            driver.find_element_by_name('tr_pass').send_keys(TORIHIKI_PASSWORD)

            # 申込確認画面へを押下
            driver.find_element_by_name('order_kakunin').click()

            # 申込を押下
            driver.find_element_by_name('order_btn').click()

            # 新規上場株式ブックビルディング / 購入意思表示画面へ戻る を押下
            driver.find_element_by_css_selector('body > table > tbody > tr > td > table:nth-child(1) > tbody > tr > td\
                 > table:nth-child(3) > tbody > tr > td > table:nth-child(9) > tbody > tr > td > a').click()


    # 楽天証券のIPOの申込みする関数
    def RAKUTEN_IPO_APPLY(self):

        # login関数の呼び出し
        self.login()

        # 新規上場株式ブックビルディング / 購入意思表示ボタンを押下
        element = driver.find_element_by_css_selector('div.pcm-nav-03 select--order > div > ul > a.pcm-nav-03-btn')
        element.click()

        for i in range(10):
            driver.implicitly_wait(10)
            # 参加ボタンを探索
            element = None
            try:
                element = driver.find_element_by_css_selector('table.tbl-data-padding3 > tbody > tr > td.ta1ye > div.mbodym > nobr > a')
                # 銘柄名取得・表示
                name_element = driver.find_element_by_css_selector('table.tbl-data-padding3 > tbody > tr > td.ta1ye > div.mbodym > a')
                print(name_element.text)
            
            except NoSuchElementException:
                print('申込可能銘柄なし')
                driver.quit()
                sys.exit()

            # 参加ボタンを押下
            element.click()

            # 同意ボタンを押下
            element = driver.find_element_by_css_selector('table.buttonarea > tbody > tr > td > div > input')

            # 申込件数を入力
            input_element = driver.find_element_by_css_selector('table > tbody > tr > td > div.mbodym > nobr > input')
            input_element.send_keys(100)
            
            input_element = driver.find_element_by_css_selector('table > tbody > tr > td > div.mbodym > nobr > select#price > option[value=0]')

            # 確認ボタンを押下
            driver.find_element_by_css_selector('input[value="　　確　認　　"]').click()

            # 新規上場株式ブックビルディング / 購入意思表示画面へ戻る を押下
            driver.find_element_by_css_selector('body > table > tbody > tr > td > table:nth-child(1) > tbody > tr > td\
                 > table:nth-child(3) > tbody > tr > td > table:nth-child(9) > tbody > tr > td > a').click()
