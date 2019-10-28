TESTING FRAMEWORK FOR IFJ19

Autor: Kamil Michl

Autor tohoto repozitáře NERUČÍ za jeho správnost a korektnost.

Základní myšlenkou testování je porovnání výsledku IFJ překladače a interpretru s výsledkami stejného programu v pythonu.
Tento framefork je založený na python modulu pytest.
Pro instalaci tohoto modulu na serveru merlin použíjte následující příkazy:
	pip install pytest --user
	pip install pytest --user-timer

Soubory:
README.md - Tento soubor
testing.py - Jádro testovacího programu
run_tests.sh - Ulehčení spouštění testovacího scriptu
ifj19.py - soubor obsahující funkce pro umožnění interpretace jazyku IFJ19 nativním pythonem
ic19int - interpret stažený ze stránek předmětu IFJ

Adresáře:
tests - Zde se nachází zdrojové soubory jednotlivých testů
outputs - Vytvořený testovacím scriptem. Obsahuje testy přeložené do mezikódu, které selhaly
          varování: Tento adresář se smaže při každém spuštění testovacího scriptu

Použití:
Obsah kořenového adresáře tohoto projektu nakopírujte do kořenového adresáře projektu (vyžaduje Makefile ve stejném adresáří jako testing.py).
V souboru testing.py upravte konstanty v sekci "CONFIGURATION":
	V prví části se nachází seznam testů ve formátu (zdrojový_soubor, návratový_kód_překladače, návratový_kód_interpretru, vstupní_data)
	V druhé části se nachází konfigurační konstanty, které jsou podrobněji popsány v kódu
Použíjte soubor run_tests.sh pro zapnutí testů (případně upravte parametry modulu pytest podle svého uvážení)
