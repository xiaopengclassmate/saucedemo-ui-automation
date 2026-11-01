from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class CartPage(BasePage):
    path = "/cart.html"

    ITEMS = ".cart_item"
    CHECKOUT_BUTTON = '[data-test="checkout"]'
    CONTINUE_SHOPPING = '[data-test="continue-shopping"]'

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/cart\.html$"))

    def item_count(self) -> int:
        return self.page.locator(self.ITEMS).count()

    def expect_item_count(self, count: int) -> None:
        expect(self.page.locator(self.ITEMS)).to_have_count(count)

    def item_names(self) -> list[str]:
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def remove(self, product_name: str) -> None:
        self.page.locator(self.ITEMS).filter(
            has_text=product_name
        ).get_by_role("button", name="Remove").click()

    def checkout(self) -> CheckoutPage:
        self.page.click(self.CHECKOUT_BUTTON)
        return CheckoutPage(self.page)
