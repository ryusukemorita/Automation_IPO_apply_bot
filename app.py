from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')

DRIVER_PATH = './chromedriver.exe'
USERNAME = '********'   # ユーザー名を入力
PASSWORD = '********'   # パスワードを入力

# ブラウザの起動
driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)

# Webページにアクセスする
url = 'https://www.sbisec.co.jp/ETGate'
driver.get(url)

# ロード完了後まで待つ
sleep(5)

# ユーザーネームの入力
element = driver.find_element_by_css_selector('#user_input > input[type=text]')
element.send_keys(USERNAME)

# パスワードの入力
element = driver.find_element_by_css_selector('#password_input > input[type=password]')
element.send_keys(PASSWORD)

# ログインボタンの押下
element = driver.find_element_by_css_selector('#SUBAREA01 > form > div > div > div > p.sb-position-c > a > input')
element.click()

# 国内株式→IPO・POを押下
ipo_url = 'https://site1.sbisec.co.jp/ETGate/?OutSide=on&_ControlID=WPLETmgR001Control&_DataStoreID=DSWPLETmgR001Control&burl=search_domestic&dir=ipo%2F&file=stock_info_ipo.html&cat1=domestic&cat2=ipo&getFlg=on'
driver.get(ipo_url)

# 新規上場株式ブックビルディング / 購入意思表示ボタンを押下
element = driver.find_element_by_css_selector('#main > div:nth-child(11) > div > div > a > img')
element.click()

for i in range(10):
   sleep(2)
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
   name_element = driver.find_element_by_css_selector('body > table > tbody > tr > td > table:nth-child(1) > tbody > tr > td > table:nth-child(3) > tbody > tr:nth-child(1) > td > form > table:nth-child(7) > tbody > tr > td > div > font > b')
   print(name_element.text)

   # 申込件数を入力
   suryo_element = driver.find_element_by_css_selector('body > table > tbody > tr > td > table:nth-child(1) > tbody > tr > td > table:nth-child(3) > tbody > tr:nth-child(1) > td > form > table:nth-child(21) > tbody > tr > td > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(3) > td')
   suryo = re.search(r'\d+株', suryo_element.text).group()[0:-1] # "（売買単位/100株）"から株数のみを取得
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
   driver.find_element_by_css_selector('body > table > tbody > tr > td > table:nth-child(1) > tbody > tr > td > table:nth-child(3) > tbody > tr > td > table:nth-child(9) > tbody > tr > td > a').click()