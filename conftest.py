import os

import allure
import pytest

from config import settings
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

_CONSOLE_LOGS: dict[int, list[str]] = {}


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """保留 pytest-playwright 的 --headed 等参数，同时支持 SLOW_MO。"""
    return {**browser_type_launch_args, "slow_mo": int(os.getenv("SLOW_MO", "0"))}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": settings.BASE_URL,
        "viewport": {"width": 1440, "height": 900},
        "locale": "en-US",
    }


@pytest.fixture
def page(context):
    """覆盖 pytest-playwright 的 page fixture，统一超时并收集控制台日志。"""
    test_page = context.new_page()
    test_page.set_default_timeout(settings.DEFAULT_TIMEOUT_MS)
    test_page.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT_MS)

    logs: list[str] = []
    _CONSOLE_LOGS[id(test_page)] = logs
    test_page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))

    yield test_page

    _CONSOLE_LOGS.pop(id(test_page), None)
    test_page.close()


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def inventory_page(page) -> InventoryPage:
    login = LoginPage(page).open()
    login.login(settings.STANDARD_USER, settings.PASSWORD)
    inventory = InventoryPage(page)
    inventory.expect_loaded()
    return inventory


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """失败时自动截图、记录 URL 和控制台日志，并附加到 Allure 报告。"""
    report = yield
    if report.when != "call" or not report.failed:
        return report

    test_page = item.funcargs.get("page")
    if test_page is None:
        return report

    try:
        allure.attach(
            test_page.screenshot(full_page=True),
            name="失败截图",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            test_page.url,
            name="失败页面 URL",
            attachment_type=allure.attachment_type.TEXT,
        )
        logs = _CONSOLE_LOGS.get(id(test_page), [])
        if logs:
            allure.attach(
                "\n".join(logs[-50:]),
                name="浏览器控制台日志",
                attachment_type=allure.attachment_type.TEXT,
            )
    except Exception:
        # 报告增强不能影响测试结果
        pass

    return report
