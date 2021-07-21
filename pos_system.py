import os
# import sys
from datetime import datetime

# import eel
import pandas as pd

READ_CSV_PATH = os.path.join(os.getcwd(), "csv/product_master.csv")
RECEIPT_PATH = os.path.join(os.getcwd(), "receipt/{datetime}.txt")


class Item:
    def __init__(self, item_code: str, item_name: str, price: int) -> None:
        self.item_code: str = item_code
        self.item_name: str = item_name
        self.price: int = price

    # def get_price(self):
    #     return self.price


# オーダークラス
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
                # item_data = {
                #     "item_code": item.item_code,
                #     "item_name": item.item_name,
                #     "price": item.price,
                # }
                return item.item_name, item.price

    def add_item_order(self, item_code: str, item_amount: int) -> bool:
        item_data = self.fetch_item_data(item_code)
        if item_data:
            self.item_order_list.append(item_code)
            self.item_amount_list.append(item_amount)
            return True
            # eel.output_oder_list(f"{item_code}が{item_amount}個")
        else:
            # eel.not_exist_item("指定した商品が見つかりません。")
            return False

    # def input_order(self):
    #     while True:
    #         # 商品コード入力
    #         order_item_code: str = input("注文したい商品コードを入力してください。未入力で注文処理へ。>>")
    #         order_item_code = order_item_code.strip()
    #         if order_item_code.strip():
    #             if self.item_exists(order_item_code):
    #                 # 数量入力
    #                 while True:
    #                     order_item_count: str = input("数量を入力してください。>>")
    #                     order_item_count = order_item_count.strip()
    #                     try:
    #                         order_item_count_int: int = int(order_item_count)
    #                         break
    #                     except Exception:
    #                         print("数量を正しく入力してください。")
    #                         pass
    #                 # オーダーリストに追加
    #                 self.add_item_order_list(order_item_code, order_item_count_int)
    #             else:
    #                 print("商品コードに誤りがあります。")
    #                 continue
    #         else:
    #             print("清算処理へ移ります。")
    #             break

    # def add_item_order(self, item_code: str):
    #     self.item_order_list.append(item_code)

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
            # self.write_receipt("商品コード：{}".format(item_data["item_code"]))
            # self.write_receipt("商品名：{}".format(item_data["item_name"]))
            # self.write_receipt("金額：{}".format("{:,}".format(item_data["price"])))
            # self.write_receipt("数量：{}".format("{:,}".format(order_count)))
            # self.write_receipt("小計：￥{}円".format("{:,}".format(item_total_price)))
            # self.write_receipt("===================================")
            oder_text += f"{count}.商品名:{item_name} 値段:{price}円 個数:{order_count}個\n"
        # self.write_receipt("合計：￥{}円".format("{:,}".format(self.total_price)))
        oder_text += "=============================\n"
        # print(f"合計：￥{"{:,}".format(self.total_price)}円になります。")
        oder_text += f"合計：￥{self.total_price:,}円\n"
        self.receipt_text = oder_text
        return oder_text

    def pay_off(self, pay_price: int) -> tuple[str, bool]:
        # while True:
        # pay_price_str: str = input("支払い金額を入力してください>>")
        # pay_price_str = pay_price_str.strip()
        # try:
        # pay_price: int = int(pay_price_str)
        pay_flg = True
        self.pay_price = pay_price
        self.change_price = pay_price - self.total_price
        # self.write_receipt()
        # self.write_receipt("おつり：￥{}円".format("{:,}".format(change_price)))
        if self.change_price > 0:
            pay_text = f"{self.change_price:,}円のお返しになります。"
        elif self.change_price == 0:
            pay_text = f"{self.total_price:,}円ちょうどお預かりします。"
        else:
            pay_text = "料金が不足しています。"
            pay_flg = False
            # pass
        return pay_text, pay_flg

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

    # except Exception:
    # print("金額を正しく入力してください。")
    # pass


# メイン処理
# def main():
#     item_master = reegist_master()
#     # 商品一覧表示
#     for item in item_master:
#         print(f"{item.item_code} {item.item_name} {item.price}")
#     # オーダー登録
#     order = Order(item_master)
#     # 注文入力
#     order.input_order()
#     # オーダー表示
#     order.view_item_list()
#     # 支払い
#     order.pay_off()
#     print("レシートが発行されました。")
#     print("ありがとうございました。")


# def reegist_master():
#     item_master = []
#     try:
#         df = pd.read_csv(
#             READ_CSV_PATH, dtype={"item_code": object, "item_name": object}
#         )
#         for index, row in df.iterrows():
#             # マスタ登録
#             item_master.append(
#                 Item(row["item_code"], row["item_name"], int(row["price"]))
#             )
#         return item_master
#     except Exception:
#         print("マスタ登録できませんでした。")
#         sys.exit()


class PosSystem:
    # def __init__(self, csv_path: str = None):
    def __init__(self) -> None:
        self.item_master = []
        # self.csv_path = csv_path
        self.order = None

    # マスタ登録(課題３)
    def add_item_master(self) -> bool:
        print("------- マスタ登録開始 ---------")
        count = 0
        try:
            df = pd.read_csv(READ_CSV_PATH, dtype={"item_code": object})
            #     # self.csv_path, dtype={"item_code": object}
            #     READ_CSV_PATH,
            #     dtype={"item_code": object},
            # )  # CSVでは先頭の0が削除されるためこれを保持するための設定
            for item_code, item_name, price in zip(
                df["item_code"],
                df["item_name"],
                df["price"],
            ):
                self.item_master.append(Item(item_code, item_name, price))
                # print("{}({})".format(item_name, item_code))
                count += 1
            print("{}品の登録を完了しました。".format(count))
            print("------- マスタ登録完了 ---------")
            return True
        except Exception:
            print("マスタ登録が失敗しました")
            # print("------- マスタ登録完了 ---------")
            return False

    def init_order(self) -> None:
        self.order = Order(self.item_master)
