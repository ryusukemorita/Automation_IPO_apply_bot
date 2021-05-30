from app import APP
from config import SBI_INFO as sbi
from config import RAKUTEN_INFO as rktn
from config import MONEX_INFO as mnx


# SBI証券のIPO申請プロセスを実行するコマンド
sbi_app = APP(sbi.url, sbi.login_id, sbi.password, sbi.css_selector_id_input, sbi.css_selector_password_input, sbi.css_selector_login_button, sbi.ipo_url, sbi.torihiki_password)
sbi_app.SBI_IPO_APPLY()


# 楽天証券のIPO申請プロセスを実行するコマンド
rktn_app = APP(rktn.url, rktn.login_id, rktn.password, rktn.css_selector_id_input, rktn.css_selector_password_input, rktn.css_selector_login_button, rktn.ipo_url, rktn.torihiki_password)
rktn_app.RAKUTEN_IPO_APPLY()


# SBI証券のIPO申請プロセスを実行するコマンド
"""
mnx_app = APP(mnx.url, mnx.login_id, mnx.password, mnx.css_selector_id_input, mnx.css_selector_password_input, mnx.css_selector_login_button, mnx.ipo_url, mnx.torihiki_password)
mnx_app.login()
"""