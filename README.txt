TESTING FRAMEWORK FOR IFJ19

Autor: Kamil Michl

Upozornění: Autor tohoto repozitáře NERUČÍ za správnost a korektnost vytvořených scriptů ani testů.

Tento testovací script je primárně určen pro použití na serveru merlin. Pokud ho chcete používat jinde, pokyny k instalaci a použití se mohou lišit.

Základní myšlenkou testování je porovnání výsledku IFJ překladače a interpretru s výsledkami stejného programu v pythonu.
Tento framefork je založený na python modulu pytest.

Prerekvizity:
Pro instalaci tohoto modulu na serveru merlin použíjte následující příkazy:
	pip install pytest --user
	pip install pytest-timeout --user
Poznámka: Pro spuštění mimo server merlin potřebujete především nainstalovaný python3

Soubory:
README.md - Tento soubor
testing.py - Jádro testovacího programu
run_tests.sh - Ulehčení spouštění testovacího scriptu
ifj19.py - soubor obsahující funkce pro umožnění interpretace jazyku IFJ19 nativním pythonem
ic19int - interpret stažený ze stránek předmětu IFJ
log.txt - Vytvořený testovacím scriptem. Obsahuje detailnější záznam testu.
          varování: Tento soubor se smaže při každém spuštění testovacího scriptu

Adresáře:
tests - Zde se nachází zdrojové soubory jednotlivých testů
outputs - Vytvořený testovacím scriptem. Obsahuje testy přeložené do mezikódu, které selhaly
          varování: Tento adresář se smaže při každém spuštění testovacího scriptu

Použití:
V souboru testing.py upravte konstanty v sekci "CONFIGURATION":
	V první části se nachází konfigurační konstanty, které jsou podrobněji popsány v kódu.
	Druhou část není potřeba upravovat pokud pouze testy pouštíte a neupravujete. V této části se nachází seznam testů ve formátu (zdrojový_soubor, návratový_kód_překladače, návratový_kód_interpretru, vstupní_data).
Před spuštěním testů je potřeba váš projekt přeložit klasicky pomocí příkazu "make". Tento script poté pouští pouze hotový přeložený program.
Použíjte soubor run_tests.sh pro zapnutí testů (případně upravte parametry modulu pytest podle svého uvážení)
Výstupem je přehled výsledků jednotlivých testů společně se stručnými zprávami o chybách. Detailnější informace o proběhnutých testech lze nalést v souboru log.txt, který byl scriptem vygenerován.

Přidávání testů:
Nové testy lze přidávat jednoduše vytvořením testovacího programu v novém souboru v adresáři tests. Následně pak přidáním testu do konfigurace v testing.py ve formátu popsaném dříve. Pokud chcete poskytnout testy i ostatním studentům, vytvářejte testy v samostatných větvích gitu a poté vytvořte merge request, abych mohl testy integrovat do master větve.
