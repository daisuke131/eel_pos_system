import eel

from desktop import start
from pos_system import PosSystem

app_name = "web"
end_point = "index.html"
size = (600, 700)


@eel.expose
def add_order_item(item_code: str, amount: str):
    global system
    if system.order is None:
        system.init_order()
    res = system.order.add_item_order(item_code, int(amount))
    if res:
        res_text = system.order.output_oder_list()
        eel.output_oder_list(res_text)
    else:
        eel.alert_js(f"『{item_code}』は商品マスターに登録されていません")


def init_pos_system():
    global system
    system = PosSystem()
    system.add_item_master()


if __name__ == "__main__":
    init_pos_system()
    start(app_name, end_point, size)
