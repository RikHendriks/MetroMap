import metromap as mm


name_list_xml = mm.read_xml.NameListXMLReader(r"data/name_lists.xml")

print(name_list_xml.name_lists)

city = mm.city.City('City', 100, 50)

city.add_cell(mm.city.Cell('station', (2, 3)))
city.add_cell(mm.city.Cell('station', (1, 0)))

print(city)
