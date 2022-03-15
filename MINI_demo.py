from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from nltk.corpus import wordnet as wn
import clueGenerator as clueGen
import warnings

warnings.filterwarnings("ignore")

#Used for splitting a string to newlines in each 64 characters.
#Used to prevent any text overlaps.
def insertNewLines(string, every=64):
    return '-\n   '.join(string[i:i+every] for i in range(0, len(string), every))

#Open the chrome
driver = webdriver.Chrome()

#Open the site
driver.get("https://www.nytimes.com/crosswords/game/mini")


#popup close button element
#waited until the button becomes clickable because if the program extracts the button to early, it doesn't work.
popupOK = WebDriverWait(driver, 120).until(
EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button/div")))

popupOK.click()

#Reveal menu button element
revealPuzzleMenu = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button')
revealPuzzleMenu.click()

#Reveal button element
reveal = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a')
reveal.click()

#Confirm revealing element
confirm = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/article/div[2]/button[2]')
confirm.click()

#Close window element
closeWindow = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/span')
closeWindow.click()


#Gets all of the clues with their clue number and clue text. (Across and down)
clues = driver.find_elements_by_class_name('Clue-li--1JoPu')

#Creating two empty lists to store the clues.
across = list()
down = list()

#previous is used to compare with the previous clue number.
#If the previous clue number is bigger, it means we are in the down clues now.
#This is necessary to discriminate across and down clues.
prev = -1

cur = across
#Adding the clues to the across and down lists to use in GUI.
for i in clues:

	#clueLine[0] is the clue number and clueLine[1] is the clue text.
	clueLine = i.text.split('\n')

	#If the previous clue number is bigger, across clues are exhausted and we start to add into down clues.
	if(int(clueLine[0]) <= prev):
		cur = down
	#After the check, making the current clue number previous for the next iteration.
	prev = int(clueLine[0])
	#Adding the clue to the current list
	cur.append([clueLine[0], clueLine[1]])

for i in across:
	print(i)
for i in down:
	print(i)

print('==========================================')

#Getting the whole puzzle area
puzzle = driver.find_element_by_css_selector("g[data-group='cells']")
#Getting the tiles(or blocks) from the game area.
tiles = puzzle.find_elements_by_xpath("*")

#A 2D array to store the entries(answers).
entries = list()

#An array to store a row of the puzzle entries temporarily.
entryRow = list()

columnCounter = 0
counter = 1 # We couldn't extract the clue numbers. Therefore we use a counter to generate the numbers manually.
for i in tiles:

	#To seperate rows 5 by 5 when in the end of a row, current entryRow is appended to entries and a new row is generated.
	if(columnCounter == 5):
		columnCounter = 0
		entries.append(entryRow)
		entryRow = list()

	#Getting all the information such as the letter and clue location
	tile = i.find_elements_by_xpath("*")

	#Tile has only letter
	if(len(tile) == 3):
		entryRow.append(i.find_element_by_class_name('Cell-hidden--3xQI1').get_attribute("innerHTML"))
	#Tile has number and letter
	elif(len(tile) == 4):
		entryRow.append(i.find_elements_by_class_name('Cell-hidden--3xQI1')[1].get_attribute("innerHTML") + str(counter))
		counter += 1
	#Black tile (empty tile)
	else:
		entryRow.append('#')
	columnCounter += 1
entries.append(entryRow)

#For debugging purposes (To see the result in terminal)
#print(entries)

#Close the browser
driver.close()

acrossCounter = 0
downCounter = 0

for row in range(5):
	for col in range(5):
		if len(entries[row][col]) == 2:
			#maybeacross
			ns = ''
			if col - 1 < 0 or entries[row][col - 1] == '#':
				for curc in range(col, 5):
					if entries[row][curc][0] == '#':
						break
					ns += entries[row][curc][0]
				across[acrossCounter].append(ns)
				acrossCounter += 1
			#maybedown
			ns = ''
			if row - 1 < 0 or entries[row - 1][col] == '#':
				for curc in range(row, 5):
					if entries[curc][col][0] == '#':
						break
					ns += entries[curc][col][0]
				down[downCounter].append(ns)
				downCounter += 1

all = across + down
# print('========')
# print(all)
# print('========')

clue_log = {#cluelardan birisi fillblanck tarzıysa 1 olucak,çok fazla olmamalı, eski clue logunu tutmak
  "fill_blank": 0,
  "antonym": 0,
  "synonym": 0
}
for riddle in all:
	riddle.append(clueGen.createNewClue(riddle[1], riddle[2], clue_log))

# print(across)
# print(down)



# Creating the empty frame
master = Tk()
master.lift()
master.attributes("-topmost", True)
master.title('MINI - Project Demo 1')
#A suitable size for our GUI
master.geometry("1200x450")
#MAX height and width that we can resize without breaking anything.
canvas_width = 1920
canvas_height = 1080
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()


#img = PhotoImage(file="logo.png")
#w.create_image(400,20, anchor = NW, image=img)

#Grids offset from the side and above
offset = 40
leftOffset = 40
boxSize = 60
#Letters' offset from the sides and above
wordOffset = 16
#Iterating once for each tile
for i in range(5):
	for j in range(5):
		#If tile is empty, create a black rectangle.
		if entries[i][j] == '#':
			w.create_rectangle(leftOffset + boxSize * j, offset + boxSize * i, leftOffset + boxSize * (j + 1),
				offset + boxSize * (i + 1), fill="black")
		else:
			#Creating a white rectangle
			w.create_rectangle(leftOffset + boxSize * j, offset + boxSize * i, leftOffset + boxSize * (j + 1),
				offset + boxSize * (i + 1), fill="white")

			#Printing the tile letter 
			text = Label(master, text= entries[i][j][0], font=("Helvetica", 18, 'bold'))
			text.place(x = leftOffset + boxSize * j + wordOffset + 5, y= offset + boxSize * i + wordOffset )
			text.config(background="white")

			#If the tile should have a clue location, also print it 
			if len(entries[i][j]) == 2: 	
				text1 = Label(master, text=entries[i][j][1], font=("Helvetica", 7))
				text1.place(x = leftOffset + boxSize * j + 5, y= offset + boxSize * i + 5 )
				text1.config(background="white")
			

#Label for group name and date. Date is formatted
groupLabel = Label(master, text="MINI" + " "+ datetime.now().strftime("%d/%m/%Y %H:%M:%S"), font=("Helvetica", 12))
master.update()
groupLabel.place(x = leftOffset + boxSize * 5 - groupLabel.winfo_reqwidth(), y = offset + boxSize * 5 + 5)

#Across title
acrossLabel = Label(master, text="Across", font=("Helvetica", 25))
acrossLabel.place(x = 400, y = offset)

#Down title
downLabel = Label(master, text="Down", font=("Helvetica", 25))
downLabel.place(x = 800, y = offset)

#Creating one single string for all the clues by adding them togeter.
#This makes managing the labels simpler becuase we will have only one label for the clues.
acrosses = ''
for i in across:
	acrosses += insertNewLines(i[0] + ' ' + i[1] + '\n')
	acrosses += insertNewLines('   ' + i[3] + '\n\n')
	
clueLabel = Label(master, text=acrosses, font=("Helvetica", 10), justify=LEFT)
clueLabel.place(x = 400, y = offset + 60)

downs = ''
for i in down:
	downs += insertNewLines(i[0] + ' ' + i[1] + '\n')
	downs += insertNewLines('   ' + i[3] + '\n\n')

clueLabel = Label(master, text=downs, font=("Helvetica", 10), justify=LEFT)
clueLabel.place(x = 800, y = offset + 60)

#Start the GUI
mainloop()