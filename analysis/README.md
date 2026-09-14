# analysis

- `data/` : 대표 실험 데이터 (CSV, 게인 세트별)
- `step_response.py` : 스텝응답에서 오버슈트·정착시간·정상상태오차 계산 및 그래프
- `sim_1axis.py` : 1축 동역학 모델 시뮬레이션, 실측과 비교
- `figures/` : 생성된 그래프

실행
```
pip install numpy matplotlib pandas
python step_response.py data/kp2.0_ki0.1_kd0.5.csv
```
