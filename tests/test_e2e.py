import os

import pytest
from playwright.sync_api import expect, sync_playwright


BASE_URL = os.getenv("CALCULATOR_BASE_URL", "http://127.0.0.1:8000")


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def calculator_page(browser):
    page = browser.new_page()
    try:
        page.goto(BASE_URL)
        expect(
            page.get_by_role("heading", name="Calculator", exact=True)
        ).to_be_visible()
        yield page
    finally:
        page.close()


@pytest.mark.parametrize(
    ("button", "a", "b", "expected"),
    [
        ("Add", "2.5", "3", "5.5"),
        ("Subtract", "2", "5", "-3"),
        ("Multiply", "-2", "4", "-8"),
        ("Divide", "5", "2", "2.5"),
    ],
)
def test_calculator_buttons(calculator_page, button, a, b, expected):
    calculator_page.get_by_placeholder("First number").fill(a)
    calculator_page.get_by_placeholder("Second number").fill(b)
    calculator_page.get_by_role("button", name=button, exact=True).click()

    expect(calculator_page.locator("#result")).to_have_text(
        f"Calculation Result: {expected}"
    )


def test_calculator_recovers_after_division_by_zero(calculator_page):
    calculator_page.get_by_placeholder("First number").fill("5")
    second_number = calculator_page.get_by_placeholder("Second number")
    divide_button = calculator_page.get_by_role("button", name="Divide", exact=True)
    result = calculator_page.locator("#result")

    second_number.fill("0")
    divide_button.click()
    expect(result).to_have_text("Error: Cannot divide by zero!")

    second_number.fill("2")
    divide_button.click()
    expect(result).to_have_text("Calculation Result: 2.5")