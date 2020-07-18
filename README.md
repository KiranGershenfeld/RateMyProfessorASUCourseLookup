# RMPASU  
Visit https://rmp-asu.herokuapp.com/ (May take a second to load)  
Paste a link directly from the ASU Course Search website and the website will display RateMyProfessor information for each teacher listed on the linked url. Please give the page a few seconds to load the data, it can take like 15-20 seconds depending on the number of professors it needs to check.

This app is written in python, the web implementation uses Flask, and the site is hosted through Heroku.

# How It Works
The main python script uses BeautifulSoup to parse the html of the linked ASU Course Search page and compile a list of teachers. Unfortunately, RateMyProfessor teacher pages use an internal ID and not the name of the teacher, so the script first has to find that ID from a JSON search query page. Once it has the ID, it finds the teachers actual RMP page and parses the html to find their scores. That data is then packaged up in a JSON dictionary and served back through Flask to the javascript running on the webpage. After some light data processing, it is displayed onto the page. This process does take a decent amount of time (python requests just arent that fast) so searching a page with a lot of professors will take some time. 

# Improvements and Updates
I am actively maintaining this project and would love to see it improve. If you have any suggestions or want to help out please message me or send a pull request give it a shot. If you want to expand this to work with a different university it will probably take some doing but that would be really amazing. 
