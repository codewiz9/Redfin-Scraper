from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
def get_data(zip):
    #all the diffrent data I want to get
    price = []
    adress = []
    beds = []
    baths = []
    sqr_feet = []
    brokrege_number = []
    image = []
    lot_size = []
    #number of houses I want to get data for i am not using this now but this feature can be implmented later 
    houses_to_scrape = 5
    #get the correct url
    main_url = 'https://www.redfin.com/zipcode/{}'.format(zip)
    #creat the soup
    page = requests.get(main_url)
    soup = bs4(page.text, 'html.parser')
    #address
    for i in soup.findAll('div', class_='link-and-anchor'):
        adrs = i.getText()
        adress.append(adrs)
    #price
    for i in soup.findAll('span', class_ = 'homecardV2Price'):
        if len(adress) > len(price):
            price.append('No price found')
        p = i.getText()
        price.append(p)
    #beds/baths/squar feet/ acers
    for i in soup.findAll('div', class_ = 'stats'):
        x = i.getText()
        if 'beds' in x:
            beds.append(x)
        elif 'baths' in x:
            baths.append(x)
        elif 'sq ft' in x and '(lot)' not in x:
            sqr_feet.append(x)
        elif '(lot)' in x:
            x.replace("(lot)", "")
            lot_size.append(x)
    #phone number
    for i in soup.findAll('div', class_ = 'disclaimerV2'):
        p = i.getText()
        brokrege_number.append(p)
    #image
    #for i in soup.findAll('img',class_='homecard-image'):
        #print(i)
        #url = str(i['src'])
        #image.append(url)
    make_excell(price, adress, beds, baths, sqr_feet, brokrege_number, lot_size, zip)
#bellow is the function for makeing data into xecell
def make_excell(price, adress, beds, baths, sqr_feet, brokrege_number, lot_size, zip):
    data = {'prices': price, 'address': adress, 'beds': beds, 'baths': baths, 'sqr_feet': sqr_feet, 'brokrege_number': brokrege_number, 'lot_size': lot_size}
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.transpose()
    df.to_excel("house_for_sale_at_the_zip_{}.xlsx".format(zip))
#main function
def main():
    zip = input("What zip code would you like to use: ")
    if len(zip) == 5:
        print('your data was collected')
        return get_data(zip)
    else:
        zip = input("Plz enter a real zip: ")
        return get_data(zip)
main()