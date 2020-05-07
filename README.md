# Łaczenie stron PDF
Łączenie stron w pary by przygodować je do druku

## Użycie
``` shell
./program.py <plik wejściowy>
```

Wymagane jest posiadanie wgranej biblioteki PyPDF2:
``` shell
pip install PyPDF2
```

### Opcjonalne paramerty

```
-r <rozmiar x,rozmiar y> - rozmiar (297,210)
-m <margines x,margines y> - margines (18,10)
-ms <margines> - margines środek (10)
-mo - okłatka ma posiadać margines
-w <plik> - plik wyjściowy
```
