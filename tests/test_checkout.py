import allure
import pytest


@allure.feature("下单流程")
@pytest.mark.checkout
class TestCheckout:
    @allure.story("完整下单")
    @allure.title("添加两件商品后可以完成下单")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_end_to_end_purchase(self, inventory_page):
        inventory_page.add_to_cart("Sauce Labs Backpack")
        inventory_page.add_to_cart("Sauce Labs Bike Light")

        cart = inventory_page.go_to_cart()
        cart.expect_loaded()
        cart.expect_item_count(2)
        assert "Sauce Labs Backpack" in cart.item_names()

        checkout = cart.checkout()
        checkout.fill_info("Auto", "Tester", "100000")
        checkout.continue_to_overview()
        assert "$" in checkout.total_text()

        checkout.finish()
        assert checkout.complete_message() == "Thank you for your order!"

    @allure.story("表单校验")
    @allure.title("未填写邮编时无法进入订单确认页")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_postal_code_is_required(self, inventory_page):
        inventory_page.add_to_cart("Sauce Labs Backpack")

        cart = inventory_page.go_to_cart()
        checkout = cart.checkout()
        checkout.fill_info("Auto", "Tester", "")
        checkout.click_continue()

        assert checkout.error_message() == "Error: Postal Code is required"
