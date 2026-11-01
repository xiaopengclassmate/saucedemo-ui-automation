from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    path = "/"

    USERNAME = '[data-test="username"]'
    PASSWORD = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR = '[data-test="error"]'

    def open(self) -> LoginPage:
        super().open()
        expect(self.page.locator(self.LOGIN_BUTTON)).to_be_visible()
        return self

    def expect_loaded(self) -> None:
        expect(self.page.locator(self.LOGIN_BUTTON)).to_be_visible()

    def login(self, username: str, password: str) -> InventoryPage:
        self.page.fill(self.USERNAME, username)
        self.page.fill(self.PASSWORD, password)
        self.page.click(self.LOGIN_BUTTON)
        return InventoryPage(self.page)

    def error_message(self) -> str:
        error = self.page.locator(self.ERROR)
        expect(error).to_be_visible()
        return error.inner_text()
