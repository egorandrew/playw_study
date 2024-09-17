import time
import base64

from playwright.sync_api import Page, expect, Route, Dialog, BrowserContext
import re


def test_login_click(page: Page):
    page.goto('https://tp3-test.etpgpb.dev')
    page.locator("//button[.='Войти']").click()
    page.locator('#username').fill("customer1_etp@mailforspam.com")
    page.locator('#password').fill("hfuFwc9S(Ad8c$")
    page.locator('#password').blur()
    page.locator('#kc-login').click()
    expect(page.locator("//h2")).to_have_text("Выберите организацию")

    time.sleep(10)


def test_request(page: Page):
    def change_request(route: Route):
        data = route.request.post_data
        if data:
            data = data.replace('customer1_etp%40mailforspam.com', 'svasvasasvadsvasasas')
            # print(data)
        route.continue_(post_data=data)

    page.route(re.compile('auth/realms/master/login-actions/authenticate'), change_request)
    page.goto('https://tp3-test.etpgpb.dev')
    page.locator("//button[.='Войти']").click()
    page.locator('#username').fill("customer1_etp@mailforspam.com")
    page.locator('#password').fill("hfuFwc9S(Ad8c$")
    page.locator('#password').blur()
    page.locator('#kc-login').click()

    expect(page.locator("//h2")).to_have_text("Выберите организацию")
    time.sleep(10)


def test_response(page: Page):
    def change_response(route: Route):
        print('Hi')
        response = route.fetch()
        data = response.text()
        data.decode("utf-8")
        data = data.replace('0103001599', 'svasvasvasvas')
        print(data)
        route.fulfill(response=response, body=data)

    page.route(re.compile('api/v1/user/organizations'), change_response)
    page.goto('https://tp3-test.etpgpb.dev')
    page.locator("//button[.='Войти']").click()
    page.locator('#username').fill("customer1_etp@mailforspam.com")
    page.locator('#password').fill("hfuFwc9S(Ad8c$")
    page.locator('#password').blur()
    page.locator('#kc-login').click()

    expect(page.locator("//h2")).to_have_text("Выберите организацию")
    time.sleep(5)


def test_alerts(page: Page):
    page.goto('https://demoblaze.com')

    def accept_alert(alert: Dialog):
        print(alert.message)
        alert.accept()

    page.on('dialog', accept_alert)
    page.get_by_role('link', name='Samsung galaxy s6').click()
    page.get_by_role('link', name='Add to cart').click()
    page.wait_for_event('dialog')
    page.locator('#cartur').click()


def test_tabs(page: Page, context: BrowserContext):
    page.goto('https://mail.ru/')
    page.locator('//a[.="Спорт"]').click()
    with context.expect_page() as new_tab_event:
        page.locator('//span[.="Китай уже шестой!"]').click()
        new_tab = new_tab_event.value
    new_tab.locator('//a/span[.="Медальный зачет"]').click()


def test_iframe(page: Page):
    page.goto('https://www.qa-practice.com/elements/iframe/iframe_page')
    page.frame_locator('iframe').locator('.navbar-toggler-icon').click()


def test_select(page: Page):
    page.goto('https://magento.softwaretestingboard.com/men/tops-men/jackets-men.html')
    page.locator('#sorter').first.select_option('Price')











