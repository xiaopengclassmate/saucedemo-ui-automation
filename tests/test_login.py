import allure
import pytest

from utils.data_loader import load_yaml

LOGIN_CASES = load_yaml("data/login_cases.yaml")


@allure.feature("登录")
@pytest.mark.login
class TestLogin:
    @allure.story("正常登录")
    @allure.title("标准用户可以成功登录并看到商品列表")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "case",
        LOGIN_CASES["success"],
        ids=[case["id"] for case in LOGIN_CASES["success"]],
    )
    def test_valid_login(self, login_page, case):
        inventory = login_page.login(case["username"], case["password"])
        inventory.expect_loaded()
        assert inventory.item_count() == 6

    @allure.story("异常登录")
    @allure.title("非法凭据登录失败并提示错误")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "case",
        LOGIN_CASES["invalid"],
        ids=[case["id"] for case in LOGIN_CASES["invalid"]],
    )
    def test_invalid_credentials(self, login_page, case):
        login_page.login(case["username"], case["password"])
        assert login_page.error_message() == case["expected_error"]

    @allure.story("必填校验")
    @allure.title("用户名或密码为空时展示必填提示")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "case",
        LOGIN_CASES["required"],
        ids=[case["id"] for case in LOGIN_CASES["required"]],
    )
    def test_required_fields(self, login_page, case):
        login_page.login(case["username"], case["password"])
        assert login_page.error_message() == case["expected_error"]
