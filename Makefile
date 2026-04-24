# Reproduce every figure and table in the paper.
PY := python

.PHONY: all backtest robustness validation projection clean

all: backtest robustness validation projection

backtest:
	$(PY) src/backtest/cesi_backtest.py

robustness:
	$(PY) src/robustness/cesi_robustness_R1.py
	$(PY) src/robustness/cesi_robustness_R2.py

validation:
	$(PY) src/validation/cesi_test2_shock.py
	$(PY) src/validation/cesi_test3_leadlag.py
	$(PY) src/validation/cesi_test4_realeconomy.py
	$(PY) src/validation/cesi_R4_pressure_test.py
	$(PY) src/validation/cesi_R5_meaning_test.py

projection:
	$(PY) src/projection/cesi_R3_projection.py
	$(PY) src/projection/cesi_R3b_regime_mapping.py

clean:
	rm -rf results/figures/*.png results/figures/*.svg results/tables/* results/series/*
