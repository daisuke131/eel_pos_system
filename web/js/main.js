const add_order_item = async () => {
    let input_product_code = $("#input_product_code").val()
    let input_amount = $("#input_amount").val()
    if (!input_product_code) {
        alert("商品コードを入力してください。")
        return
    }
    else if (!input_amount) {
        alert("数量を入力してください。")
        return
    }
    await eel.add_order_item(input_product_code, input_amount);
}

eel.expose(output_oder_list)
function output_oder_list(order_text) {
    $("#output-order").val(order_text);
    $("#output-order").scrollTop = $("#output-order").scrollHeight;
}

eel.expose(alert_js)
function alert_js(text) {
    alert(text)
}

// 半角数字のみ入力可
$(document).on('keydown', '.input_number_only', function (e) {
    let k = e.keyCode;
    let str = String.fromCharCode(k);
    // 8 = back space key 46 = delete key
    if (!(str.match(/[0-9]/) || (37 <= k && k <= 40) || k === 8 || k === 46)) {
        return false;
    }
});
$(document).on('keyup', '.input_number_only', function (e) {
    this.value = this.value.replace(/[^0-9]+/i, '');
});

$(document).on('blur', '.input_number_only', function () {
    this.value = this.value.replace(/[^0-9]+/i, '');
});