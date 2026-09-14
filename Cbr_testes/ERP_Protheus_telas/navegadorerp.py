from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(
        "https://forride214654.protheus.cloudtotvs.com.br:11154/webapp/"
    )

    context = browser.contexts[0]
    page = context.pages[0]

    page.get_by_placeholder("Pesquisar").click()
    page.get_by_placeholder("Pesquisar").fill("MNTA655")
    page.keyboard.press("Enter")

    input("Enter para sair")