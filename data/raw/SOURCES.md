# Data sources

Every series used in the CESI construction is drawn from a public source. This file lists each series, its source, accession date, and licence. Raw files themselves are not committed to the repository (see `.gitignore`); re-fetch them from the URLs below.

| Series | Source | Accession | Licence |
|---|---|---|---|
| Primary energy consumption (E), EJ | Energy Institute, *Statistical Review of World Energy 2024*; Our World in Data substitution method | 2024 | CC-BY |
| Electricity generation (X), TWh | Energy Institute, *Statistical Review of World Energy 2024* | 2024 | CC-BY |
| Industrial production index (I) | World Bank / UNIDO INDPRO global aggregate | 2024 | World Bank terms |
| Population index (P) | UN Population Division, WPP 2024 revision | 2024 | UN terms |
| Global oil reserves (R) | BP / Energy Institute historical tables | 2024 | CC-BY |
| Global oil production | Energy Institute | 2024 | CC-BY |
| Civilisational EROI step function | Cleveland (2005); Hall et al. (2009); Murphy & Hall (2010); Lambert et al. (2014) | n/a | peer-reviewed literature |
| OPEC reserve haircut constant | Salameh (2004); Simmons (2005); Laherrère (2006); Bentley et al. (2007) | n/a | peer-reviewed literature |
| FAO Food Price Index | Food and Agriculture Organization | 2024 | FAO terms |
| World Bank Fertiliser Price Index | World Bank Pink Sheet | 2024 | World Bank terms |
| US Energy CPI (CPIENGSL) | FRED / BLS | 2024 | FRED terms |
| UCDP State-Based Armed Conflicts | Uppsala Conflict Data Program | 2024 | CC-BY |
| OECD Real Wages Index | OECD | 2024 | OECD terms |
| Global real GDP | World Bank WDI | 2024 | World Bank terms |
| US M2 | FRED / Federal Reserve | 2024 | FRED terms |
| WTI, BCOM, XLE, GLD, SPX | FRED, S&P, Bloomberg (via public endpoints) | 2024 | respective terms |

If any series is revised upstream after the accession date above, numerical results may shift slightly; the qualitative findings are robust to the perturbation sizes reported in R1.
