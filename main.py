import metromap as mm


name_list_xml = mm.read_xml.NameListXMLReader(r"data/name_lists.xml")

city = mm.city.City.generate_city('City', 50, 25, 10)

print(city)
