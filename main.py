import metromap as mm


city = mm.city.City.generate_city('City', 50, 50, 25)

city.plot_city(r"output/city_output.svg")
