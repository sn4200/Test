import requests
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def google_item_info_api(request, sku):
    bezeichnung = str(sku)
    try:
        url = f"https://www.google.com/search?q={sku}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.ok:
            soup = BeautifulSoup(resp.text, "html.parser")
            # Suche nach erstem Link zu autodoc.de
            autodoc_link = None
            for a in soup.find_all("a", href=True):
                if "autodoc.de" in a["href"] and a.text.strip():
                    autodoc_link = a
                    break
            if autodoc_link:
                bezeichnung = autodoc_link.text.strip()
    except Exception:
        pass
    return JsonResponse({"name": bezeichnung})

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def item_info_api(request, sku):
    from .models import Item
    item = Item.objects.filter(sku=str(sku)).first()
    if item:
        data = {"name": item.name}
    else:
        data = {"error": "Artikel nicht gefunden"}
    return JsonResponse(data)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TouchGoodsReceiptForm
from .models import Item

@login_required
def touch_main(request):
    message = None
    if request.method == "POST":
        form = TouchGoodsReceiptForm(request.POST)
        if form.is_valid():
            artikelnummer = form.cleaned_data["item_name"]
            quantity = form.cleaned_data["quantity"]
            # Prüfe, ob Artikel mit dieser Nummer existiert
            item = Item.objects.filter(sku=str(artikelnummer)).first()
            if not item:
                # Bezeichnung aus Web-API holen
                import requests
                from bs4 import BeautifulSoup
                bezeichnung = str(artikelnummer)
                try:
                    url_json = f"https://world.openfoodfacts.org/api/v0/product/{artikelnummer}.json"
                    resp = requests.get(url_json, timeout=5)
                    if resp.ok:
                        data = resp.json()
                        if 'product' in data and 'product_name' in data['product'] and data['product']['product_name']:
                            bezeichnung = data['product']['product_name']
                        else:
                            # Fallback: HTML-Seite von OpenFoodFacts parsen
                            url_html = f"https://world.openfoodfacts.org/product/{artikelnummer}"
                            resp_html = requests.get(url_html, timeout=5)
                            if resp_html.ok:
                                soup = BeautifulSoup(resp_html.text, "html.parser")
                                h2 = soup.find('h2', class_='title-1')
                                if h2 and h2.text.strip():
                                    bezeichnung = h2.text.strip()
                            # Fallback: autodoc.de
                            url_autodoc = f"https://www.autodoc.de/search?keyword={artikelnummer}"
                            resp_autodoc = requests.get(url_autodoc, timeout=5)
                            found_bs = False
                            if resp_autodoc.ok:
                                soup = BeautifulSoup(resp_autodoc.text, "html.parser")
                                for li in soup.find_all("li", class_="product-description__item"):
                                    title = li.find("span", class_="product-description__item-title")
                                    value = li.find("span", class_="product-description__item-value")
                                    if title and value and "Artikelnummer" in title.text:
                                        bezeichnung = value.text.strip()
                                        found_bs = True
                                        break
                            # Wenn BeautifulSoup nichts findet, versuche Selenium
                            if not found_bs:
                                try:
                                    from selenium import webdriver
                                    from selenium.webdriver.chrome.options import Options
                                    from selenium.webdriver.common.by import By
                                    from webdriver_manager.chrome import ChromeDriverManager
                                    chrome_options = Options()
                                    chrome_options.add_argument('--headless')
                                    chrome_options.add_argument('--no-sandbox')
                                    chrome_options.add_argument('--disable-dev-shm-usage')
                                    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
                                    driver.get(url_autodoc)
                                    # Warte kurz, bis die Seite geladen ist
                                    import time
                                    time.sleep(2)
                                    # Suche nach Produktbeschreibung
                                    items = driver.find_elements(By.CLASS_NAME, "product-description__item")
                                    found_artikelnummer = False
                                    for item in items:
                                        try:
                                            title = item.find_element(By.CLASS_NAME, "product-description__item-title")
                                            value = item.find_element(By.CLASS_NAME, "product-description__item-value")
                                            if "Artikelnummer" in title.text:
                                                bezeichnung = value.text.strip()
                                                found_artikelnummer = True
                                                break
                                        except Exception:
                                            continue
                                    # Fallback: Produktname, falls keine Artikelnummer gefunden
                                    if not found_artikelnummer:
                                        try:
                                            # Versuche Produktnamen aus erstem Suchergebnis zu holen
                                            name_elem = driver.find_element(By.CLASS_NAME, "product-description__name")
                                            if name_elem and name_elem.text.strip():
                                                bezeichnung = name_elem.text.strip()
                                        except Exception:
                                            try:
                                                # Alternativ: Linktext des ersten Produktes
                                                link_elem = driver.find_element(By.CLASS_NAME, "product-link")
                                                if link_elem and link_elem.text.strip():
                                                    bezeichnung = link_elem.text.strip()
                                            except Exception:
                                                pass
                                    driver.quit()
                                except Exception:
                                    pass
                except Exception:
                    pass
                warehouse = None
                from .models import Warehouse
                warehouse = Warehouse.objects.first()
                item = Item.objects.create(name=str(artikelnummer), sku=bezeichnung, quantity=0, warehouse=warehouse)
            item.quantity += quantity
            item.save()
            message = f"Wareneingang für {item.name} ({item.sku}) erfolgreich gebucht!"
            form = TouchGoodsReceiptForm()
    else:
        form = TouchGoodsReceiptForm()
    # Artikelnamen für datalist
    return render(request, "goods_receipt_touch.html", {"form": form, "title": "Wareneingang Touch", "message": message, "standalone": True})
