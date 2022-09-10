import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd

url="https://www.bollywoodhungama.com/movie-release-dates/"
response=requests.get(url)
html=bs4(response.text,"html.parser")
movies_row=html.find("tbody")
movies=movies_row.find_all("tr")
movies.pop(0)
link_list=[]
rating_list=[]
date_list=[]
name_list=[]
for i,movie in enumerate(movies):
    tds=movie.find_all("td")
    date=tds[0].text
    name=tds[1].text
    link=tds[1].a['href']
    rating=tds[2].text

    if int(rating)>70:
        name_list.append(name)
        date_list.append(date)
        link_list.append(link)
        rating_list.append(rating)
        #print(f"{name}\n{date}\n{rating}\n{link}\n\n")
movie_dictionary={'name':name_list,'date':date_list,'rating':rating_list,'link':link_list}
movies_df=pd.DataFrame(movie_dictionary)

movies_df=movies_df.sort_values(by="rating",ascending=False)
print(movies_df[['name','rating','link']].head(30))
"""
<tr><td>22 December 2023</td>
<td> <a href="https://www.bollywoodhungama.com/movie/bade-miyan-chote-miyan/">Bade Miyan Chote Miyan</a></td>
<td class="TAR"><span class="bh-poll-view-count poll--count yelrat" data-post-id="1336550">67</span></td></tr>
"""
