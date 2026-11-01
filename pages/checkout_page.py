from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = '[data-test="firstName"]'
    LAST_NAME = '[data-test="lastName"]'
    POSTAL_CODE = '[data-test="postalCode"]'
    CONTINUE = '[data-test="continue"]'
    CANCEL = '[data-test="cancel"]'
    FINISH = '[data-test="finish"]'
    ERROR = '[data-test="error"]'
    COMPLETE_HEADER = '[data-test="complete-header"]'
    SUMMARY_TOTAL = ".summary_total_label"

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> CheckoutPage:
        self.page.fill(self.FIRST_NAME, first_name)
        self.page.fill(self.LAST_NAME, last_name)
        self.page.fill(self.POSTAL_CODE, postal_code)
        return self

    def click_continue(self) -> None:
        self.page.click(self.CONTINUE)

    def continue_to_overview(self) -> CheckoutPage:
        self.click_continue()
        expect(self.page).to_have_url(re.compile(r"/checkout-step-two\.html$"))
        return self

    def finish(self) -> CheckoutPage:
        self.page.click(self.FINISH)
        expect(self.page).to_have_url(re.compile(r"/checkout-complete\.html$"))
        return self

    def error_message(self) -> str:
        error = self.page.locator(self.ERROR)
        expect(error).to_be_visible()
        return error.inner_text()

    def complete_message(self) -> str:
        header = self.page.locator(self.COMPLETE_HEADER)
        expect(header).to_be_visible()
        return header.inner_text()

    def total_text(self) -> str:
        return self.page.locator(self.SUMMARY_TOTAL).inner_text()
