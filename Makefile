setup:
	pip3 install -r requirements.txt

pipeline:
	python3 load_data.py
	python3 summary.py
	python3 stat_analysis.py
	python3 subset.py

dashboard:
	streamlit run dashboard.py