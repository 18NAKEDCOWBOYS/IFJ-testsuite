TESTING FRAMEWORK FOR IFJ20

Autor: Kamil Michl

Upozornění: Autor tohoto repozitáře NERUČÍ za správnost a korektnost vytvořených scriptů ani testů.
Upozornění: Funkčnost scriptu je ověřena na servru merlin, na jiných strojích se může postup spuštění a instalace lišit.

Základní myšlenkou testování je porovnání výsledku IFJ překladače a interpretru s výsledkami stejného programu v jazyce go.
Tento framefork je založený na python modulu pytest.

Soubory:
README.txt   - Tento soubor
install.sh   - Nainstaluje a nastaví potřebné prerekvizity
testing.py   - Jádro testovacího programu
config.py    - Konfigurace testů a testovacího běhu
clean.sh     - Vyčistí adresář od veškerých souborů generovaných testy
run_tests.sh - Ulehčení spouštění testovacího scriptu
ifj20.go     - soubor obsahující funkce pro umožnění interpretace jazyka IFJ20 nativním interpretem jazyka go
ic20int      - referenční interpret ze stránek předmětu IFJ
log.txt      - Vytvořený testovacím scriptem. Obsahuje detailnější záznam testu.
               varování: Tento soubor se smaže při každém spuštění testovacího scriptu

Adresáře:
tests        - Zde se nachází zdrojové soubory jednotlivých testů
outputs      - Vytvořený testovacím scriptem. Obsahuje testy přeložené do mezikódu, které selhaly
               varování: Tento adresář se smaže při každém spuštění testovacího scriptu

Instalace:
Pro instalaci na servru merlin použíjte příkaz "chmod +x ./install.sh" a poté script "./install.sh".
Dále je nutné před použitím mít připravený spustitelný program překladače jazyku IFJ20, který vytváříte.

Použití:
Upravte obsah souboru "config.py":
	První část tvoří definice statických konstant. Tyto konstanty by neměli být měněny
	V druhé části se nachází konfigurační nastavení, které jsou podrobněji popsány v kódu.
	Třetí část obsahuje seznam všech spouštěných testů společně s očekávanými vstupy a výstupy. Není zde potřeba upravovat nic pokud pouze testy spouštíte a neupravujete.
Použíjte soubor "run_tests.sh" pro zapnutí testů. Výstupem je přehled výsledků jednotlivých testů společně se stručnými zprávami o chybách. Detailnější informace o proběhnutých testech lze nalést v souboru log.txt, který byl scriptem vygenerován.

Přidávání testů:
Nové testy lze přidávat jednoduše vytvořením testovacího programu v novém souboru v adresáři tests. Následně pak přidáním testu do souboru "config.py" ve formátu popsaném v souboru. Pokud chcete poskytnout testy i ostatním studentům, vytvářejte testy v samostatných větvích gitu a poté vytvořte merge request, abych mohl testy integrovat do master větve nebo mě kontaktuje přes discord "kam29#4080"
