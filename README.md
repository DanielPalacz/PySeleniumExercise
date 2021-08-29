## PySeleniumExercise
- (Python, Pytest, Page Object Pattern)
<br/><br/>

### A. Requirements
* python 3.8 version (tested with: Python 3.8.10)
* Unix-like OS (tested with Ubuntu 20.04.2 LTS)
  
### B. Environment preparation
* clone the repository:
* - git clone https://github.com/DanielPalacz/PySeleniumExercise.git
* From the repository directory:
* - python3 -m venv local_env
* - source local_env/bin/activate
* - pip install -r requirements.txt

    
### Test execution
* From the repository directory:
* - PYTHONPATH=. pytest -s -vv --html=report.html --self-contained-html
    
### Test results
* Test result location: {Repo directory}/Results/{Timestamp directory}
* Under Test result location should appear:
* - downloded pdf ebooks
* - log.txt file
* - report.html (simpled report based on pytest-html plugin) 