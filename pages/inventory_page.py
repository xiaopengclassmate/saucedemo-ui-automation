from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from pages.base_page import BasePage
from pages.cart_page import CartPage


class InventoryPage(BasePage):
    path = "/inventory.html"

    ITEMS = ".inventory_item"
    ITEM_NAMES = ".inventory_item_name"
    ITEM_PRICES = ".inventory_item_price"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = '[data-test="shopping-cart-link"]'
    SORT = '[data-test="product-sort-container"]'
    BURGER_MENU = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/inventory\.html$"))
        expect(self.page.locator(self.ITEMS).first).to_be_visible()

    def item_count(self) -> int:
        return self.page.locator(self.ITEMS).count()

    def item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAMES).all_inner_texts()

    def item_prices(self) -> list[float]:
        prices = self.page.locator(self.ITEM_PRICES).all_inner_texts()
        return [float(price.replace("$", "").strip()) for price in prices]

    def sort_by(self, option: str) -> None:
        """option: az | za | lohi | hilo"""
        self.page.select_option(self.SORT, option)

    def _item(self, product_name: str) -> Locator:
        return self.page.locator(self.ITEMS).filter(has_text=product_name)

    def add_to_cart(self, product_name: str) -> None:
        self._item(product_name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, product_name: str) -> None:
        self._item(product_name).get_by_role("button", name="Remove").click()

    def cart_badge_count(self) -> int:
        badge = self.page.locator(self.CART_BADGE)
        return int(badge.inner_text()) if badge.is_visible() else 0

    def expect_badge_count(self, count: int) -> None:
        badge = self.page.locator(self.CART_BADGE)
        if count == 0:
            expect(badge).to_have_count(0)
        else:
            expect(badge).to_have_text(str(count))

    def go_to_cart(self) -> CartPage:
        self.page.click(self.CART_LINK)
        return CartPage(self.page)

    def logout(self):
        from pages.login_page import LoginPage

        self.page.click(self.BURGER_MENU)
        self.page.click(self.LOGOUT_LINK)
        return LoginPage(self.page)
