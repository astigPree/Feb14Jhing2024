from kivy.properties import ListProperty, StringProperty

content = """
    Tadahhhh! my first program sa babaye na mapapangasawa ko!
    
    Ikaw ikaw lang gayud an kauna unahan na hihimoan ko sani.
    
    kinilig na naman an tanda ko hahaha.
    
    Pero seryuso SALAMAT sa pagiging adi sa akon at pag palanga sa akon.
    
    You show what love is! At pagiging usad sa dahilan san akon pag bag-o.
    
    Aram ko naiibahan ka sa mga gina panhimo ko saimo, pero gina baton mo dyapon ako.
    
    Kun nano an gina isip mo amo ina sya an gusto ko sabihon kaya salamat gayud jhing hehehe.
    
    Sana pag abot san panahon makamit naton an gusto naton sa buhay, salamat jhing and Labyu jhing 😚
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


miss_miss_lyrics ="""......
,Hinahanap ka na ng puso ko
,Baby ikaw lang talaga
,Ang nami-miss ko\nsa tuwi-tuwina
,.........
,Sa tuwi-twina
,...............
,At baby ako’y mag-aabang
,At dadalhin ka sa nakaraan
,..........
,Sa nakaraan*
"""

miss_miss_lyrics_delay = 69


list_of_images = list = ListProperty(["Pictures/flower.png" , "Pictures/images.jpeg" , "Pictures/gift box.png"])
