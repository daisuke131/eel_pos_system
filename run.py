import eel

from desktop import start
from pos_system import PosSystem

app_name = "web"
end_point = "index.html"
size = (600, 700)
system = PosSystem()


@eel.expose
def add_order_item(item_code: str, amount: str):
    """
    オーダーに商品を追加する
    """
    global system
    # Orderが存在しなければOrderインスタンスを作成
    # if system.order is None:
    if not system.order:
        system.init_order()
        system.order.add_item_order(item_code, int(amount))
    # res = system.order.add_item_order(item_code, int(amount))
    # if not res:
    #     eel.alertJs(f"『{item_code}』は商品マスターに登録されていません")
    # else:
    #     res_text = system.order.get_order_items()
    #     eel.view_order_items(res_text)


def init_pos_system():
    """
    POSシステムの初期化処理
    """
    global system  # グローバル変数を使用する場合の宣言

    # POSシステムに商品マスタを登録
    # system = PosSystem()
    system.add_item_master()  # CSVからマスタへ登録


if __name__ == "__main__":
    init_pos_system()
    start(app_name, end_point, size)
