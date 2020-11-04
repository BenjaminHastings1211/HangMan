from tkinter import *
import random
W, H = 600,500
font = ('Arial',50)

words = ['apple','banana','orange','strawberry','blueberry','kiwi','grapefruit','grape','cherry','pineapple','coconut','watermelon']


class GameController():
    def __init__(self):
        self.wrongLetters = []
        self.usedLetters = []
        self.gameOver = False
        self.won = False

        self.currentWord = SecretWord(random.choice(words))
        self.traker = ScoreTracker()

    def inputLetter(self,e):
        if self.gameOver == False and self.won == False:
            self.currentWord.checkLetter(e.char)

            self.checkGameOver()

    def checkGameOver(self):
        if self.traker.timesWrong  >= 6:
            self.gameOver = True
            self.currentWord.revealWord()
            canvas.create_text(W/2,50,text='Game Over',font=('Arial',64),fill='red')
        elif self.currentWord.complete == True:
            self.won = True
            canvas.create_text(W/2,50,text='You Won!',font=('Arial',64),fill='black')


class ScoreTracker():
    def __init__(self):
        self.origin = [250,100]
        self.timesWrong = 0
        self.dead = False
        self.letterLocations = []
        self.blankSize = None

        self.bodySeg = [
            [self.origin[0]+80,self.origin[1]+25,self.origin[0]+120,self.origin[1]+65],
            [self.origin[0]+100,self.origin[1]+65,self.origin[0]+100,self.origin[1]+115],
            [self.origin[0]+100,self.origin[1]+75,self.origin[0]+80,self.origin[1]+90],
            [self.origin[0]+100,self.origin[1]+75,self.origin[0]+120,self.origin[1]+90],
            [self.origin[0]+100,self.origin[1]+115,self.origin[0]+85,self.origin[1]+135],
            [self.origin[0]+100,self.origin[1]+115,self.origin[0]+115,self.origin[1]+135]
        ]

        self.wrongLetterLabel = canvas.create_text(W/2,H-100,text='',font=('Arial',24))

        self.createFrame()

    def createFrame(self):
        canvas.create_line(self.origin[0],self.origin[1],self.origin[0],self.origin[1]+150,fill='black',width=2)
        canvas.create_line(self.origin[0],self.origin[1],self.origin[0]+100,self.origin[1],fill='black',width=2)
        canvas.create_line(self.origin[0]+100,self.origin[1],self.origin[0]+100,self.origin[1]+25,fill='black',width=2)

    def drawNext(self):

        if self.timesWrong == 0:
            canvas.create_oval(self.bodySeg[0])
        elif self.timesWrong <= 6:
            canvas.create_line(self.bodySeg[self.timesWrong])
        else:
            self.dead = True
        self.timesWrong += 1

    def drawBlanks(self):
        blanks = gameController.currentWord.spaces
        space = 50
        totalLength = blanks*(space)
        x = W/2 - totalLength/2
        spaceSize = (totalLength / blanks) * 0.8
        self.blankSize = spaceSize
        spaceBetween = (totalLength / blanks) - spaceSize
        
        for i in range(blanks):
            canvas.create_line(x,350,x+spaceSize,350,width=2)
            self.letterLocations.append(x)
            x += spaceBetween + spaceSize

    def displayLetter(self,letter,index):
        xPos = self.letterLocations[index]
        canvas.create_text(xPos+self.blankSize/2,320,text=letter,font=font)

    def drawIncorrectLeters(self):
        finalString = ''
        for i, letter in enumerate(gameController.wrongLetters):
            if i % 10 == 0:
                finalString += '\n'
            finalString += '%s '%letter

        canvas.itemconfig(self.wrongLetterLabel,text=finalString)

class SecretWord():
    def __init__(self,word):
        self.word = word
        self.spaces = len(word)
        self.complete = False
        self.display = [' ' for letter in self.word]

    def revealWord(self):
        for i, letter in enumerate(self.display):
            if letter == ' ':
                letter = self.word[i]
                gameController.traker.displayLetter(letter,i)

    def checkLetter(self,letter):
        if letter not in gameController.usedLetters and self.complete == False:
            new = [acutalLetter if letter == acutalLetter or self.display[i] != ' ' else ' ' for i,acutalLetter in enumerate(self.word)]
            if self.display == new:
                if letter not in self.display:
                    gameController.wrongLetters.append(letter)
                    gameController.traker.drawNext()
                gameController.traker.drawIncorrectLeters()
            else:
                self.display = new
                for i, letter in enumerate(self.display):
                    gameController.traker.displayLetter(letter,i)

            gameController.usedLetters.append(letter)

            if ''.join(self.display) == self.word:
                self.complete = True


root = Tk()
root.title('Hang Man')
root.resizable(0,0)
root.geometry("%sx%s"%(W,H))

canvas = Canvas(root,width=W,height=H,bd=0,highlightthickness=0,bg='white')
canvas.pack()

gameController = GameController()
gameController.traker.drawBlanks()

root.bind('<Key>',gameController.inputLetter)

root.mainloop()
