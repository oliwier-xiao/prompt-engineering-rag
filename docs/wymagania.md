# Wymagania przedmiotu (Prompt Engineering, laboratorium)

Źródło: materiały organizacyjne przedmiotu. Temat **12. Asystent analizy dokumentów typu RAG**:
kategoria RAG, poziom zaawansowany, ocena bazowa **5,0**.

## Temat 12

- **Cel:** aplikacja odpowiadająca na pytania na podstawie wskazanego zbioru dokumentów.
- **Minimalny zakres:** przetwarzanie dokumentów, fragmentacja, wyszukiwanie kontekstu, odpowiedzi
  ze wskazaniem źródeł i ograniczanie halucynacji.
- **Zagadnienia prompt engineeringu:** prompty osadzone w kontekście, cytowanie, odmowa przy braku
  danych, ocena wierności.
- **Oczekiwany rezultat:** działający prototyp oraz porównanie odpowiedzi bez RAG i z RAG.
- **Możliwe modyfikacje:** zmiana dziedziny dokumentów, strategii fragmentacji, wyszukiwania lub
  ewaluacji.

## Przebieg zajęć

| Etap | Główne działania | Rezultat kontroli |
|---|---|---|
| Start | Wprowadzenie, zasady zaliczenia, utworzenie zespołów | Wybór tematu |
| Planowanie | Doprecyzowanie celu, zakresu, narzędzi i kryteriów sukcesu | Plan pracy |
| Prototypowanie | Pierwsza wersja rozwiązania oraz kluczowych promptów | Działający rdzeń lub pierwsza kompletna wersja artefaktu |
| Iteracja | Testy, analiza nieudanych wyników, modyfikacja promptów i zakresu | Porównanie wersji promptów i udokumentowane wnioski |
| Finalizacja | Dopracowanie rozwiązania i raportu | Gotowy projekt i raport |
| Zaliczenie | Krótka prezentacja projektu i odpowiedzi na pytania | Oddanie raportu i materiałów |

## Ocena

Poziom zaawansowany (system łączący kilka komponentów, RAG, agentów lub zaawansowaną ewaluację):
ocena bazowa 5,0. Wymagania: poprawna architektura, bezpieczeństwo, rzetelne testy i analiza błędów.

Ocena może zostać **obniżona** m.in. za:

- niepełną realizację uzgodnionego zakresu,
- istotne błędy merytoryczne, techniczne lub metodologiczne,
- brak systematycznego testowania i iteracyjnego doskonalenia promptów,
- brak analizy nieudanych rezultatów, halucynacji i ograniczeń,
- źle przygotowany raport,
- niesystematyczną pracę podczas zajęć albo nierówny, niejasny podział pracy,
- naruszenie zasad etycznych, prawnych, bezpieczeństwa lub ochrony danych.

## Minimalne wymagania wspólne

1. Co najmniej **trzy istotnie różniące się wersje** kluczowego promptu lub zestawu promptów.
2. Analiza nieudanych albo problematycznych rezultatów.
3. Opis zastosowanych technik promptowania i uzasadnienie najważniejszych decyzji.
4. Omówienie zagrożeń etycznych, prawnych, prywatności i bezpieczeństwa.
5. Repozytorium kodu lub uporządkowane archiwum wszystkich istotnych materiałów.
6. Informacja o użytych modelach, narzędziach, ustawieniach i ograniczeniach odtwarzalności.

## Raport końcowy (PDF, termin: ostatnie zajęcia w semestrze)

Raport może być generowany przy pomocy AI, ale należy to wspomnieć w dokumencie i wskazać
zastosowane narzędzia i prompty. Wymagane sekcje:

1. Strona tytułowa i skład zespołu.
2. Cel i zakres.
3. Opis zastosowanych narzędzi, modeli i architektury rozwiązania.
4. Opis strategii promptowania oraz kolejnych wersji kluczowych promptów.
5. Wyniki, przykłady odpowiedzi i porównanie iteracji.
6. Analiza błędów, halucynacji, ograniczeń i zagrożeń.
7. Wnioski.
8. Podział pracy członków zespołu.
9. Odnośniki do kodu, danych i pozostałych materiałów.

Szkielet w `raport/sections/` odpowiada tej liście 1:1.

## Prezentacja

- Krótkie omówienie celu i zakresu.
- Demonstracja najważniejszego rezultatu lub działania prototypu.
- Pokazanie przynajmniej jednej istotnej iteracji promptu i wynikających z niej poprawek.
- Omówienie sposobu ewaluacji, napotkanych problemów i ograniczeń.
- Gotowość wszystkich członków zespołu do odpowiedzi na pytania.

Forma: działający prototyp i/lub artefakty. Prezentacja w PowerPoint nie jest konieczna.

## Zasady korzystania z GenAI

- Wykorzystanie GenAI jest istotą projektu, ale zespół odpowiada za weryfikację wszystkich wyników.
- Dokumentować najważniejsze prompty, iteracje, użyte modele i ustawienia.
- Nie przekazywać do zewnętrznych usług danych osobowych, poufnych ani objętych ograniczeniami
  licencyjnymi.
- W raportach i materiałach oznaczać treści wygenerowane lub istotnie przekształcone przez AI.
- Nie naśladować stylu żyjących twórców ani nie wykorzystywać cudzej tożsamości, wizerunku lub
  głosu bez podstawy.
- Kod wygenerowany przez model uruchomić, przetestować i przeanalizować pod kątem bezpieczeństwa.
- Źródła, dane i zasoby zgodne z zasadami przedmiotu i właściwie opisane.
