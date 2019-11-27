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
README.md    - Tento soubor
testing.py   - Jádro testovacího programu
config.py    - Konfigurace testů a testovacího běhu
clean.sh     - Vyčistí adresář od veškerých souborů generovaných testy
run_tests.sh - Ulehčení spouštění testovacího scriptu
ifj19.py     - soubor obsahující funkce pro umožnění interpretace jazyku IFJ19 nativním pythonem
ic19int      - interpret stažený ze stránek předmětu IFJ
log.txt      - Vytvořený testovacím scriptem. Obsahuje detailnější záznam testu.
               varování: Tento soubor se smaže při každém spuštění testovacího scriptu

Adresáře:
tests        - Zde se nachází zdrojové soubory jednotlivých testů
outputs      - Vytvořený testovacím scriptem. Obsahuje testy přeložené do mezikódu, které selhaly
               varování: Tento adresář se smaže při každém spuštění testovacího scriptu

Použití:
Upravte obsah souboru "config.py":
	První část tvoří definice statických konstant. Tyto konstanty by neměli být měněny
	V druhé části se nachází konfigurační nastavení, které jsou podrobněji popsány v kódu.
	Třetí část obsahuje seznam všech spuštěných testů společně s očekávanými vstupy a výstupy. Není zde potřeba upravovat pokud pouze testy spouštíte a neupravujete.
Před spuštěním testů je potřeba váš projekt přeložit klasicky pomocí příkazu "make". Tento script poté pouští pouze hotový přeložený program.
Použíjte soubor run_tests.sh pro zapnutí testů (případně upravte parametry modulu pytest podle svého uvážení). Před spuštěním testů je potřeba spustit příkaz "chmod +x" na všechny spouštěné soubory, kvůli přidělení práv spouštět. Jedná se o soubory runtest.sh, ic19int a vámi přeložená binárka překladače IFJ19.
Výstupem je přehled výsledků jednotlivých testů společně se stručnými zprávami o chybách. Detailnější informace o proběhnutých testech lze nalést v souboru log.txt, který byl scriptem vygenerován.

Přidávání testů:
Nové testy lze přidávat jednoduše vytvořením testovacího programu v novém souboru v adresáři tests. Následně pak přidáním testu do konfigurace v config.py ve formátu popsaném v souboru. Pokud chcete poskytnout testy i ostatním studentům, vytvářejte testy v samostatných větvích gitu a poté vytvořte merge request, abych mohl testy integrovat do master větve.
