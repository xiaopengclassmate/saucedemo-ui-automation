import allure
import pytest


@allure.feature("商品列表")
@pytest.mark.inventory
class TestInventory:
    @allure.story("商品展示")
    @allure.title("商品列表展示全部 6 个商品")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_inventory_shows_all_products(self, inventory_page):
        assert inventory_page.item_count() == 6
        assert "Sauce Labs Backpack" in inventory_page.item_names()

    @allure.story("排序")
    @allure.title("可以按价格升序/降序排列商品")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "option,reverse",
        [("lohi", False), ("hilo", True)],
        ids=["价格从低到高", "价格从高到低"],
    )
    def test_sort_by_price(self, inventory_page, option, reverse):
        inventory_page.sort_by(option)
        prices = inventory_page.item_prices()
        assert prices == sorted(prices, reverse=reverse)

    @allure.story("购物车")
    @allure.title("添加/移除商品时购物车角标同步更新")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_cart_badge_updates(self, inventory_page):
        inventory_page.add_to_cart("Sauce Labs Backpack")
        inventory_page.expect_badge_count(1)

        inventory_page.add_to_cart("Sauce Labs Bike Light")
        inventory_page.expect_badge_count(2)

        inventory_page.remove_from_cart("Sauce Labs Backpack")
        inventory_page.expect_badge_count(1)

        inventory_page.remove_from_cart("Sauce Labs Bike Light")
        inventory_page.expect_badge_count(0)

    @allure.story("退出登录")
    @allure.title("用户可以从侧边栏退出登录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_logout(self, inventory_page):
        login_page = inventory_page.logout()
        login_page.expect_loaded()
