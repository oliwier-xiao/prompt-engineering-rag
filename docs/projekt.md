# Opis projektu: Uczelniany Asystent Sylabusów i Zasad Zaliczeń

## 1. Wybór tematu

Temat jest wybrany: **Uczelniany Asystent Sylabusów i Zasad Zaliczeń**. Wybór poprzedziła burza
mózgów w rozmowie z Gemini (10 kandydatów), udokumentowana w dzienniku promptów
(`raport/sections/prompty.tex`, wpisy 1 i 2). Pozostałe warianty rozważane na etapie wyboru
(zapis w skrócie):

| # | Temat | Kluczowy atut RAG |
|---|---|---|
| **1** | **Sylabusy i zasady zaliczeń (wybrany)** | Cytowanie regulaminu, odmowa dla spraw spoza bazy |
| 2 | GDD niezależnej gry („Lore Master”) | Model nie zna autorskiego lore |
| 3 | Helpdesk / onboarding IT | Wewnętrzne procedury zamiast ogólnych porad |
| 4 | Dokumentacja techniczna nowszych wersji bibliotek | Omija cutoff wiedzy modelu |
| 5 | Porównywarka publikacji naukowych | Cytowanie stron, hybrydowe wyszukiwanie |
| 6 | Analizator umów B2B / NDA | Wskazanie paragrafu w konkretnej umowie |
| 7 | Ulotki leków i suplementów | Silny guardrail etyczny |
| 8 | Bot eventowy | Dane, których model nie mógł znać |
| 9 | Sprawozdania finansowe | Trudna ekstrakcja tabel (dobre źródło porażek do analizy) |
| 10 | Zamówienia publiczne (SWZ) | HyDE, metadane |

Dlaczego temat 1: dane łatwo zdobyć (sylabusy własnego kierunku), pytania są realne, a **odmowa przy
braku danych** (kluczowy element oceny) daje się demonstrować wprost.

## 2. Idea: bez RAG vs z RAG

Dwa tryby tego samego modelu, te same pytania:

- **Bez RAG:** model odpowiada z wiedzy parametrycznej. Spodziewane: ogólnikowe „typowe normy”,
  zmyślone progi i terminy.
- **Z RAG:** do promptu trafiają najtrafniejsze fragmenty sylabusów. Spodziewane: dokładna wartość,
  cytat z nazwą dokumentu i sekcji, odmowa gdy brak informacji.

## 3. Roadmapa (z rozmowy, doprecyzowana)

1. Pobrać sylabusy (PDF/DOCX) wybranego kierunku do `data/raw/`.
2. Ekstrakcja tekstu i prosty podział po nagłówkach (strategia bazowa), wariant z overlapem
   jako eksperyment.
3. Prompt systemowy wymuszający cytowanie dokumentu i zakazujący wiedzy zewnętrznej.
4. Dokumentacja udanych i nieudanych odpowiedzi (wymóg zaliczeniowy), min. 3 wersje promptu.

## 4. Scenariusze testowe (zestaw `eval/`)

Pytania, na których system musi się „złapać” na odmowie. Rosnąca trudność:

1. **Poza dziedziną (oczywiste):** „Jaki jest przepis na naleśniki?”. Oczekiwana odmowa.
2. **Ta sama dziedzina, brak w bazie:** „Jakie są zasady zaliczania WF-u na innym uniwersytecie?”.
   Model zna to z internetu, ale ma zakaz użycia tej wiedzy. Oczekiwana odmowa z informacją, że
   wgrane sylabusy tego nie obejmują.
3. **Specyficzny szczegół, którego sylabus nie precyzuje (najlepszy pod ocenę 5,0):** np.
   „Czy prowadzący pozwala na 15 minut spóźnienia bez konsekwencji?”. Model bez RAG dopowiada
   „kwadrans akademicki”. RAG ma znaleźć tylko ogólny próg obecności i wskazać, że tolerancji
   spóźnień sylabus nie określa.
4. **Pytania z odpowiedzią w dokumencie:** próg obecności, formy zaliczenia, wagi ocen, literatura.
   Sprawdzają poprawność i cytowanie.
5. **Pytania o przedmiot z innego wydziału/kierunku:** odmowa zamiast zgadywania.
6. **Próby obejścia promptu (prompt injection, „zignoruj wcześniejsze instrukcje”):** część
   omówienia bezpieczeństwa.

Każdy przypadek: pytanie, oczekiwane zachowanie, wynik bez RAG, wynik z RAG, ocena (poprawna /
halucynacja / niepotrzebna odmowa).

## 5. Wstępne ustalenia o stacku (do zatwierdzenia w następnym etapie)

Nic poniżej nie jest zamknięte. Etap 2 to porównanie UI i wybór.

**UI.** Przedmiot to laboratorium prompt engineeringu, nie web developmentu, więc gotowa
biblioteka Pythona zamiast własnego frontu w React.

| | Gradio | Streamlit | Chainlit |
|---|---|---|---|
| Polecany przez prowadzącego | tak (wskazany) | nie narzuca | nie narzuca |
| Czat | prosty, `ChatInterface` | wymaga trochę kodu | natywny, wygląd jak ChatGPT |
| Podgląd źródeł (chunków) | ręcznie | ręcznie | wbudowane kroki/źródła |
| Uwagi | szybkie, wygląda jak panel badawczy | dobre do dashboardów | w tej rozmowie faworyt pod RAG |

Wniosek wstępny z rozmowy: Chainlit ze względu na podgląd pobranych fragmentów na żywo. Do
zweryfikowania na etapie 2 (stan projektów, wsparcie dla polskiego, łatwość demo).

**Model.** Rozmowa wskazała darmowe modele z OpenRoutera (tag `free`). Zastrzeżenie: lista
darmowych modeli i ich dostępność zmieniają się, nazwy z rozmowy trzeba sprawdzić przed użyciem,
a limity i polityka logowania danych mogą wykluczać wysyłanie wrażliwych dokumentów.

**Embeddingi.** Lokalnie, `sentence-transformers`; do sprawdzenia modele radzące sobie z polskim.

**Wektorówka.** ChromaDB (lokalna, bez osobnego kontenera). Szkic: Python, LangChain,
PyPDFLoader.

## 6. Ryzyka i ograniczenia (zalążek rozdziału do raportu)

- Sylabusy mogą mieć ograniczenia licencyjne i zawierać dane osobowe prowadzących: dane surowe poza
  gitem, publikować tylko to, co wolno.
- Wysyłanie dokumentów do zewnętrznego API (OpenRouter) a zasady przedmiotu o danych objętych
  ograniczeniami.
- Halucynacje mimo RAG: złe chunki, pominięte fragmenty, tabele w PDF, model „uzupełniający”
  brakującą wartość.
- Odtwarzalność: modele LLM niedeterministyczne, darmowe modele znikają. Zapisywać nazwę modelu,
  datę, temperaturę i seed (jeśli dostępny).
