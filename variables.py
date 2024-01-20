from kivy.properties import ListProperty, StringProperty

content = """
    Aram mo jhing hinimo ko ini para sabihon tanan na gusto ko sabihon.
    """

maximum_height = 0.8

list_of_heights : list[float, ...] = ListProperty([
		( maximum_height - 0.1 , 0.5, ) , 
		( maximum_height - 0.15 , 0.05), 
		( maximum_height - 0.1 , 0.05, ) , 
		( maximum_height - 0.15 , 0.05), 
		( maximum_height - 0.1 , 0.05, ) , 
		( maximum_height - 0.05 , 0.05), 
		( maximum_height - 0.1 , 0.05, ) , 
		( maximum_height - 0.03 , 0.05), 
		( maximum_height - 0.1 , 0.05, ) , 
		( maximum_height - 0.03 , 0.05), 
		( maximum_height - 0.0 , 0.05, ) , 
	])


miss_miss_lyrics ="""
Hinahanap ka na ng puso ko
Baby ikaw lang talaga
Ang nami-miss ko sa tuwi-tuwina
Sa tuwi-twina
At baby ako’y mag-aabang
At dadalhin ka sa nakaraan
Sa nakaraan
"""


list_of_images = list = ListProperty(["Pictures/flower.png" , "Pictures/images.jpeg" , "Pictures/gift box.png"])
