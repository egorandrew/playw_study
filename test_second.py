import os.path
import re
import time

import pytest
from playwright.async_api import Page
from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://gm3-test.etpgpb.dev/")
#     page.goto("https://gm3-test.etpgpb.dev/auth")
#     page.get_by_placeholder("Логин").click()
#     page.get_by_placeholder("Логин").fill("support_user@pitanie.gazprom.ru")
#     page.get_by_placeholder("Логин").click()
#     page.get_by_placeholder("Пароль").click()
#     page.get_by_placeholder("Пароль").fill("ma-123456795")
#     page.get_by_role("button", name="Вход").click()
#     page.get_by_role("link", name="Заказы").click()
#     page.get_by_title("Все").click()
#     page.get_by_role("link", name="-2024-31834").click()
#     time.sleep(5)
#
#     # ---------------------
#     context.close()
#     browser.close()
#
#
# with sync_playwright() as playwright:
#     run(playwright)
def test_start(page: Page) -> None:
    page.goto("https://gm3-test.etpgpb.dev/auth")
    page.get_by_text("Забыли пароль?").click()
    page.get_by_label("Логин").click()
    page.get_by_label("Логин").fill("vsvsvsvsvs@mail.ru")
    page.get_by_role("button", name="Подтвердить").click()
    page.get_by_text("Назад к авторизации").click()
    time.sleep(1)


def test_check_1(page):
    page.goto('https://zimaev.github.io/checks-radios/')
    page.locator("text=Default checkbox").check()
    page.locator("text=Checked checkbox").check()
    page.locator("text=Default radio").check()
    page.locator("text=Default checked radio").check()
    page.locator("text=Checked switch checkbox input").check()


def test_check_2(page: Page) ->None:
    page.goto('https://zimaev.github.io/checks-radios/')
    page.locator("text=Default checkbox").click()
    page.locator("text=Checked checkbox").click()
    page.locator("text=Default radio").click()
    page.locator("text=Default checked radio").click()
    page.locator("text=Checked switch checkbox input").click()


def test_select(page):
    page.goto('https://zimaev.github.io/select/')
    page.select_option('#floatingSelect', value="3")
    time.sleep(3)
    page.select_option('#floatingSelect', index=1)
    time.sleep(3)
    page.select_option('#floatingSelect', label="Нашел и завел bug")
    time.sleep(3)


def test_drag_and_drop(page):
    page.goto('https://zimaev.github.io/draganddrop/')
    page.drag_and_drop("#drag", "#drop")


def test_dialogs_1(page: Page):
    page.goto("https://zimaev.github.io/dialog/")
    page.get_by_text("Диалог Alert").click()
    page.get_by_text("Диалог Confirmation").click()
    page.get_by_text("Диалог Prompt").click()


def test_dialogs_2(page: Page):
    page.goto("https://zimaev.github.io/dialog/")
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_text("Диалог Confirmation").click()


def test_select_multiple_1(page):
    page.goto('https://zimaev.github.io/upload/')
    page.set_input_files("#formFile", "hello.txt")
    page.locator("#file-submit").click()


def test_select_multiple_2(page):
    page.goto('https://zimaev.github.io/upload/')
    page.on("filechooser", lambda file_chooser: file_chooser.set_files("hello.txt"))
    page.locator("#formFile").click()


def test_select_multiple_3(page: Page):
    page.goto('https://zimaev.github.io/upload/')
    with page.expect_file_chooser() as fc_info:
        page.locator("#formFile").click()
    file_chooser = fc_info.value
    file_chooser.set_files("hello.txt")


def test_download(page: Page):
    page.goto('https://demoqa.com/upload-download')
    with page.expect_download() as download_info:
        page.locator("a:has-text(\"Download\")").click()

    download = download_info.value
    file_name = download.suggested_filename
    destination_folder_path = "./data/"
    download.save_as(os.path.join(destination_folder_path, file_name))


def test_screenshot(page: Page):
    page.goto('https://tp3-test2.etpgpb.dev')
    page.screenshot(path="screen1.png")
    page.locator(".anchors").screenshot(path="screen2.png")
    page.locator(".anchors").screenshot(path="screen3.jpeg", type="jpeg", quality=1)
    page.screenshot(path="screen4.png", timeout=10000)


def test_new_tab(page: Page):
    page.goto('https://mail.ru/')
    with page.context.expect_page() as tab:
        page.locator("//a[@href='https://news.mail.ru/incident/62735352/?frommail=1']").click()
    page = tab.value
    page.locator("(//a[@href='/story/politics/ukraine_conflict/'])[1]").click()


def test_assertions(page: Page):
    page.goto('https://demo.playwright.dev/todomvc/#/')
    expect(page).to_have_url("https://demo.playwright.dev/todomvc/#/")
    input_field = page.get_by_placeholder('What needs to be done?')
    expect(input_field).to_be_empty()
    input_field.fill("задача 1")
    input_field.press('Enter')
    input_field.fill("задача 2")
    input_field.press('Enter')
    todo_item = page.get_by_test_id('todo-item')
    expect(todo_item).to_have_count(2)
    todo_item.get_by_role('checkbox').nth(0).click()
    expect(todo_item.nth(0)).to_have_class('completed')

