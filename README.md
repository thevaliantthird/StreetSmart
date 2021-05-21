# StreetSmart
This repository contains Team VASU's Project for ITSP 2021 at IIT-Bombay.

Note: The Model will be designed only to cater with Population Dense Places like Indian Cities,
and would definitely give extraneous results if run on less populated regions.


The model structure on the front-end to re-iterate upon is:

1) Give me the image of an underdeveloped city
2) You may also give me in addition to that the position of certin plans about that, eg. where is a factory, business complex or School planned to be, along with its area of course
3) Then using these two, we will be judging whether or not, we should compute values describing the traffic, the given building would contribute to
4) The ML part would end here, and then we'd be using various Flow Algorithms, to get to a model.

5) Then, we'll judge how good our developed city is using a cost-function, and thus by a reinforced learning type approach, we will improve the transport network of our city.

The Planning Process will also allow you to choose from certain categories for the planned buildings, these being:

1) NOTA
2) BusinessAndMarketingComplexes
3) Residential
4) Offices
5) PowerPlants_Factories_ConstructionSites
6) Healthcare
7) Educational
8) GodownsAndStorage
9) Transport
10) HotelsAndLeisure


The Syntax which is to be used while running the whole thing: (Ubuntu): python labelImg.py [IMAGE DIRECTORY] [LABELS FILE(CLASSES.TXT]

The classes.txt file is uploaded in the repo here, download it and have it on your PC!

Also, Remember pressing on SAVE after labelling and make sure AND labelImg has a bug i.e. When you run the program and set the Output as YOLO, it should output as a .txt
file but for some reason it doesn't!

But there's an easy way to fix it, just click on that YOLO icon a few times, it'll cycle from YOLO->VOC/PASCAL->....->YOLO, and after that you'll be good to go, you'll click on Python 
and it would store your file as a .txt file(make sure to store it in the same directory as your pictures)! 

General Guidelines while labelling:

1) Try to get equal labels for all the given categories, as that's something we'll need!
2) Even NOTA should have equal number of images as the other categories!
3) MAKE SURE THAT YOU'VE MADE FOLDERS, IN THE IMAGES DIRECTORY(WHERE YOU ARE DOING YOUR THING), These folders should be named 0,1,2.....9 (denoting the classes)!



Its preferred to spend the first day's time, taking all the screenshots and the rest of the 9 days categorizing them properly!

Don't forget to put these all in all folder!
And when you take the screenshots, do them with a certain numbering 
1.png
2.png
3.png
etc.

Certain Screenshot apps like 'Screenshot' on Ubuntu have this feature to change them, better use that!


Dealing with parsed Roads (Utkarsh's Part):

1) You'll be getting a matrix(as a 2D Numpy Array) with same dimension as that of the Image itself.
2) Majority of the entries in this part will be zero. The non-zero entries will denote the traffic assoiated with the roads that are identified around that pixel.
3) The first task would be to convert the roads to be boundaries as for all we care, that's all that matters.
4) These roads as well as the Image Boundary would together compartmentalize the map into various parts
5) Your next task would be to create a new class which has as its attributes, an image and the nearest boundary (Basically take all boundaries which are within a given threshold,
and only take the first such boundary(s) and store them in the class)


Parsing Images to get the roads :
1) Figure out the 4-dimensional vector corresponding to all of our well known colors and tablate your range
2) Move through the Image and mark all such points on a second 2D Matrix
3) Figure out the Proper Algorithm to judge if a particular section of pixels together demarcate a road 
4) Running DFS/BFS and removing the vague sections which aren't exactly roads, but just some random points on the map which happen to have the same color which Google Maps 
reserves for Roads
5) Getting the road data into a different Data Abstraction 

