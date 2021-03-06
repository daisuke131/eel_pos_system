import sys

import eel

from desktop import start
from pos_system import PosSystem

app_name = "web"
end_point = "index.html"
size = (600, 700)


@eel.expose
def add_order_item(item_code: str, amount: str) -> None:
    global system
    if system.order is None:
        system.init_order()
    res = system.order.add_item_order(item_code, int(amount))
    if res:
        res_text = system.order.output_oder_list()
        eel.output_oder_list(res_text)
    else:
        eel.alert_js(f"『{item_code}』は商品マスターに登録されていません")


@eel.expose
def order_process(pay_price: str) -> None:
    global system
    pay_text, is_completed_payment = system.order.pay_off(int(pay_price))
    eel.alert_js(pay_text)
    if is_completed_payment:
        system.order.write_receipt()
        eel.alert_js("レシートを発行しました。")
        reset_order()


@eel.expose
def reset_order() -> None:
    system.init_order()
    eel.reset_object()


def init_pos_system() -> None:
    global system
    system = PosSystem()
    is_add_item_master: bool = system.add_item_master()
    if not is_add_item_master:
        print("システムを終了します。")
        sys.exit()


if __name__ == "__main__":
    init_pos_system()
    start(app_name, end_point, size)
