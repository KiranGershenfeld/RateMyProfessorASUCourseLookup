# RMPASU  
Visit https://rmp-asu.herokuapp.com/
Paste a link directly from the ASU Course Search website and the website will display RateMyProfessor information for each teacher listed on the linked url.

This app is written in python, the web implementation uses Flask, and the site is hosted through Heroku.

# How It Works
The python script uses the BeautifulSoup module to parse through the HTML of the linked ASU Course Search page. After pulling each teacher name listed, that name is then queried to RateMyProfessor using a behind the scenes JSON page. If a matching teacher is found, the script pulls that teacher ID from the JSON and uses that id to find their actual public facing RateMyProfessor page. Then the html is parsed to find the numeric rating values which are packaged up in JSON and sent back to the webpage. The webpage uses JavaScript to do some light processing and then displays the data.

# Improvements and Updates
I am actively maintaining this project and would love to see it improve. If you have any suggestions or want to help out please message me or send a pull request give it a go! If you want to expand this to work with a different university it will probably take some doing but that would be really amazing. 
