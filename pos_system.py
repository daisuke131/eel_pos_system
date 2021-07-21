import os
from datetime import datetime

import pandas as pd

READ_CSV_PATH = os.path.join(os.getcwd(), "csv/product_master.csv")
RECEIPT_PATH = os.path.join(os.getcwd(), "receipt/{datetime}.txt")


class Item:
    def __init__(self, item_code: str, item_name: str, price: int) -> None:
        self.item_code: str = item_code
        self.item_name: str = item_name
        self.price: int = price


class Order:
    def __init__(self, item_master) -> None:
        self.item_order_list = []
        self.item_amount_list = []
        self.total_price: int = 0
        self.change_price: int = 0
        self.pay_price: int = 0
        self.receipt_text: str
        self.item_master = item_master

    def fetch_item_data(self, item_code: str) -> tuple[str, str]:
        for item in self.item_master:
            if item.item_code == item_code:
                return item.item_name, item.price

    def add_item_order(self, item_code: str, item_amount: int) -> bool:
        item_data = self.fetch_item_data(item_code)
        if item_data:
            self.item_order_list.append(item_code)
            self.item_amount_list.append(item_amount)
            return True
        else:
            return False

    def output_oder_list(self) -> str:
        oder_text = "==========ご注文リスト==========\n"
        self.total_price = 0
        count = 0
        for order_item_code, order_count in zip(
            self.item_order_list, self.item_amount_list
        ):
            item_name, price = self.fetch_item_data(order_item_code)
            item_total_price: int = int(price) * int(order_count)
            self.total_price += item_total_price
            count += 1
            oder_text += f"{count}.商品名:{item_name} 値段:{price}円 個数:{order_count}個\n"
        oder_text += "=============================\n"
        oder_text += f"合計：￥{self.total_price:,}円\n"
        self.receipt_text = oder_text
        return oder_text

    def pay_off(self, pay_price: int) -> tuple[str, bool]:
        is_completed_payment = True
        self.pay_price = pay_price
        self.change_price = pay_price - self.total_price
        if self.change_price > 0:
            pay_text = f"{self.change_price:,}円のお返しになります。"
        elif self.change_price == 0:
            pay_text = f"{self.total_price:,}円ちょうどお預かりします。"
        else:
            pay_text = "料金が不足しています。"
            is_completed_payment = False
        return pay_text, is_completed_payment

    def write_receipt(self):
        self.receipt_text += f"お預かり：￥{self.pay_price:,}円\n"
        self.receipt_text += f"お釣り：￥{self.change_price:,}円"
        csv_path = RECEIPT_PATH.format(
            datetime=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        )
        with open(
            csv_path,
            mode="w",
            encoding="utf_8_sig",
        ) as f:
            f.write(self.receipt_text)


class PosSystem:
    def __init__(self) -> None:
        self.item_master = []
        self.order = None

    def add_item_master(self) -> bool:
        print("------- マスタ登録開始 ---------")
        count = 0
        try:
            df = pd.read_csv(READ_CSV_PATH, dtype={"item_code": object})
            for item_code, item_name, price in zip(
                df["item_code"],
                df["item_name"],
                df["price"],
            ):
                self.item_master.append(Item(item_code, item_name, price))
                count += 1
            print(f"{count}品の登録を完了しました。")
            print("------- マスタ登録完了 ---------")
            return True
        except Exception:
            print("マスタ登録が失敗しました")
            return False

    def init_order(self) -> None:
        self.order = Order(self.item_master)
