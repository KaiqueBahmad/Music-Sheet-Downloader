from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import requests
import shutil
import os


class Finder():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        #service = Service(executable_path=Path(__file__).parent / 'chromedriver.exe')
        service = Service(executable_path=Path(os.getcwd()+r'\\chromedriver.exe'))

        self.browser = webdriver.Chrome(
            service=service,
            options=options
        )

        self.path = os.getcwd()+r'\\Sheets'
        if not os.path.isdir(self.path):
            os.mkdir(self.path)


    def choice_free_sheet(self, html):
        section = BeautifulSoup(html,'html.parser')


        for num, sheet in enumerate(section.find_all(class_='mrNlf')):
            if len(sheet) == 1:
                return num+1
            elif len(sheet) == 2 and not 'https://musescore.com/pro/landing/official-scores?feature=badge' in str(sheet):
                return num+1


    def get_sheet(self, music, folder_name= None):
        self.browser.get(f'https://musescore.com/sheetmusic?text={music}'.replace(' ','%20'))
        sheets_section = self.browser.find_element(
            By.XPATH,
            '/html/body/div[1]/div/section/section/main/div[2]/section'
        )
        choice = self.choice_free_sheet(sheets_section.get_attribute('innerHTML'))
        choice = self.browser.find_element(
            By.XPATH,
            f'/html/body/div[1]/div/section/section/main/div[2]/section/article[{choice}]/div[1]/div[2]/a'
        )
        choice.click()
        pages_section = self.browser.find_element(
            By.XPATH,
            '/html/body/div[1]/div/section/main/div/div[3]/div/div'
        )

        num_pages = self.browser.find_element(
            By.XPATH,
            '/html/body/div[1]/div/section/aside/div[5]/div[2]/table/tbody/tr[1]/td/div'
        )
        num_pages = int(num_pages.text)
        print(f'Size: {num_pages} Pages.')

        if folder_name is None:
            folder_name = music

        self.folder_path = self.path+fr'\\{folder_name}'
        os.mkdir(self.folder_path)


        for page in range(1, num_pages+1):
            path = f'/html/body/div[1]/div/section/main/div/div[3]/div/div/div[{page}]'
            page_field = self.browser.find_element(
                By.XPATH,
                path
            )
            page_field.click()
            sleep(2)
            url = self.browser.find_element(
                By.XPATH,
                path+'/img'
            )
            url = url.get_attribute('src')
            self.save(url, f'Page [{page}]-{music}')
            print(f'({page}/{num_pages}) Complete')
        print('Complete')

    def save(self, url, name):
        img = requests.get(url)
        if '.svg' in url:
            extension = '.svg'
        elif '.png' in url:
            extension = '.png'
        archive_name = name+extension
        with open(archive_name,'wb') as file:
            file.write(img.content)

        shutil.move(os.path.dirname(self.path)+fr'\\{archive_name}', self.folder_path+fr'\\{archive_name}')


if __name__ == '__main__':
    bot = Finder()
    bot.get_sheet('Moonlight Sonata') #<-- Example of use
    #
    #Use the class to create an object, and them, use this method 'get_sheet()', 1 argument is required, other is
    #optional, Required is the name of the song you wanna search, and the optional is which name you want for the
    #folder, if None is given then name will be the same than song.
