"""E22 Q0 8C9S calendar v2: recurring external placement and harvest days.
Reconstructed from public actions, not the competitor source code.
Calendar from observed public actions; current-state service checks. No future data.
"""
import base64,zlib,json,copy
_PLAN=json.loads(zlib.decompress(base64.b64decode('eJztXU1vXEeS/C8690GkRFncGy1xbGFo06CoFWYNwTCwMxhgMXvw7m2x/31Jdr+PqoyMiKz3KM9i5qRWd7NfVVZWVmZkZNbP//PiL7/+9rc///biX35+8dPVx48vvhxe/PXX//z3/3p44+Hl33797T/+/N8Pr39+8e2nP/3y093t+0/v7l8cXnz+/vrq4d9vvhyST85fPn708frmZnnvzcsvX/73sH7kj7d399/nz2z//OxV+rSLx0++/3B3/cJ98fgzVz9++OHq8QHvbj8/jDi8/fH76+ufHj/oRv3x9lM76gfZfXj3x08/nX7q8YdOwlymuH7Vfns95+5J8xePQ2keufo59qxvP324ef/Lw1fuPz1O3XnYUajNw7pfkRO8uXp3bcwvrH/3p/g5n68/3j+9eHclpnT6piu1+Yd7ucet8PH6+v3D5z9c39z+CFSklxcfwcOcf7yffy15p1sdNaSzfkiTYIEqgadNQ/t8dX991796EhMR+x8eR9I8Yfnj5ZcnYVu6ak3xqA/Nc+cVzWW9fKeVUHnRo7ZZgo1fOspvZIWbHzLlv3wW91Pz3MkOh3mffmD1vMlEAsFP1mU9gqBQ3nODvONyRzH3z1diflUQM1vvKO7u23vIHawzk/vx2+UH957C8wg+7K/4WCJvvdHYURgnCAQLDpBnFChZ0NMA1GMLAl1+2xEoOJI2CbR/VOmHyc91L4Z8oVbImYep/Rxw/IFl1CdMP1D41sCJvQzr9JnxK/H8nf/29JHzI7c3N9fv7n/5w/Xd/YebD//Wm7j5l+AXKw4v8OOT35w8g+5tuO9OQcvqqw/7PQtcwuFyfdWv8HKU9o6qEaClXmAmXT7T5NFgyo6tmXZjDC5SO2pMMH9OkOSYXVl+5nmGCfbvpvHOluaoWzuPdrEOW2x1su826Dl51lWuZQOny6a12fmkiyv8z6HUT/vDa4VIBeMuISd53lI8RetYPHpZoM0OrsxZVOcye5489BEQxH5P6gURcBd2bhYvQkjk+GxpnhyCkjSBm7httJa6knB+ozS3uox0sHLyCO4Fw51+8Puru38dwzOIlGctGAm+LHHPw94QxtrrsIKHnGBW+sgb1Rs4vc0ZkDtT+XqDk+L1FAa0iYc5OlAgQZtj4KZtQE2oDQb4oRQr+0GAgp+UwlgnIoA4TumIkO3xlRCJgmvyqgxFSF+EJUmsV6WDI/dGxIkc0oEF9L/6rKJd2+s5CCaKB0z2YmwZgMmonLxR5nHAiyyaQ2bskFRrEaJzZg2zs67VtADS0HWKc8TnbBmtjcfeOnOFp9VaWvsoYAm85RUR9Zi5DQ5+J05wQuzrl6C5WSpTcBm5gupD0PttiBoOOUKv/EcxwwE9opnR0XtE2x1LFDeNzF/44z2YBM/0BDfwN8b8uAEPgnlhy++m/BX5+/baTMIFiUjytIFjH3htxoNG3LiMq1J26y42uXWOdrEMz16QE/WDntnNGvKu5t1roRgSIosyzpM3Y95Vl0YrOmtCvrnP6vw6CyNi1DyCOQEQZMCvKh8us8yBK8K9qp0d2uiJZGmTEQcFHeM0Y+amYkjwMa8ozamNmgkABhAtARM57Ks/zUqiLCtVJcfIxz2YaAjgZ21IZhLgEjzIwHmc5Cv7PXfgdRS+MAsCU8af2yB98pz3d7c/VT0TEAJc4F93nFEOhG7Lk48+Xm4b2wNzfhwsT+f8nTeTgJZ2emKKCS8/hdg3HWM6e4pwb4B1mX4OTimxPTuhhpuyd/MfRxFt91Mz0pN1uhEhI3hks9M3m6IoiSGEvxYZa0brMmmuTsn2X53fH+/vrj5/e3139yeg2yg4UM/bNjEAUIgcXIEqFhHP1ew9dz6OeD5Ncsy4bnu97Ori+nMff73GFTfFnZH7KCvlChZ+F5wFJMOAEox5LgzdHgQtMw31bdxJMTcmuCE+OUCzS+azjcM3lNcW5XWlgjnL+XFKYpCnwI73lM6ceDH9EJZ1h5kTyZ/uRjgfkwbzurTF5h9OkSLgvyXHYm0nrndG6g/ht7RSx70ZPQQw9fiZmufivt7ePvzzxvDDJ0D69Ad4AKvyKOwQ9PE9GVQe+MzVpw/G4zhfUqG6/HUx8lhEn0xFuTzzDySZA+P83zqHkKoAOR/gOBA+CFsSx4UBvmOktINRxjAdlNmCcPx834NrAQkSVCrnPpmFR2fucQFG2aVYcgbf+q0ox0IZdBgDME8O0ePQjd5QuTkf6oQscaDgdOjp+YajEqtP5YPBxqOZCllxqgtl4ODpDlTGD61pZ+/MYOBg8TlYTMh9yESYMT/ga320s2lVTupVo9ENlAGAwJjuekFrT1ap32qkYIrqWbJSjJFDtuLKl6yFbLQWmIacB4wbGLyoS22Ror+AkkvgbCzst3N3JdHh4q0dzTx+rbXDmy4PEYkfGs8SgiPvETSOJa+yKO3Ydwb0U1l7bma1y5M8Xq4Hi53vSloz6/RyQPEVc6Y0H8A/ylAaksitBFFHEHllUq75sWsHeBrNw/7rUjAcXBL1Fyyio45sXCmJY4+GZNHbzCNkFngN71J3KAcU+lgJKQ4xsZzBrFzxIMqPnygzYQqYTJYUWRfJLGFXyr1Dw7HWCBwoYheCvWGUdPqAOIiRBVl1GkcuJ+lb0oMVPRRUpUT6dHaqVwMCR0Z0Rx3tNSoNSyvIhXdQ3WjECW989d7edtF8LcOY14Mmru6yBf0EoV2UFZxKNIK0iLMTzqh+6UHlhWFp2mWoWBKxjf1YNidtZyfExiWCswXvWXQ/jbSjhCaT96bmCgwgA2/xk5iD1mYMDRoLerFWOJPyPi3m4pRjLktnCk7zrqm4jXEWMJXwTIS8JZot20xPaUJddqyBD+fdkwO4g/QKDgSvxwwEGiVWGsXsD6FHL9nJ00n7w4ebP55yW5rPkjPejz9zBjJQU2/XLyBwnhuohr+iChpThjEbCIDm0Cw1DUOWP0adFq10CuXdKR9bIdExubZMqd+rI9g5OqTj9uHk8gOB7dr1qYX11AmOzwG7oeMKHfLABedfxqppYqTJkpB9M1YOmW/hHYE8NhBVjMd1UFzKXtVZ8z77Ls4CmAnRU5WOlQBe2OrTOLLzuEY2sFm+IV18yi/ajMctQwLcKyWlHkAcEVPcDetcd06LxDLy6LcmPuiXYoGVScsHDgBV2UvlY/ECXlVMFZw/Pq7AbowB4Meb/MdGVpKM6LPDKdWR7Tfjw1JuAP0eKF8Ly8oJ1aJGwKWO4jxaeiayMfkjkC2ooZNWeLZFREWvEE2DrL3npDx3Um+MEgryNprheUgCTbpaoXVOM+nJWemjlSpDLW48YyxtlCzyl15D0K0urV3VAtzHGGlHs6JpRaL5AqzDVaGW6hY8FE6ZEiVuY4xRVCgYMcGif+aMBsSb2K2d/ahuAz5vjIW8HJVp9CmtJhZQMQAgOm1Jx68TY8cZcg134a3Bo4gOAHK0OapVVTeWlgVsepGJz9lTlcAU2vpBbgpB0NWmzpNl5eQGFbPGRBLJFo+Xsdym5wNW5rBZHdVpUe7dtAGRo24iapwQfXt55AKpYHvPzvwKr7euJR6RUpqPKBxdT+KHpbWrWSjBVaKuBW4tLH1ys+ak36Am9eYJPzPfydAiWmfjk61VPDorz3yKM19I+g1eQVKWDOV6e6BBbiGALadFK9BGBfV/nvh0Lz4qecE2ED/txSWF393efryWybRwspBZcH+PvwINzNgvGxm2MK35l7/OjIDt8UE/xrhzB0CwqJTadZS7764FJcfVsaxUgZ8fPH3Q2VD/ZiFRtaryC9l3sUEHLSzU+EipZZIFiQ4JehUdvuGWX9YQeRMwkPBlAJzT1aA4Kly1EoEMcY/T6Ya5N42ImVux/gO8sUBpb9tCKUG7ll9O6sDCgKmA0B/QHwENxk0C/HRNX17UfJEctUEY2O8PgwZblM/cs/M82GNzP3P6yFASBxo1pUMDrlaKzI6pclgdeEZ4ZKyj0yInZbPTI79pmo2ca8NkcjLqOgeR2L1j5eS7275bjvThI5XpJD/jZL+Y1lOE2LwdRjd0rqc5hRlw8GSEyy84TpRXlNiyVRUUjryqDyERUUF1jfzgxiOFzbFmQhDj3d3GvPhkQ7UExLNzaNwXizjPodNAwL6gFCA1JT2TRLcMWnlc+2meixlkuWhY3wkq6ujFl0fJlZE30kwAwI+ivRJoVBuAuExGDNWxa7ZzLnwkusG23vlGF0WM3Ysd1sG5kpf2/gqfgeRogGsLNRTOcMiLWt2jRJKCyRf+2wF6qGdPqjZ8pQ6C84PirzY0SzuMI2HTbsEthU54kqQ7tFuOdyShrGiQtgnvsIbs1UZg/QEV5jlCW41J6bXhizMz+ou9Qm+erw1RXjmVM0hKVDFajURoAsu5Ji1k10VoILVIVc9uc5o1hMpHjlLl8fRQ1WlFtiXw4CK7GYZFXGP4eLEjtG3HmC0Am1ADzQG1vmPcdru7ka9k7BotHwGlBJ5GyyqZ1Y1s/Pzmds4UgT0VTKNVysBuKyYAQLrixtMrqZPFsZvtDq3ZwfIg/VvtUSAFcz0higGsA1ZpUYjKEewMApB1VwXO7O5t9jinJbo7ojUUbgjHNwerdFNWXu4nc14gmcV5WP6eIZmt8TIPxrjHCQOL5WAaANNieZtXqVQEr4ftWDBawK22bud9Hp0KmuLmHeul2FauMr/lLrFalVKm8fp5VNERFg2Y62iSENphXpc5xlPkpt79NF8DhiSF1nVmRV0MI2jb5nwOhl3e1kaB6QNIcI9ZA30JTplQVCIQbLUEfw+0o2/qAdNTrocxQdoN7n6Rlg6W0kisizjtplu5Bwxs2egfYoYHbXNREUOkLygKMUg7+d9kJ0mSf5nrDCrxgFekQLsaoXOC1y0A0BRoDSmIiR/5jFWozyDcoHVckQwD3MsRvbaVSjqv4NzsPIiqkKQyMWOArxNxPWzSG7ptfkJtFE10GVngkWPRsl3GAWjGZaMXZwNP2dVE+7JKbk/2czfVgEHAzZzktE1VKfAATL9oRMDIPFFpodhKl3EiM9UbC3Tq+gYSnl5vsNQ3GFY51zKC2nsVaNIimEFRE8ZyzPOzqID1oBhwweGxG58Rx5jf/V7bE7bKsXSQGY/IuBTwMlT9h78j8qT8QNt+kGMCd2P51AWamdpETxihLowHkSjme0qt7RJU6i4gMQGdb5RDDDEOScJa5w9DU/XBu3SsGhuUkcjG/xq9STPmqpAuT8PHN5PR5gFyzY2klGFRlJAllgcdWVbGgKh7wu5KkhLpGwiYmkAWdl8++y6yjBwZd5S28DZJmqPRnNS5tU01cp5jADizG6LGFZg8W0rOCZmCJSFoSp+oJqcNAWaenUirtzXRR0ad/8ia9oKIe6j0upjz57uAJhCyC5zLY/Qy3cAWDujg6Hb22lSbknOZBqWtwhNAZlGlX2sIbgsn+R87m9GZFzaAQk9kLhGn7pGamhKYwZJQ6JaCIWyN9fwYjNPFEpaSTQcH/WM8sujQ8gY9uYhLcSZT+vorgFhpqZTUPn+BhIS6cNut4r37AzZmNStZS+Y9PmcCU2oxMLtpnWl3d4kM2s4buyVD7KcbwpL7Zx8/yhnvgboCgz+ojGz+wIwsXyctRDLEo0lxvJLnJdoVoh6dZZArwQ7pwvsZHUgRNWKAzUhpGrkqI3dagYqGGELGAdJpZdSR2JAGYG6kpqdLwAadAgETOoWW3n9WIecpfRyXsFD4Q2axbieYrLfd44JVmABUA8L3GrRxG2XH/A+6wi/WRw5WnjEPwKEQFdjs3YT23S+KXu9tsV1CVOZqsoQasopmCF7LtKDFkQ4KSY4DXHMAGkELAxgOJiXZ6kRnXODIT9VZWt5eAIIq9tf04Q91RbMZ4IxyCKT7xBqWARCRIf1S2XCjkRTtSteX6R76aikWo8ClqA5y+UH8T8rbBaRRGdRPubJorgbRlNhaBZjMuqV7ShnmbFl9nB0lVhNErCVMRJ6nKOu/c+BaVK7UmWujORECr/mN8Pevv/vu5In+zlxewhHMWIatZtBC2ljAGeWb1onjePj1UP+91Knuyp1DD0Ava2k1i6F9Ed2mRpzxCQbJ0+ZGOr7kKxHyK9E0mkCXoyCXTMVoOXbGoEhdsIUbXCD7quPYEAODJCTNSYZJWtxJm1prjsFz+fBwY47JmXu/J0MCC+0WWRVk1lJmH3cUUTnyVlatg1e5jaLgR8RNRp0m8AifFN7ug5Iqt7IAt05uK3PwI+C9wFOajM3igYS/SfS+7mETpSVVaWA6YJEY0rOaaUXGfnwKYjxan8Nz0pI86PTeJ9CbNNl2uM16NJ4IdDUg07/rJqYnCMw9krL3e6q8//Ad2FBWQ6ABR4XuboYEyO5rJA7a4MKs1mctHs63ojBTRJi/Xga9nQSgB7K1GOW3cOpVGYmA7pSwP0PoO7XEyXrHi4fsYgjgsUHTtO5q8Pbx67tStdxX5rUDdo4fWNYcRjimop8ztc4bqW1gGftXuKMIvdF/TqDugIdje2wQl19CqUx6ZV7BRxmp7NRjkTGUyhKPOEhB6ci0SpET2w9GQ+rJBhhwUJwmGc9OFRYGWKAKgcQBOHkga0hH2f6Qoe/GGjEAvy5iKbFke8WRdk263xLb4Q3GY9++o1GRVOwrJFHh7yxrzCMDidkS9sJK1QfiatphiwWWh2Sm0G8pBtIvzfOeZ5od2QsehMAxaOd+HK6CIauskaihiXubKd4Obi0hMVFH1kpdx98cDB68xLpQCd/2AL0jcffRWQlxt301rjAtFPmOxTFzl/SVy/1azCB8N5bOOJc0k74muhYZT75VM/Y3bfeR5GqHhMMGBl4BbFwOjsNFLkN8cezILbVACnoJnHELOsktrjXs5UqfTrNyLCtnnPRqsH7gm/SvGJzIQMHw65bthTn+fMDRXWScCIUgWrVy/SDMqSGCADtFUAIULIXvFY7CPCg1gayyS/+YcElmxsmN0QmCS1q4EQML7req0ENS7NDO+wCt2I0OIv9ohFciEEuyZBiQ2BPcAYVTqEMbwyZiVUXL2MDHqsfif4K4InUkA3CSVgaDt35RD0n0Dfcq3wO4UuKUsW6PcZcaHQIuGgO0bXAsVwJtHPteZEns2x8MnQiR3k7hkC1h4En8gbBFoURwxI0ktf303BiqFENQpw40S86wOn7P0XXwARgks+pP60DPYbUSGDNS2hDNAkRjDIzRz8ecJQCNWRETRowaHHWxWVCcgb5v0ochiwVUCZq6yu4rBRWWSmHDyMwdBdJZ17jeiuyh6Ko9WUaLMetqgGWtyhJh+8AG80UuNRxOduVYwwV27z0FtaiaEFO6x6BTDwGflFkUEpMaVtdxY3zCPaA9S4Bux3xFhQUqsik0yKZecS1NUWnNR/CoFOqgbfKjh4z27djZ52I3BCeIN0Kl6DF0RVCJqN9lAEj08TyHCIHRZbB5RfhsVteIZlDOLauq42CUYqz6rueNZas+gGOYTJL4oaTYTH+y4PlheH15SoEG8rtCGHETgSi9TTAkm90tkvAvzZPpnfTOx5dQApNdMbkohO1Pc7qkFQbYLJ40SradgrWIq0dTJeikGimVoJUqwL9kcC2I0vSQRL0A5FoqjxL9uaxB1EPdlMOmEY7ZZe6AIPESD4YnEFNoqtjbitTkFrOitA2YH/6wbCj39Goep6CQFBYcqEv+VjnakDXjKVZ2kEEe5MGQ5myDlGiaJmeYVcHH9wp7Svgn43ZTqB0AENKkcW7XIA2Gbkkp0qTOn0H6Ax02xT7krep98BnXA+7bZwKPjGk/S2zNvnJ6tFNSV5bmNqqpGGOChbIM+nWLRkpZHooMCV8sRpBJqZ2CDpP4HyJyLrIq9RoBpp3qeZyorc2DdSEGZgoBK4JaTjFUCTEywTTXMc5EavMmXm2/iok7Wels5CvH/AUqFxphIhk9fZAaOodVzsU5IDzJhlZehmUr11WuIwqel2EWz6/fiyZFluXZ/djQK4OPV6abmBtMESFEtPC7IjbyYgiDTQFRB56LIJHW0pElbQHT15qtp5msQglDQw6e0ZnEakUFuyAOxfCx5igga6xxIWoaiBYyujYbC5qibO2OBNB5COIfqGNSHrOZM2Txz+bipbgQ9Goy6OQbIMhgwEXyJ6xoWzbySOc02OeDcUxkFAiOt1qamMm+ton0wwoeNMGWQf3YUNUYqx3MfJMhN4uU3nkdHsU2zEgNNMjNkY100axWPE7TCmGowHvulXikv/EWvjxkVMMuED4kjUlWuReS8LRBopBRz0AdZ77TBvseF7BoAlIUGNgZKN/I0RBct33wUmPbT5klJPTXRIb1Jg5x6HkrCGVs2YVXjIPaxq+1vBPwqTjcGb1ADnpDUKEgV8xCQh2zpXJKGG2ci8X2edQ05zpMVnm4qR9FDkCBbuA8ho7Xb7kqgFppZQUtkgMWKR+Q9R8627t7yulSSykepjhVR3ttoEL85oAGZ0+q/5ygAb1eEEajb9JP4KWLXZuClUjrfUpYJ9CkpuXt6p3AJSu3ST14sBBurGLyRRCQmjRqAaFsGtkbN2LCyQW3NKYrIGnZKDhHUQOYUlqQQzZOKESKo1aMZ5hFlgxXwCBVYEHiOid9wUT6h7NaGUxwwL6/KP0F9jbrqt1B1Wkoik8LP4yXoYB7u2TUGZ7xojR+3SR1n6BBMIRkfzZKs6enuEY+rUx+FTeAcThjKJTQREHgJsFghA1h4Lr5PqEUxLABWBCkj9yOm2w9A6ehmdhSTpYoAszS7nMHDPA5ic7wZDJAI0mLsHrQiWSNjUNUYNqArlLmduBxyVDDgoxmIxtM5DntDPOpx1C8Gs9iQqrGMyrE9iNTdu5B6qPi7DuXCCXokBm0OugeuFLNY/0IdkQ3g934KaiSATUBrNf0pl2HSN+7wmK8LZXD0bgbVffm+9VbFKPxBU9XGZk3BmvnTXEHWEAu58cv4KlzSvDJGmVoEf5G4wuK2gyB43tBPY8NIBywJy1a2e9OGwnu8qtQUubDRfNmTqsgP5CDOut7XmMxYgB7hq+2jQaPHlPU1I7FRzH8EIXueVeR9Zhp801jVOoOFlIkLCypijdyrlIVWC+VvcvReAExTV83W3+t4oW2JaNF+3AJ2H0S2uaR7eQ+jUZDyGcbzwmRjYYSqoHlVPQGgJbQYv1WEy7MI97ep5UdmMXcHpc+vCd9R0ftRwANzpdgzRl0T6SRu5EA3pbYImJdPVpM6RpglzmCqmWG6FPatNgXaLCti+HncNMBOtTnNoHK8PjXJ3gX0Ct6Ajf5wEsgOW3HHhWJAh7DkysSCf9GziTJJs/v06uYeQ4JDO3QqORjzZIZFkM63uLzqVR1MnabsctfY4Bg6PO5a2MfUe+SoY0MeiIbNvQvlTv1zG95228XLGqAbfAMDdjF05Js7VlUvcaCDMUvxbWaF+2yJ+CJq5IwrEU0ciJyUlmFTnnCWlDblcwHElSxxCBkzVzIYMP12+WuK82Gwlfs7gnMUOqvUbaTM3FogYNJD4lXD6/YSuktSpMVMq8g5k0k7BuHsYF1r1cCgZuEH+gRQd0zwu4lv0BZMIfusA68GHZPJh922l5KjZvt19isB31QO7nGmOUMqeB11PXyiQiaK6eMEBCooDecP9LHHGmIi2WKNLtInoZiazubhowXmMoIFZ1TzSRdI40iEpdGOuiPtrFA4qOVaGoz5GCe3O7hkGbhW1R71iaVNSXcDUMp7RW/WxBPvZuOZ7kyigceY5CnAjFEldTxksFKMxtCQBAEPchXzpLmVeikKYi2m5eIxqtLwIgHifLtGeVBe8Al1j2rpAX0zU3lwMD5goCJPJjkRWSAM1ctXrB5qEy6nMZHhDqS6LY6j1MHmDK9paynWD0zRsaVCkyW0RMHCVZiVVgz+0GEQLZJQ9XL+WWSmFbJGLKEh7LC/8I7hSIiu528xz6F3gFuc68zcLkDxfRIE5VrHZ1HWp9Q57k/XnQs9hRKftUbclT7V/Ap/BOEhWhtf8IvsuKh5Na9XAaToTexD+DUsLxbOCY5ScWB9vls19APnQgj/oHyJtbaBPuR7E9NNGs91QiYvE2mWuqez29rUR5IunLLZzuxYUj6CzhqgE9LaUWbyLCkUb2Sn90iMdsv3UmpjSWek5f0xXrOHGZBDeu2UjlUFLcaqENZSVzMlx93Vb2fB4Mcyaj907cKzDC/LsPT+3gUOJcIqrXww3tL+TkT37U+3M2ndTEMbSi73KzchNFjlPRpG4fee6/FuIskIlmFZBVEtxqhzvTCcKcwn6gjT6p3tx+uIZq0IsBM2np4jRu548M3z0HHuBMozSYqZFgXdl1pOQ9erlrKgulaBJ9XVKyH4l0tgsfp6got0+AJ9Ojh8MOpwoIEr3oghmZ6CxbSCGEL1dG5zWzjW7srNO2YT7OzjFbh3GIoe6aKUpfJRkz/4i1mrjnT5wzWeXRrjQoSQzg24kMqX5NPiTKfVOISTIOiOYqR4rwmv7YdqFmW53lZKYTiw3uVdFVAoJlRRt1IQYIsmjeuNk7bMbfZyJU4JttiwjeAvcPrqkDb1iA9v+PO+dFsNXxn/JUWYCCmiRWNZ01fIlgRu9zivsRpvblprtIFTthgbHZ44VZBEa6+BT6eAfkMFauyOwmygfrNVNxggHd2LjrGq7wF1ihBjNfX0ebXtE3qNBrFKjoETYCRaz1ya3eOXZ9SXAuIR63s+//1iaX4wm3qe+gP6FA+zqEcq3ApD7TFixroxIIpVskWbaXT+7SUQzJLEZy4vfbgrLtIjAELl6ZLEhZl0KKyEhAEyPFE0ztkwRmxEPz4AVlKaLALqEDYhVW0mqJb7dJHumNNo5CPv5rTw6/e3SIDOO3O0xckoYJf/KfUFkbvekXS0YvwsOU2vs1WImU0swOpRHZ0GqfmHcmSwhCsYGOMMZOrtA1VxEKHzCC4+N6RLvZkQocFxw4QAFAQv+6xR4WrEyMHKWa9tRt75JaHbmMPOC6xVSbfsvQY4tkQfGR4BWEIizyQcIqmvZ39rxwDhO2UMDaw/v1bJUrTN8nsa92GfVyu+GrjCufvbGtZnMInz8kSOu8lnSNG3V1GEHISURYMbXs5nqXa44liMpEYbTKowqCrOYWfgKXPLxJCHYEMwnC/xaLYXqVik3UBkOrBOJwcV87ENrLxLt1ZgYuMyM2khQ5l2W3exKmTnUSwQZ8JQapbOl+IMvbEt2MPj6QOtqTa9vhR4j8UKyUq8fom+2Oc3aJ7+DTr8o5S8Y/f6q41yQW6YQZQreflb6FS39hJ47yQWgbF4vPJXSxA06Rjdtubx9xJMSs4OJdANVh5eH4hg7Qjw9aBMB8btWExYd4AZUOUVcl6k53BLkRyQ6fc18btrUZXIIK3sYUPOOPFAVpXFCrrInQacIa1/tNQAYVEJOlximm9K4rcxAXSFUHuMBIz+nAo0hEJ6YoBC6hLzep7UeXI3GzoRPQIpKVXFG5gOx3MrpBK67lyFYBTbhx0PSsztnCrhBlsRr5lVWl8qz82Ngb5dA94QDi6A7dqkCIdVd7OYR9qdXQN9pFJCkvi/JQvPzAn43IdMBC333qw/clnta+XGO5Wg+O/Z1jN7HYkAbHNPZxtbA7v1xwWgxyi9s1O0YjJT278jiVkgq027ZcMA8OKlCNvBcYPacdGDTgoRYNSlQ1jspKzfNYVPtO0s2MSFjFdOVGL1OWX1qc0Az8DC0gt6Ly1GokV+w9RLlapUwgYZ3901QcMOsDSAC/nJJDgUXMh/KuNIkkfATsNxc3i8gghQn5V6pAgraUHj98FZoQgkWk0RKZWFjuLBWnhBfZ4S13XCfkNmhjHS0c3fhIoCfiMMSjsv8TJ5hs5KGAgkEVh14fIdlGZr+p4aZwnEw6aAd+2rNqljkGwBb04XDgiViBZi3gGjlJsNMaZUZrsWj2AOXhoLWu6LkKx2iXRIRQrQXaQGUjL22hszGY2EEEa2VEFRqhiYeZ5Ucy60HaeiqzQRZACPQCddpVceSo85AInPmNXgXm0g9a9EZhAOGZmAiDIa3KFySsd/UhffU6v1/pyyKsGAdQaGqeiIh9i9pwKQfb3wPaMFBTuCpjIDRm0A8Qmr6KsAyrmEpH2rX47JNBLtLAg9IeBpkQIkiV32xWzxnOR2fYU3ESULg3S37ZbRkMzp9Fm3YIqt/LwC8cgNWmcBcXdCM7iKd+VxXjYOFmW/aVEZM8jV8S5qtEI4ti9ywsfIWViKFr0YGuaCEnEd5K4NYAH4+1EkHMZn+M2ZIJOQg0dACzhUap56fZf5A+t6P7sPvjAMyKecjg9js+QnC4RK1k9ZMGfkvOZkdyRU4gYiqT+gJGpBWt8rC4M7j2PBAO+ldWRCAJD4tBVeujE3c9Nc/xaWISd+EZFbI1lZEsbVhTaJC5y2HihzY28UM+7j2ukLTBpXsO20Mo398oWaCS3Ay+ClpXWX42dcZwmVMhxIEIp/1TjDoTxY5Yv0uCSIXwqjQyWltIH+bVkoK6SAHyyuYeAuwBjyDy0NBQaBzNzyze2PXLWuZ5PA+vICFWZtQPZinJ4MkYRugjfrNS7+D0LYzaFtlUKyWqHikQ24OXluh5jtrgvX6ZtYC4Dxw6stZ8iUDAWPr0LV111czGm+PQRB1weQ3hOdQlt7b/29VgkRZ3G/2+8r114xr0Bsp7AlnO0EimLA4COqGKsIIq+Y1icKqxwZ9zEKEIikXMw/azKy3MpCEmHtTIJEESRdjnvInDD2QizgkcR3376cPP+l3e3pwMvTgyNPtIq5ZFKhOklkZvB+T7eCHey3Ve6MRk9+oH7l8UUqUnWPowAp3jpCFDiSEdLPxvnMvMaeXqgFRwzyQEOHSfNDG3pctyg9Si8oDuBGguvliI7/EFkQst0KVnbcLgb/O3tkHYg7zXGqdOTmgPBbHeFDpHEB405xkqpJjle2MlTaxbF0rYU/DzAQ6XUYoyK9/Jt00Bxgtaim8gTubQuAuPuhUbr3PDwY7x1hskEY6pPaZF/n5ioTyA2sj4PRr3IKCyrbkJn58l6RlpxbqR2mgrXOcZZpSVOJPJ2HMNu+KEZIpkQ8OCZpAkG1i1mjJ6tE7i+JBSghOrVAKZHRVv9fGEehYJsPr0G4lhnyY/nyzeeJEyDiMzgJIgQmuMzNmdgje04kcM3FZdfVhlX/SmGmkYCdiOYZdFV6KYZWrnU5pemBtc6/Lpb2EDbX1dXrf4wkQHZqk+zubzMTmu8upeXIekvcnnzUBYQNrROiC/mL8OfsvdroyIZfOWZqc75ZrmsV08yfVYQK6KkKBuRo1nyO9yFXp9O4bIz2hYszm+kUqtSuczbjHh9jPLgjqGp2fANzBuGTdVUCYPsRvh/POHFSBE8i9FZ7CoAIdmdZboGOGvl0ARig918sB9FFOfdaVEhLJiNSlVinWfja4pG82xwoZiTk35pXNH0ylrqlK6y7rbhVKXa7iP3vMCfds26iCC9AMXuggCnlIJcO+An+8A9FttyOl3DlRA8MBA6F0fl+AcmKXToZiKW04gvgB7O2gcukSQDN8rLs3rjbNOdBuBz73AoYiLGh4RMcRwFIW7HBH3IRa2lMCnixQbJiDINJpnC7ZoxcOhqfTlUebl2W+9vf7i6v6Wx/eXbBjy+vrn9EQeJ3Xswu35Cx/IIJBF+OZimKVnUvY7Jtw9NK/GzIeFecP9vRYyKqP4p31y+giEeTb48jvtc0TQgAjb8Y4kcRAWxCSvAT+sCVi1d/7Hk3qZLj3+Mug6www38RAqHMwyxfbGZGvacy7LnCuR30RHrQDbHmGSj/4ly1OCWlX5+TzP88n9hpxlf')))

# Three original Q0 construction slots: D11 H15, H19, H20.
for _i in (254, 258, 259):
 _a = _PLAN[_i]
 _commands = [_a['farmer']] + _a['hands']
 assert sum(c == ['BUILD_COOP'] for c in _commands) == 1
 for _c in _commands:
  if _c == ['BUILD_COOP']: _c[0] = 'BUILD_PASTURE'
for _a in _PLAN:
 for _c in [_a['farmer']] + _a['hands'] + _a['market']:
  if len(_c) > 1:
   if _c[1] == 'GOOSE': _c[1] = 'SHEEP'
   elif _c[1] == 'EGG': _c[1] = 'WOOL'


# D12: move the single sheep purchase from H2 to H1 so worker 1 can
# collect it at H2. Existing H2 hires retain their actual spawn positions.
_PLAN[264]['market'].append(['BUY_ANIMAL', 'SHEEP', 1])
_PLAN[265]['market'] = [([] if c[:2] == ['BUY_ANIMAL', 'SHEEP'] else c) for c in _PLAN[265]['market']]
_ROUTE = [
 ['PICKUP','SHEEP'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'],
 ['PLACE','SHEEP'], ['SOUTH'], ['EAST'], ['EAST'], ['DROP'],
 ['PICKUP','WHEAT',2], ['WEST'], ['FEED'], ['CARE'], ['WEST'],
 ['WEST'], ['FEED'], ['CARE'], ['WEST'], ['WATER'], ['SOUTH'],
 ['PLANT','WHEAT'], ['WATER']]
for _hour, _command in enumerate(_ROUTE, 2):
 _PLAN[264 + _hour - 1]['hands'][0] = _command
# Worker 6 keeps his original route and grain supply; delivery is now
# already done by worker 1. Reuse the old PLACE slot for sheep service.
_PLAN[268]['hands'][5] = ['PASS']
_PLAN[275]['hands'][5] = ['PASS']
_HARVEST_DAYS = {(4,1): {17,20,23,26,29}, (3,2): {17,20,23,26,29},
                 (2,3): {18,21,24,27,30}}

_TARGETS = {(4, 1), (3, 2), (2, 3)}
_SERVICE = {'FEED', 'CARE', 'HARVEST', 'COLLECT_FERTILIZER', 'PASS'}

class Agent:
 def __init__(self, context=None): pass
 def __call__(self, obs, cfg=None):
  day, hour = int(obs['day']), int(obs['hour'])
  i = day * 24 + hour
  if not 0 <= i < len(_PLAN):
   return {'farmer': ['PASS'], 'hands': [], 'market': []}
  action = copy.deepcopy(_PLAN[i])
  farm = obs['farms'][int(obs['player'])]
  private = obs['private']
  commands = [action['farmer']] + action['hands']
  projected = {}
  for w, (pos, cmd) in enumerate(zip([farm['farmer']] + farm['hands'], commands)):
   xy = tuple(pos)
   if xy not in _TARGETS or cmd[0] not in _SERVICE: continue
   if xy not in projected:
    projected[xy] = copy.deepcopy(farm['tiles'][pos[1]][pos[0]])
   tile = projected[xy]
   if not isinstance(tile, dict) or tile.get('animal') != 'SHEEP': continue
   inv = private['inventories'][w]
   # Keep all routes and hiring slots. Repurpose stationary goose service
   # slots for the sheep's actual state; grain demand stays one/head/day.
   op = 'PASS'
   if day + 1 in _HARVEST_DAYS[xy] and tile.get('yield_units', 0):
    op = 'HARVEST'; tile['yield_units'] = 0
   elif day < 29 and not tile['fed_today'] and inv.get('WHEAT', 0):
    op = 'FEED'; tile['fed_today'] = True
   elif day < 29 and not tile['cared_today']:
    op = 'CARE'; tile['cared_today'] = True
   elif day == 29 and tile.get('yield_units', 0):
    op = 'HARVEST'; tile['yield_units'] = 0
   elif tile.get('fertilizer_available'):
    op = 'COLLECT_FERTILIZER'; tile['fertilizer_available'] = False
   cmd[:] = [op]
  # Existing wool/egg sale windows now clear wool, including extra sheep
  # output; product PLACE EGG above becomes PLACE WOOL for D30 delivery.
  for order in action['market']:
   if len(order) > 2 and order[:2] == ['SELL', 'WOOL']: order[2] = 100
  if day == 11 and hour == 10:
   milk = private['inventories'][1].get('MILK', 0) if len(private['inventories']) > 1 else 0
   if milk: action['market'].append(['SELL', 'MILK', milk])
  return action

def create_agent(context=None): return Agent(context)
_AGENT = Agent()
def agent(observation, configuration=None):
 return _AGENT(observation, configuration)
