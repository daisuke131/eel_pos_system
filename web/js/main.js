const add_order_item = async () => {
    let input_product_code = $("#input_product_code").val()
    let input_amount = $("#input_amount").val()
    await eel.add_order_item(input_product_code, input_amount);
}

eel.expose(output_oder_list)
function output_oder_list(order_text) {
    $("#output-order").append(order_text + "\n");
    $("#output-order").scrollTop = $("#output-order").scrollHeight;
}