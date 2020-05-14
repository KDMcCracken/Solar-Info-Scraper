import web_scraper
import building_footprint

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

from kivy.core.window import Window
Window.size = (900, 200)


Builder.load_file("kivyApp.kv")


class BootInterfaceScreen(Screen):
    def save(self, id, text):
        App.get_running_app().config.set('BootValues', id, text)


class DisplayInfoScreen(Screen):
    """ Screen that displays all the info for the given address"""
    # All our class variables to use in the kivy.kv file
    building_area = StringProperty('')
    sunlight_per_year = StringProperty('')
    area_for_panels = StringProperty('')
    savings_with_solar = StringProperty('')
    cost_of_solar = StringProperty('')
    home_value = StringProperty('')
    home_value_with_solar = StringProperty('')

    def __init__(self, **kwargs):
        super(DisplayInfoScreen, self).__init__(**kwargs)

        self.building_area = kwargs.get("building_area")
        self.sunlight_per_year = kwargs.get("sunlight_per_year")
        self.area_for_panels = kwargs.get("area_for_panels")
        self.savings_with_solar = kwargs.get("savings_with_solar")
        self.cost_of_solar = kwargs.get("cost_of_solar")
        self.home_value = kwargs.get("home_value")
        self.home_value_with_solar = kwargs.get("home_value_with_solar")


# A Screen manager for switching between screens
screen_manager = ScreenManager()
screen_manager.add_widget(BootInterfaceScreen(name='boot_interface_screen'))


class MyApp(App):

    address = None

    def build_config(self, config):
        # Stops the config from converting all string to lowercase
        config.optionxform = str

        # Create the sections that are needed throughout runtime
        config.adddefaultsection('BootValues')
        config.setall(
            'BootValues', {
                'physical_address': ''
            }
        )

    def build(self):
        global config
        return screen_manager

    def scrape_and_display(self):
        print("Scraping Google Solar")
        google_solar_vals = web_scraper.scrape_googlesolar(self.config['BootValues']['physical_address'])

        print("Scraping Nerd Wallet")
        try:
            house_value = web_scraper.scrape_nerdwallet(self.config['BootValues']['physical_address'])
        except:
            print("\nNerdWallet does not have that address's value on record. Please try a new address\n")
            exit()

        print("Scraping Calcmaps")
        building_area = web_scraper.scrape_calcmaps(building_footprint.run(self.config['BootValues']['physical_address'],
                                                          self.config['BootValues']['state']))
        
        # Remove the '$' from the house value and replace the ',' with ''
        house_value = house_value[1:]
        house_value = house_value.replace(',', '')

        # Get new value of home based on 4.1% increase national average and format as currency
        home_value_with_solar = int(house_value) * 1.041
        home_value_with_solar = "${:,.2f}".format(home_value_with_solar)

        # Reformat house value as currency
        house_value = "${:,.2f}".format(int(house_value))

        # Switch our screen to 'infoScreen' with a check for prior existence
        if screen_manager.current != 'infoScreen':
            if screen_manager.has_screen('infoScreen'):
                screen_manager.current = 'infoScreen'

            screen_manager.add_widget(DisplayInfoScreen(name='infoScreen', **google_solar_vals,
                                                        home_value=house_value,
                                                        home_value_with_solar=home_value_with_solar,
                                                        building_area=building_area))
            screen_manager.current = 'infoScreen'


if __name__ == '__main__':
    try:
        MyApp().run()
    except:
        print("\nClosing chrome webdriver\n")
        web_scraper.driver.quit()
