##Imports
from math import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  ##Allows Embedding with Tkinter
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
from tkinter import *
from tkinter import ttk
from functools import partial

##
print(np.asin(0.2))
##
bgcolour = "grey"
sg = "blue"
Window = Tk()
Window.geometry("1250x1000")
GraphShowing = "Y,X"
Window.config(bg = "blue")
BackGround = Frame(Window,width = 1000,height = 1000,bg = bgcolour)
#SelectGround = Frame(Window,width = 125,height = 1000,bg = sg)#The frame buttons for choosing challenge is
BackGround.pack()
#SelectGround.pack(side = LEFT)
Buttons = []
Switch = []
Simulations = []
Selection = []
List = []
Challenge = []
Sim = []
ScaleButtons = []
##Might Make Own Legend Where all Variables Are Displayed to save space
#apogee - Highest Point
#make a way to export as png
#Instantiate Rest of Values for each challenge in a method
def func(z):
    y = 0.5**2*log(abs(sqrt(1+z**2)+z))+0.5*z*sqrt(1+z**2)
    return y
def InvertedParabolicArcCalculation(U,θ,g,R): ## Challenge 6 ## Almost Finished Come Bsck
  ##Calculate limits
  θ = θ * pi/180
  a = (U**2)/(g*(1+(tan(θ))**2))
  b = tan(θ)
  c = tan(θ) - g*R*(1+(tan(θ))**2)/(U**2)
  s = a * (func(b) - func(c))
  #x = linspace(0,R,N)
  #t = x/U*cos(θ)
  
  return s
#h = 2
#U = 30
#θrad = 50*(180/pi)
#g = 9.8
#R = (U**2/g)*(sin(θrad)*cos(θrad) + cos(θrad)*sqrt(sin(θrad)**2+((2*g*h)/(U**2))))
#print(R)
#x = 0
#Total = 0
#while x <=  9.86:#R:
#Total += InvertedParabolicArcCalculation(U,θrad,g,90.517,R)
#x += 0.1
#print(Total)
class MainMenu():
    def __init__(self,Challenge):
        self.Challenge = Challenge
        self.Open = True
        self.Title = Label(BackGround,text = "PROJECTILE MOTION \n APP", font = ("Elephant Pro",25),
              bg = "grey",fg = "yellow")
        #Img = ImageTk.PhotoImage(Image.open("Cannon.PNG"))
        self.Cover = Label(BackGround,text = "Hope You Enjoyed Watching\n",bg = "grey",fg = "grey",font = 20)
                           #bg = "grey",fg = "yellow")
        self.Cover.place(x = 250, y = 600)
        self.Title.place(x = 350,y= 300)
        self.SimButtons = SimulationSelect(600,500)
        self.SimButtons.Generate(Challenge)
    def clicked(self):
        if self.Open == True:
            self.Title.destroy()
            self.Cover.destroy()
            for i,it in enumerate(self.SimButtons.B):
                it.destroy()
            self.SimButtons = SimulationSelect(1125,0)
            self.SimButtons.Generate(self.Challenge)
            self.Open = False
class Switch_Preset():
  def __init__(self,List,Options,ChallengeAsociated):
    self.List = List
    self.Options = Options
    x,y = 600,300
    self.B = Menubutton(BackGround, width = 25, height = 2,bg = "Orange",text = "Presets")
    self.B.place(x = x, y = y)
    self.M = Menu(self.B, tearoff = False)
    self.Challenge = ChallengeAsociated
    self.LoadOptions()
  def LoadOptions(self):
    menu = self.M
    Options = self.Options    
    for i,it in enumerate(self.List):
      if Options[i][12] == self.Challenge:
        self.M.add_command(label = it, command = partial(self.GeneratePreset,i))
    self.B.config(menu=menu)
    return
  def GeneratePreset(self,i):
    Options = self.Options
    Graph(Options[i][0], Options[i][1],
                         Options[i][2],Options[i][3],
                         Options[i][4],Options[i][5],
                         Options[i][6],Options[i][7],
                         Options[i][8],Options[i][9],
                         Options[i][10],Options[i][11],
                         Options[i][12]).CommandButtons(0)
  
class SwitchGraph():
  def __init__(self,Types,Obj,ChallengeAsociated):
    self.Types = Types
    x,y = 800,300
    self.B = Menubutton(BackGround, width = 25, height = 2,bg = "Red",text = "Graphs")
    self.B.place(x = x, y = y)
    self.M = Menu(self.B, tearoff = False)
    self.Obj = Obj
    self.LoadOptions()
  def LoadOptions(self):
    #print(self.Types)
    menu = self.M
    for i,it in enumerate(self.Types):
      self.M.add_command(label = it, command = partial(self.GenerateGraph,it))
    self.B.config(menu=menu)
  def GenerateGraph(self,it):
    global GraphShowing
    GraphShowing = it
    #print("Grap", GraphShowing)
    Obj = self.Obj
    Graph(Obj.U,Obj.h,Obj.θ,Obj.g,Obj.x,Obj.y,
          Obj.e,Obj.N,Obj.M,Obj.Cd,Obj.AD,Obj.A,
          Obj.name).CommandButtons(0)
class SaveButton():
  def __init__(self,SavePlot,name,Anim):
    self.plot = SavePlot
    self.name = name
    self.Anim = Anim
    B = Button(BackGround,width = 25,height = 2,command = partial(self.Save),bg = "Lime Green",text = "Save")
    B.place(x = 250,y = 600)
  def Save(self):
    print(self.Anim)
    if self.name != "Bounce":
      self.plot.savefig(self.name+".png")
    else:
      self.Anim.SaveAnimation()      
class ScaleB():

  def __init__(self, MinValue, MaxValue, CurrentValue, X, Y,ChallengeAssociated,ValueChange): #Add Resolution as variable
    Buttons.append(self)
    self.DistanceX = X + 150
    self.DistanceY = Y
    #print(CurrentValue)
    self.OriginalInput = CurrentValue
    self.MinValue = MinValue
    self.MaxValue = MaxValue
    if ValueChange == "U":
        self.unit = "ms⁻¹"
        self.Var = "Launch Speed"
    if ValueChange == "h":
        self.unit = "m"
        self.Var = "Height"
    if ValueChange == "θ":
        self.unit = "°"
        self.Var = "Launch Angle"
    if ValueChange == "g":
        self.unit = "ms⁻²"
        self.Var = "Gravity"
    if ValueChange == "x":
        self.unit = "m"
        self.Var = "Horizontal Position"
    if ValueChange == "y":
        self.unit = "m"
        self.Var = "Vertical Position"
    if ValueChange == "e":
        self.unit = ""
        self.Var = "Coefficient of Restition"
    if ValueChange == "N":
        self.unit = ""
        self.Var = "Number Of Bounces"
    if ValueChange == "M":
        self.unit = "Kg"
        self.Var = "Mass"
    if ValueChange == "Cd":
        self.unit = ""
        self.Var = "Coefficient of Drag"
    if ValueChange == "A":
        self.unit = "m²"
        self.Var = "Cross-Sectional Area"
    if ValueChange == "AD":
        self.unit = "Kgm⁻³"
        self.Var = "Air Density"
    self.Value = ValueChange
    text = self.Value + "/" + self.Var + ": " + self.unit  + "\n" + "min = " + str(self.MinValue) + " max = " + str(self.MaxValue) + "\n" + "Current Value = " + str(CurrentValue)
    self.Variable = Label(BackGround,text = text,bg = "grey",font = ("Arial",6))
    self.Delta = Scale(BackGround,from_=0,to=MaxValue,orient="horizontal",command=partial(self.SliderChanged),bg = bgcolour,resolution = 0.01)
    self.Input = Entry(BackGround)
    self.n = 0
    self.buttonschanged = 0
    #self.Input.insert(int(CurrentValue), int(CurrentValue))
    #self.Delta.set(CurrentValue)
    if self.Input.get() != self.OriginalInput:
      self.OriginalInput = self.Input.get()
      partial(self.EntryChanged)
    self.Delta.place(x=X, y=Y,width = 105)
    self.Input.place(x=X,y=Y+40,width=105)
    self.Variable.place(x=X,y=Y-40,width = 105)
    #self.Input.insert(0, "0")
    #self.Delta.set(CurrentValue)
    self.Input.bind("<Return>", partial(self.EntryChanged))
    self.ChallengeAssociated = ChallengeAssociated
    self.Delta.set(CurrentValue)
  def SliderChanged(self, U):
    Variables = [it.Value for i,it in enumerate(Buttons)]
    self.buttonschanged += 1
    for i,it in enumerate(Challenge):
        if it.name == self.ChallengeAssociated:
            plt.close()
            #print(it.U)
            for x,xt in enumerate(Variables):
                #print(xt)
                if self.Value == xt:
                    setattr(it,xt,Buttons[x].Delta.get())
            #print(xt,Variables[-1])
            #if self.buttonschanged == len(Buttons):
            it = Graph(it.U,it.h,it.θ,it.g,it.x,it.y,it.e,it.N,it.M,it.Cd,it.AD,it.A,self.ChallengeAssociated)
            self.Input.delete(0, END)
            self.Input.insert(int(self.Delta.get()), int(self.Delta.get()))
            text = self.Value + "/" + self.Var + ": " + self.unit  + "\n" + "min = " + str(self.MinValue) + " max = " + str(self.MaxValue) + "\n" + "Current Value = " + str(self.Delta.get())
            self.Variable.config(text = text)
            it.Command("")
  def EntryChanged(self, x):
    Variables = [it.Value for i,it in enumerate(Buttons)]
    if self.Input.get() != self.OriginalInput and len(self.Input.get()) != 0:
        for i,it in enumerate(Challenge):
            if it.name == self.ChallengeAssociated:
              self.OriginalInput = self.Input.get()
              plt.close()
              self.Delta.set(self.Input.get())
              text = self.Value + "/" + self.Var + ": " + self.unit  + "\n" + "min = " + str(self.MinValue) + " max = " + str(self.MaxValue) + "\n" + "Current Value = " + str(self.Input.get())
              self.Variable.config(text = text)

    it = Graph(it.U,it.h,it.θ,it.g,it.x,it.y,it.e,it.N,it.M,it.Cd,it.AD,it.A,self.ChallengeAssociated)
    it.Command("")

class Graph():

  def __init__(self, U, h, θ,g,x,y,e,N,M,Cd,AD,A,name):
    self.g, self.U, self.h, self.θ = float(g), float(U), float(h), float(θ) ##Change g back to 10 later
    self.M,self.Cd,self.AD,self.A = M,Cd,AD,A
    self.x,self.y = float(x),float(y)
    self.dt, self.t = 0.001, 0
    self.dX = 0.02
    self.Xa,self.Ya = 0,0
    ListOfChangingValues = [self.U,self.h,self.θ,self.x,self.y]
    self.θrad = self.θ * (pi / 180)
    self.X, self.Y = [], []
    self.height, self.width = 550, 600
    Simulations.append(self)
    self.name = name
    self.a = 0
    self.e = e
    self.N = N
    self.Command = ""
    self.Save = ""
    self.ButtonBelowGraph = 150
    if self.name != "":
        self.Command = getattr(self,self.name)
        self.CommandButtons = getattr(self,self.name+"Buttons")
  def ProjectileMotionButtons(self,z):
    global Buttons,Switch
    for i,it in enumerate(Buttons):
        it.Delta.destroy()
        it.Input.destroy()
        it.Variable.destroy()
    for i,it in enumerate(Switch):
      it.B.destroy()
      it.M.destroy()
    plt.close()
    MMenu.clicked()
    Buttons = []
    Switch = []
    Switch += [Switch_Preset(PresetNames,Preset,self.name)]
    U = ScaleB(0.00, 100.00,self.U, 100, Challenge[0].height + self.ButtonBelowGraph,"ProjectileMotion","U")
    h = ScaleB(0.00, 200.00,self.h, U.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"ProjectileMotion","h")
    θ = ScaleB(0.00, 90.00,self.θ, h.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"ProjectileMotion","θ")
    g = ScaleB(0.00, 100.00,self.g, θ.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"ProjectileMotion","g")
    setattr(Save,"name",self.name)
    self.ProjectileMotion(0)
  def ProjectileTrajectoryButtons(self,z): ##Challenge 2
    global Buttons,Switch
    for i,it in enumerate(Buttons):
        it.Delta.destroy()
        it.Input.destroy()
        it.Variable.destroy()
    for i,it in enumerate(Switch):
      it.B.destroy()
      it.M.destroy()
    MMenu.clicked()
    Switch = []
    plt.close()
    Buttons = [] ##Max Horizontal Range
    self.dX = 0.02
    Switch += [Switch_Preset(PresetNames,Preset,self.name)]
    U = ScaleB(1.00, 300.00,self.U,100, Challenge[0].height + self.ButtonBelowGraph,"ProjectileTrajectory","U")
    h = ScaleB(0.00, 200.00,self.h, U.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"ProjectileTrajectory","h")
    θ = ScaleB(0.00, 90.00,self.θ, h.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"ProjectileTrajectory","θ")
    g = ScaleB(0.00, 100.00,self.g, θ.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"ProjectileMotion","g")
    #R = ScaleButtons.append(ScaleB(0.00,100.00,Challenge[0].width,250,"ProjectileTrajectory"))
    setattr(Save,"name",self.name)
    self.ProjectileTrajectory(0)
  def ProjectileToHitTargetButtons(self,z):
      global Buttons,Switch
      for i,it in enumerate(Buttons):
        it.Delta.destroy()
        it.Input.destroy()
        it.Variable.destroy()
      for i,it in enumerate(Switch):
        it.B.destroy()
        it.M.destroy()
      MMenu.clicked()
      Switch = []
      plt.close()
      Buttons = []
      Switch += [Switch_Preset(PresetNames,Preset,self.name)]
      U = ScaleB(0.00, 300.00,self.U,100, Challenge[0].height + self.ButtonBelowGraph,"ProjectileToHitTarget","U")
      h = ScaleB(0.00, 200.00,self.h, U.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"ProjectileToHitTarget","h")
      X = ScaleB(0.00, 1000.00,self.x, h.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"ProjectileToHitTarget","x")
      Y = ScaleB(0.00, 1000.00,self.y, X.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"ProjectileToHitTarget","y")
      setattr(Save,"name",self.name)
      self.ProjectileToHitTarget(0)
    #min U >= sqrt(g)*sqrt(Y+sqrt(X**2+Y**2)) U min when =: X and Y are coords of Point
  def ProjectileMaxRangeButtons(self,z):
    global Buttons,Switch
    for i,it in enumerate(Buttons):
        it.Delta.destroy()
        it.Input.destroy()
        it.Variable.destroy()
    for i,it in enumerate(Switch):
      it.B.destroy()
      it.M.destroy()
    MMenu.clicked()
    Switch = []
    plt.close()
    Buttons = []
    Switch += [Switch_Preset(PresetNames,Preset,self.name)]
    U = ScaleB(1.00, 100.00,self.U, 100, Challenge[0].height + self.ButtonBelowGraph,"ProjectileMaxRange","U")
    h = ScaleB(0.00, 200.00,self.h, U.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"ProjectileMaxRange","h")
    θ = ScaleB(0.00, 90.00,self.θ, h.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"ProjectileMaxRange","θ")
    setattr(Save,"name",self.name)
    self.ProjectileMaxRange(0)
  def TrajectoryandBoundingButtons(self,z):
    global Buttons,Switch
    for i,it in enumerate(Buttons):
        it.Delta.destroy()
        it.Input.destroy()
        it.Variable.destroy()
    for i,it in enumerate(Switch):
      it.B.destroy()
      it.M.destroy()
    MMenu.clicked()
    Switch = []
    plt.close()
    Buttons = []
    Switch += [Switch_Preset(PresetNames,Preset,self.name)]
    U = ScaleB(1.00, 300.00,self.U, 100, Challenge[0].height + self.ButtonBelowGraph,"TrajectoryandBounding","U")
    h = ScaleB(0.00, 200.00,self.h, U.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"TrajectoryandBounding","h")
    X = ScaleB(0.00, 1000.00,self.x, h.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"TrajectoryandBounding","x")
    Y = ScaleB(0.00, 1000.00,self.y, X.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"TrajectoryandBounding","y")
    setattr(Save,"name",self.name)
    self.TrajectoryandBounding(0)
  def ProjectilesButtons(self,z):
    global Buttons,Switch
    #self.g = 10 ## Change later
    for i,it in enumerate(Buttons):
        it.Delta.destroy()
        it.Input.destroy()
        it.Variable.destroy()
    for i,it in enumerate(Switch):
      it.B.destroy()
      it.M.destroy()
    MMenu.clicked()
    Switch = []
    plt.close()
    Buttons = []
    Switch += [Switch_Preset(PresetNames,Preset,self.name)]
    U = ScaleB(1.00, 300.00,self.U, 100, Challenge[0].height + self.ButtonBelowGraph,"Projectiles","U")
    setattr(Save,"name",self.name)
    self.Projectiles(0)
  def BounceButtons(self,z):
    global Buttons,Switch
    for i,it in enumerate(Buttons):
        it.Delta.destroy()
        it.Input.destroy()
        it.Variable.destroy()
    for i,it in enumerate(Switch):
      it.B.destroy()
      it.M.destroy()
    MMenu.clicked()
    Switch = []
    plt.close()
    Buttons = []
    Switch += [Switch_Preset(PresetNames,Preset,self.name)]
    U = ScaleB(1.00, 300.00,self.U, 100, Challenge[0].height + self.ButtonBelowGraph,"Bounce","U")
    h = ScaleB(0.00, 200.00,self.h, U.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"Bounce","h")
    θ = ScaleB(0.00, 90.00,self.θ, h.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"Bounce","θ")
    N = ScaleB(0.00, 100,self.N, θ.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"Bounce","N")
    e = ScaleB(0.00, 1.00,self.e, N.DistanceX,Challenge[0].height + self.ButtonBelowGraph,"Bounce","e")
    ##Create Buttons for e and N
    #e = 0.7
    #N = 6
    setattr(Save,"name",self.name)
    self.Bounce(0)
  def AirResistanceButtons(self,z):
    global Buttons,Switch,GraphShowing
    for i,it in enumerate(Buttons):
        it.Delta.destroy()
        it.Input.destroy()
        it.Variable.destroy()
    for i,it in enumerate(Switch):
      it.B.destroy()
      it.M.destroy()
    MMenu.clicked()
    Switch = []
    plt.close()
    Buttons = []
    GraphTypes = ["Y,X","Y,T","UX,T","UY,T","U,T"]
    Switch += [Switch_Preset(PresetNames,Preset,self.name)]
    Switch += [SwitchGraph(GraphTypes,self,self.name)]
    U = ScaleB(1.00, 300.00,self.U, 0, Challenge[0].height + self.ButtonBelowGraph,"AirResistance","U")
    h = ScaleB(0.00, 200.00,self.h, U.DistanceX, Challenge[0].height + self.ButtonBelowGraph ,"AirResistance","h")
    θ = ScaleB(0.00, 90.00,self.θ, h.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"AirResistance","θ")
    M = ScaleB(0.00, 100.00,self.M, θ.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"AirResistance","M")
    Cd = ScaleB(0.00, 4.00,self.Cd, M.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"AirResistance","Cd")
    AD = ScaleB(0.00, 100.00,self.AD, Cd.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"AirResistance","AD")
    A = ScaleB(0.00, 1.00,self.A, AD.DistanceX, Challenge[0].height + self.ButtonBelowGraph,"AirResistance","A")
    print(GraphShowing)
    setattr(Save,"name",self.name)
    self.AirResistance(0)
  def LaunchButtons(self,z):
    global Buttons,Switch
    for i,it in enumerate(Buttons):
        it.Delta.destroy()
        it.Input.destroy()
        it.Variable.destroy()
    for i,it in enumerate(Switch):
      it.B.destroy()
      it.M.destroy()
    MMenu.clicked()
    Save = MMenu.Save
    Switch = []
    plt.close()
    Buttons = []
    Switch += [Switch_Preset(PresetNames,Preset,self.name)]
    U = ScaleB(1.00, 100000.00,self.U, 100, Challenge[0].height + 125,"Launch","U")
    h = ScaleB(0.00, 200.00,self.h, U.DistanceX, Challenge[0].height + 125 ,"Launch","h")
    θ = ScaleB(0.00, 90.00,self.θ, h.DistanceX, Challenge[0].height + 125,"Launch","θ")
    self.Launch(0)
    ##Add Presets of Planets and ability to change Mass and rotational speed
  def ProjectileMotion(self,z): ##Challenge 1
    #print("hi")
    #print(self.U,self.h)
    Last = False
    U,Ux,Uy = self.U,self.U*cos(self.θrad),self.U*sin(self.θrad)
    self.T,self.UX,self.UY,self.Ulist = [],[],[],[]
    while (self.h + (self.U * sin(self.θrad) * self.t) - (1 / 2 * self.g * self.t**2)) >= 0 or Last == True:  ##Equation for vertical if below zero want to end graph
      #print(self.θrad)
      if self.θ == 90:
        self.X.append(0)
      else:
        self.X.append(self.U * cos(self.θrad) * self.t)
      self.Y.append(self.h + (self.U * sin(self.θrad) * self.t) - (1 / 2 * self.g * self.t**2))
      self.t += self.dt
      if self.name == "AirResistance":
        self.T.append(self.t)
        Ux = self.U*cos(self.θrad)
        Uy = Uy - self.g*self.dt
        U = sqrt(Ux**2+Uy**2)
        self.UX.append(Ux)
        self.UY.append(Uy)
        self.Ulist.append(U)
      if (self.h + (self.U * sin(self.θrad) * self.t) - (1 / 2 * self.g * self.t**2)) < 0:
        if Last == True:
            Last = False
        else:
            Last = True
    #print(self.X)
    #print("Hi")
    if self.name != "AirResistance":
      self.plot()
  def ProjectileTrajectory(self,z): ##Challenge 2
    x = 0
    print(self.dX)
    #print(self.name)
    if self.name == "ProjectileTrajectory" or "TrajectoryandBounding":
      #print("hI")
      R = (self.U**2/self.g)*(sin(self.θrad)*cos(self.θrad) + cos(self.θrad)*sqrt(sin(self.θrad)**2+((2*self.g*self.h)/(self.U**2))))
    if self.name == "ProjectileToHitTarget":
      #print("loo")
      R = self.x
    if self.name == "ProjectileMaxRange":
      #print("boo")
      #print("Hi")
      self.a = (2*self.g*self.h)/(self.U**2)
      R = ((self.U**2)/(self.g)*sqrt(1+(self.a)))
    while x <= R:
        #Ya = (self.h+((self.U**2)/(2*self.g))*sin(self.θrad)**2) Y apogee
        self.Y.append(self.h + x*tan(self.θrad) - (self.g/(2*(self.U**2))) * (1 + tan(self.θrad)**2)*x**2)
        self.X.append(x)
        x += self.dX
    #InvertedParabolicArcCalculation(self.U,self.θ,self.g,x,R)
    #Apogee
    self.Ya = self.h+((self.U**2)/(2*self.g))*sin(self.θrad)**2
    self.Xa = (self.U**2/self.g)*(sin(self.θrad)*cos(self.θrad))
    self.t = x/(self.U*cos(self.θrad))
    #print(Ya,Xa)
    #self.dt = (self.Xa,self.Ya) ## for plotting purposes
    if self.Command == getattr(self,"ProjectileTrajectory"):
        self.plot()
        #print(self.name)
    return R
    #print(self.X,self.Y)
  def ProjectileToHitTarget(self,z): ##Challenge 3
      #print(self.U,self.h,self.x,self.y)
      self.Umin = sqrt(self.g)*sqrt((self.y-self.h)+sqrt(self.x**2+(self.y-self.h)**2))
      print(self.Umin)
      if self.x != 0:
        self.θmin = atan(((self.y-self.h)+sqrt(self.x**2+(self.y-self.h)**2))/self.x) * (180/pi)
      else:
        self.θmin = 0
      a,b,c = ((self.g)/(2*(self.U**2)))*self.x**2,-self.x,self.y-self.h+((self.g*self.x**2)/(2*(self.U**2)))
      self.discriminant = -1
      #if b**2 - 4*a*c >= 0 and a > 0:
      self.discriminant = b**2 - 4*a*c
      #print("d: ", self.discriminant, "a: ",a, "b: ",b, "c: ",c)
      self.θmaxP = atan((-b+sqrt(self.discriminant))/(2*a))*(180/pi)
      self.θmaxM = atan((-b-sqrt(self.discriminant))/(2*a))*(180/pi)
      #print(self.Umin,self.θmin,self.θmaxP,self.θmaxM,self.h)
      if self.Command == getattr(self,"ProjectileToHitTarget"):
        self.plotProjectileToHitTarget(z)
  def ProjectileMaxRange(self,z): ##Challenge 4
    self.a = (2*self.g*self.h)/(self.U**2)
    self.θmax = asin((1/sqrt(2+self.a))) * (180/pi)
    d = (self.U**2/self.g)
    self.tmax = d*sqrt(2+self.a)
    self.Rmax = Graph(self.U,self.h,self.θmax,self.g,self.x,self.y,self.e,self.N,self.M,self.Cd,self.AD,self.A,"ProjectileMaxRange")
    RMAX = self.Rmax.ProjectileTrajectory(0)
    if self.name == "ProjectileMaxRange":
      R = Graph(self.U,self.h,self.θ,self.g,self.x,self.y,self.e,self.N,self.M,self.Cd,self.AD,self.A,"ProjectileTrajectory")
      r = R.ProjectileTrajectory(0)
      fig = plt.figure()
      s = InvertedParabolicArcCalculation(self.U,self.θ,self.g,r)
      smax = InvertedParabolicArcCalculation(self.U,self.θmax,self.g,RMAX)
      Canvas = FigureCanvasTkAgg(fig, master=BackGround)
      Canvas.get_tk_widget().place(x=0,y=50,height=self.height,width=self.width)
      f = "{n:.2f}"
      plt.ylabel("y/m")
      plt.xlabel("x/m")
      plt.title("ProjectileMaxRange" + "\nU = " + str(self.U) + " U^2/g = " + f.format(n = d) + " S = " + f.format(n = s) + " Smax = " + f.format(n = smax))
      plt.plot(R.X,R.Y,"--")
      plt.plot(self.Rmax.X,self.Rmax.Y,"o-")
      plt.ylim(bottom = 0)
      plt.xlim(xmin = 0)
      plt.grid(True)
      setattr(Save,"plot",fig)
  def TrajectoryandBounding(self,z): ##Challenge 5
    MinHighLow = Graph(self.U,self.h,self.θ,self.g,self.x,self.y,self.e,self.N,self.M,self.Cd,self.AD,self.A,"TrajectoryandBounding")
    MinHighLow.ProjectileToHitTarget(0)
    MaxRange = Graph(self.U,self.h,self.θ,self.g,self.x,self.y,self.e,self.N,self.M,self.Cd,self.AD,self.A,"TrajectoryandBounding")
    Bounding = Graph(self.U,self.h,self.θ,self.g,self.x,self.y,self.e,self.N,self.M,self.Cd,self.AD,self.A,"TrajectoryandBounding")
    Bounding.Bounding(0)
    fig = plt.figure()
    Canvas = FigureCanvasTkAgg(fig, master=BackGround)
    Canvas.get_tk_widget().place(x=0,y=50,height=self.height,width=self.width)
    MaxRange.ProjectileMaxRange(0)
    plt.plot(MaxRange.Rmax.X,MaxRange.Rmax.Y,"-")
    plt.plot(Bounding.X,Bounding.Y,"--")
    MinHighLow.plotProjectileToHitTarget(0)
    setattr(Save,"plot",fig)
  def Projectiles(self,z): ##Challenge 7
    dt = 0.1
    fig = plt.figure()
    Canvas = Canvas = FigureCanvasTkAgg(fig, master=BackGround)
    Canvas.get_tk_widget().place(x=0,y=50,height=self.height,width=self.width)
    #θrad = 85*(pi/180)
    θ = [85,78,70.5,60,45,30]
    θrad = [it*pi/180 for i,it in enumerate(θ)]
    dX = [self.U*it for i,it in enumerate(θ)]
    for i,it in enumerate(θrad):
      t = 0
      r,T = [],[]
      self.X,self.Y = [],[]
      #print(it)
      if it > 70.5*(pi/180):
        a = ((3*self.U)/(2*self.g))*sin(it)
        b = sqrt((9*self.U**2)/(4*self.g**2)*sin(it)**2 - (2*self.U**2)/ (self.g**2))
        Tmin = a+b
        Tmax = a-b
        #tmin = ((3*self.U)/(2*self.g))*(sin(it) - sqrt(sin(it)**2-8/9))
        #tmax = ((3*self.U)/(2*self.g))*(sin(it) + sqrt(sin(it)**2-8/9))
        #print(Tmin,Tmax)
        plt.plot(Tmin,sqrt((self.U**2*Tmin**2)-(self.g*Tmin**3*self.U*sin(it)) + (0.25*self.g**2*Tmin**4)),"X",markersize = 5,color = "red")
        plt.plot(Tmax,sqrt((self.U**2*Tmax**2)-(self.g*Tmax**3*self.U*sin(it)) + (0.25*self.g**2*Tmax**4)),"X",markersize = 5,color = "green")
        #Xmin,Xmax = self.U * cos(it) * tmin, self.U * cos(it) * tmax
        #Ymin,Ymax = self.U* sin(it) - 0.5*self.g*tmin**2, self.U * sin(it) - 0.5*self.g*tmax**2
        #print(Xmin,Xmax,Ymin,Ymax)
        #plt.plot(Xmin,Ymin, "X", markersize = 5,color = "red")
        #plt.plot(Xmax,Ymax,"X", markersize = 5,color = "green")
      if θ[i] == 70.5:
        Tminmax = (self.U/self.g) * sqrt(2)
        #print(Tminmax)
        #Xminmax = self.U * cos(it) * Tminmax
        #Yminmax = self.U * sin(it) - 0.5 * self.g*Tminmax**2
        #print(Xminmax,Yminmax)
        #plt.plot(Xminmax,Yminmax, "X", markersize = 5)
        plt.plot(Tminmax,sqrt((self.U**2*Tminmax**2)-(self.g*Tminmax**3*self.U*sin(it)) + (0.25*self.g**2*Tminmax**4)),"X",markersize = 5)
      while t <= 1.25*Tmin:
        r.append(sqrt((self.U**2*t**2)-(self.g*t**3*self.U*sin(it)) + (0.25*self.g**2*t**4)))
        T.append(t)
        self.X.append(self.U * cos(it) * t)
        self.Y.append(self.U * sin(it) * t - 0.5*self.g*t**2)
        #plt.plot(self.X,self.Y)
        t += dt
      #print(self.X,self.Y)
      #T,r
      plt.plot(T,r)
      setattr(Save,"plot",fig)
    plt.ylim(bottom = 0)
    plt.xlim(xmin = 0)
  def Bounce(self,z): ##Challenge 8
    Ux = self.U*cos(self.θrad)
    Uy = self.U*sin(self.θrad)
    n = 0
    self.X,self.Y = [],[]
    Ax,Ay = 0,-self.g
    y = self.h
    x = 0
    t = 0
    dt = 0.01
    self.z = 0
    #print(self.h)
    tsince = 0
    while n <= self.N:
      x = x + (Ux*dt + 0.5*(Ax)*(dt**2))
      y = y + (Uy*dt + 0.5*(Ay)*(dt**2))
      self.Y.append(y)
      self.X.append(x)
      Ux = Ux + 0.5*(2*Ax)*dt
      Uy = Uy + 0.5*(2*Ay)*dt
      if y < 0:
        y = 0
        n += 1
        Uy = -self.e*Uy
        U = sqrt(Uy**2+Ux**2)
      t += dt
    self.Ya = self.h+((self.U**2)/(2*self.g))*sin(self.θrad)**2 + 1
    fig = plt.figure()
    Canvas = FigureCanvasTkAgg(fig, master=BackGround)
    Canvas.get_tk_widget().place(x=0,y=50,height=self.height,width=self.width)
    Anim = AnimateGraph(self.X,self.Y,1.1*self.X[-1],1.1*self.Ya)
    Anim.CreateAnimation()
    #Anim.SaveAnimation()
    setattr(Save,"plot",fig)
    #setattr(Save,"Anim",Anim)
    #Save.Anim = Anim
    #Canvas = Canvas = FigureCanvasTkAgg(fig, master=BackGround)
    #Canvas.get_tk_widget().place(x=0,y=50,height=self.height,width=self.width)
  def AirResistance(self,z): ##Challenge 9
    #Cd = 1
    #A = 0.007854
    #AD = 1
    #M = 0.1
    K = (1/2*self.Cd*self.AD*self.A)/self.M
    #print(K)
    Ux,Uy = self.U*cos(self.θrad),self.U*sin(self.θrad)
    #print(Ux)
    x,y = 0,self.h
    t,dt = 0,0.01
    #X: Max = -(Vx/V)*M*K*V**2
    #Y: May = -Mg - Vy/V*M*K*V**2
    U = self.U
    Ax = -Ux*K*U
    Ay = -self.g-((Uy/U)*K*U**2)
    T,UX,UY,Ulist = [t],[Ux],[Uy],[self.U]
    self.Y,self.X = [self.h],[0]
    Count = 1
    NoAirRes = Graph(self.U,self.h,self.θ,self.g,self.x,self.y,self.e,self.N,self.M,self.Cd,self.AD,self.A,"AirResistance")
    NoAirRes.ProjectileMotion(0)
    while y > 0 or (GraphShowing != "Y,X" and t < NoAirRes.t):
      x = x + (Ux*dt + 0.5*(Ax)*(dt**2))
      y = y + (Uy*dt + 0.5*(Ay)*(dt**2))
      self.Y.append(y)
      self.X.append(x)
      Ux = Ux + Ax*dt
      UX.append(Ux)
      Uy = Uy + Ay*dt
      UY.append(Uy)
      U = sqrt((Ux**2)+(Uy**2))
      Ulist.append(U)
      Ax = -(Ux/U)*K*U**2
      Ay = -self.g-((Uy/U)*K*U**2)
      t += dt
      T.append(t)
    #for i,it in enumerate(T):
      #print(it,UX[i])
    fig = plt.figure()
    #print(GraphShowing)
    ###TRY TO MAKE MORE EFFICIENT
    ##Graph Y against X
    if GraphShowing == "Y,X":
      plt.plot(self.X,self.Y,label = "Air Resistance")
      plt.plot(NoAirRes.X,NoAirRes.Y,label = "No Air Resistance")
      plt.xlabel("x/m")
      plt.ylabel("y/m")
    ##Graph Y against T
    if GraphShowing == "Y,T":
      plt.plot(T,self.Y,label = "Air Resistance")
      plt.plot(NoAirRes.T,NoAirRes.Y,label = "No Air Resistance")
      plt.xlabel("t/s")
      plt.ylabel("y/m")
    ##Graph UX against T
    if GraphShowing == "UX,T":
      plt.plot(T,UX,label = "Air Resistance")
      plt.plot(NoAirRes.T,NoAirRes.UX,label = "No Air Resistance")
      plt.xlabel("t/s")
      plt.ylabel("Vx/ms^-1")
    ##Graph UY against T
    if GraphShowing == "UY,T":
      plt.plot(T,UY,label = "Air Resistance")
      plt.plot(NoAirRes.T,NoAirRes.UY,label = "No Air Resistance")
      plt.xlabel("t/s")
      plt.ylabel("Vy/ms^-1")
    ##Graph U against T
    if GraphShowing == "U,T":
      plt.plot(T,Ulist,label = "Air Resistance")
      plt.plot(NoAirRes.T,NoAirRes.Ulist,label = "No Air Resistance")
    plt.grid(True)
    ##Create Radio Button For these
##    LargeY = 0
##    for i,it in enumerate(NoAirRes.Y):
##        if it > LargeY:
##            LargeY = it
##    ax = plt.gca()
##    ax.set_xlim([0, NoAirRes.X[-1]*1.15])
##    ax.set_ylim([0, LargeY*1.15])
    if GraphShowing != "UY,T":
        plt.ylim(bottom = 0)
        plt.xlim(xmin = 0)
    plt.legend("upper right")
    #plt.title(self.name + ": " self.U = 
    Canvas = FigureCanvasTkAgg(fig, master=BackGround)
    Canvas.get_tk_widget().place(x=0,y=50,height=self.height,width=self.width)
    setattr(Save,"plot",fig)
  def Launch(self,z):
    G = 6.67*10**-11
    ##Radius and Mass of Earth(Testing)
    r = 6.37*10**6
    rplot = r/(1*10**6)
    M = 5.97*10**24
    ##Height
    self.X,self.Y,Z = [],[],[]
    y = 0
    #print(y)
    Ux,Uy = self.U*cos(self.θrad),self.U*sin(self.θrad)
    print(Ux,Uy)
    dt = 0.01
    Ax = 0
    x = 0
    z = 0
    zplot = z/(1*10**6)
    fig = plt.figure()
    ##Use Pyvista for visual instead of matplotlib
    ax = fig.add_subplot(projection = "3d")
    u, v = np.mgrid[0:rplot:50j, 0:rplot:50j]
    #print(u,v)
    Px = rplot*np.cos(u)*np.sin(v)
    Py = rplot*np.sin(u)*np.sin(v)
    Pz = rplot*np.cos(v)
    R = r + (sqrt(x**2 + y**2 + z**2))
    #Rx = r + x
    while sqrt(x**2 + y**2 + z**2) >= 0: #and sqrt(y**2+x**2+z**2) >= 0:
      ##Radius + Height
      R = r + (sqrt(x**2 + y**2 + z**2))
      #Rx = r + x
      #print(Rx)
      g = -(G*M)/(R**2)
      y = y + (Uy*dt + 0.5*g*dt**2)
      yplot = y/(1*10**6)
      #if y <= 0:
      #Ax = -(G*M)/(Rx**2)
      x = x + (Ux*dt + 0.5*Ax*dt**2)
      xplot = x/(1*10**6)
      #z = z + (Ux*dt + 0.5*Ax*dt**2)
      Uy,Ux = Uy + g*dt,Ux + Ax*dt
      self.Y.append(rplot+yplot)
      self.X.append(xplot)
      Z.append(zplot)
      #print(g)
    #print(self.X,self.Y,Z)
    plt.plot(self.X,self.Y,Z)
    ax.plot_wireframe(Px, Py, Pz, color="b")
    plt.ylabel("y/m*10**6")
    plt.xlabel("x/m*10**6")
    #plt.zlabel("z/m*10**6")
    Canvas = FigureCanvasTkAgg(fig, master=BackGround)
    Canvas.get_tk_widget().place(x=0,y=50,height=self.height,width=self.width)
  def Bounding(self,z):
  #R = (self.U**2/self.g)*(sin(self.θrad)*cos(self.θrad) + cos(self.θrad)*sqrt(sin(self.θrad)**2+((2*self.g*self.h)/(self.U**2))))
    x = 0
    while self.h+(self.U**2)/(2*self.g)-((self.g)/(2*self.U**2))*x**2 >= 0:
      self.X.append(x)
      self.Y.append(self.h+(self.U**2)/(2*self.g)-((self.g)/(2*self.U**2))*x**2)
      x += self.dX
  def plotProjectileToHitTarget(self,z):
    f = "{n:.2f}"
    if self.name == "ProjectileToHitTarget":
      fig = plt.figure()
      Canvas = FigureCanvasTkAgg(fig, master=BackGround)
      Canvas.get_tk_widget().place(x=0,y=50,height=self.height,width=self.width)
      plt.ylabel("y/m")
      plt.xlabel("x/m")
      #plt.title("Projectile to hit X,Y\n"self.Umin)
      setattr(Save,"plot",fig)
      #print(Graph(self.Umin, self.h, self.θradmin,self.x,self.y,"").ProjectileTrajectory[0])
    MinSpeed = Graph(self.Umin, self.h, self.θmin,self.g,self.x,self.y,self.e,self.N,self.M,self.Cd,self.AD,self.A,self.name)
    MinSpeed.ProjectileTrajectory(0)
    plt.plot(MinSpeed.X,MinSpeed.Y,"--",label = "MinSpeed: U = " + f.format(n = self.Umin) +
             "\n                  θ = " + f.format(n = self.θmin))
    plt.title(self.name+"\nV = " + str(self.U) + " H = " + str(self.h) + " θ = " + str(self.θ) + " g = " + str(self.g))
    #print(self.discriminant)
    if True:
      HighBall = Graph(self.U,self.h,self.θmaxP,self.g,self.x,self.y,self.e,self.N,self.M,self.Cd,self.AD,self.A,self.name) #θmaxP
      HighBall.ProjectileTrajectory(0)
      plt.plot(HighBall.X,HighBall.Y,"--",label = "HighBall: U = " + f.format(n = self.U) +
               "\n               θ = " + f.format(n = self.θmaxP))
      LowBall = Graph(self.U,self.h,self.θmaxM,self.g,self.x,self.y,self.e,self.N,self.M,self.Cd,self.AD,self.A,self.name) #θmaxM
      LowBall.ProjectileTrajectory(0)
      plt.plot(LowBall.X,LowBall.Y,"--",label = "LowBall: U = " + f.format(n = self.U) +
               "\n              θ = " + f.format(n = self.θmaxM))
    plt.legend(loc = "upper right")
    plt.plot(self.x,self.y,"X",markersize = 10)
    plt.ylim(bottom = 0)
    plt.xlim(xmin = 0)
    plt.grid(True)
    if self.name == "ProjectileToHitTarget":
      setattr(Save,"plot",fig)
    #plt.show()
    ## fix H
  def plot(self):
    fig = plt.figure()
    Canvas = FigureCanvasTkAgg(fig, master=BackGround)
    Canvas.get_tk_widget().place(x=0,y=50,height=self.height,width=self.width)
    plt.ylabel("y/m")
    plt.xlabel("x/m")
    t = "{n:.2f}"
    plt.title(self.name+"\nV = " + str(self.U) + " H = " + str(self.h) + " θ = " + str(self.θ) + " t = " + t.format(n = self.t)+"\nΔt = " + str(self.dt) + " g = " + str(self.g))
    #plt.Artist.set_label()
    plt.grid(True)
    plt.plot(self.X, self.Y, "o-",markersize = 5)
    if self.Xa and self.Ya > 0:
        plt.plot(self.Xa,self.Ya, "X", markersize = 20)
    plt.ylim(bottom = 0)
    plt.xlim(xmin = 0)
    #fig.savefig(self.name+".png")
    setattr(Save,"plot",fig)
  def ClosePlot(self):
    for i,it in enumerate(fig):
        it.close()
class SimulationSelect():
    def __init__(self,X,Y):
        self.X = X
        self.Y = Y
        self.B = []
        Selection.append(self)
    def Generate(self,Graph):
        for i,it in enumerate(Graph):
            self.B.append(Button(Window,command = partial(it.CommandButtons,0),text = it.name,width = 17,height = 1))
            self.B[-1].place(x = self.X,y = self.Y)
            self.Y += 20
class AnimateGraph:
  def __init__(self,X,Y,R,Ya):
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(X,Y)
        self.ax.set(xlim = (0,R),ylim = (0,Ya))
        self.X,self.Y = X,Y
        Canvas = FigureCanvasTkAgg(self.fig, master=BackGround)
        Canvas.get_tk_widget().place(x=0,y=50,height=550,width=600)
  def animate(self,i):
        self.line.set_xdata(self.X[:i])
        self.line.set_ydata(self.Y[:i])
        return self.line,
  def CreateAnimation(self):
        self.anim = FuncAnimation(self.fig, self.animate, frames=len(self.Y) + 1, interval=1,blit = True)
        Tk.mainloop(BackGround)
        vid = animation.FFMpegWriter(fps=60)
        self.anim.save("Bounce.mp4",writer = vid)
        plt.close()
  def SaveAnimation(self):

      plt.close()

Challenge.append(Graph(10, 5, 30,9.81,1,0,0,0,0,0,0,0,"ProjectileMotion"))
Challenge.append(Graph(10, 5, 30,9.81,1,0,0,0,0,0,0,0,"ProjectileTrajectory"))
Challenge.append(Graph(75, 0, 45,9.81,100.00,100.00,0,0,0,0,0,0,"ProjectileToHitTarget"))
Challenge.append(Graph(50,15,22,9.81,0,0,0,0,0,0,0,0,"ProjectileMaxRange"))
Challenge.append(Graph(80,200,45,9.81,500,70,0,0,0,0,0,0,"TrajectoryandBounding"))
Challenge.append(Graph(10,0,0,9.81,0,0,0,0,0,0,0,0,"Projectiles"))
Challenge.append(Graph(10,5,45,9.81,0,0,0.7,3,0,0,0,0,"Bounce"))
Challenge.append(Graph(20,0,30,9.81,0,0,0,0,0.01,0.3,1,0.50,"AirResistance"))

#Challenge1.ProjectileMotionCalculation()
Preset = [[20,2,45,9.81,1,0,0,0,0,0,0,0,"ProjectileMotion"],
          [10, 5, 30,9.81,1,0,0,0,0,0,0,0,"ProjectileMotion"],
          [10,5,30,3.71,1,0,0,0,0,0,0,0,"ProjectileMotion"],
          [10,5,30,8.87,1,0,0,0,0,0,0,0,"ProjectileMotion"],
          [10,5,30,1.63,1,0,0,0,0,0,0,0,"ProjectileMotion"],
          [5,150,30,9.81,1,0,0,0,0,0,0,0,"ProjectileMotion"],
          [10,1,42,9.81,0,0,0,0,0,0,0,0,"ProjectileTrajectory"],
          [10,5,30,9.81,100.00,100.00,0,0,0,0,0,0,"ProjectileTrajectory"],
          [10,5,30,3.71,100.00,100.00,0,0,0,0,0,0,"ProjectileTrajectory"],
          [10,5,30,8.87,100.00,100.00,0,0,0,0,0,0,"ProjectileTrajectory"],
          [10,5,30,1.63,100.00,100.00,0,0,0,0,0,0,"ProjectileTrajectory"],
          [150,0,0,9.81,1000,300,0,0,0,0,0,0,"ProjectileToHitTarget"],
          [10,2,60,9.81,0,0,0,0,0,0,0,0,"ProjectileMaxRange"],
          [150.22,0,0,9.81,1000,300,0,0,0,0,0,0,"TrajectoryandBounding"],
          [20,2,30,9.81,0,0,0,0,0.1,1.0,1,0.007854,"AirResistance"],
          [20,2,30,9.81,0,0,0,0,0.1,0.47,1,0.007854,"AirResistance"],
          [20,2,30,9.81,0,0,0,0,0.1,0.42,1,0.007854,"AirResistance"],
          [20,2,30,9.81,0,0,0,0,0.1,0.50,1,0.007854,"AirResistance"],
          [20,2,30,9.81,0,0,0,0,0.1,1.05,1,0.007854,"AirResistance"],
          [20,2,30,9.81,0,0,0,0,0.1,0.80,1,0.007854,"AirResistance"],
          [20,2,30,9.81,0,0,0,0,0.1,0.82,1,0.007854,"AirResistance"],
          [20,2,30,9.81,0,0,0,0,0.1,1.15,1,0.007854,"AirResistance"],
          [20,2,30,9.81,0,0,0,0,0.1,0.04,1,0.007854,"AirResistance"],
          [20,2,30,9.81,0,0,0,0,0.1,0.09,1,0.007854,"AirResistance"]]
PresetNames = [["BPHO INPUTS"],["Projectiles On Earth"],
               ["Projectiles On Mars"],["Projectiles On Venus"],
               ["Projectiles On Moon"],["Throwing an object from a Building"],
               ["BPHO INPUTS"],["Projectiles On Earth PT"],
               ["Projectiles On Mars PT"],["Projectiles On Venus PT"],
               ["Projectiles On Moon PT"],
               ["BPHO INPUTS"],["BPHO INPUTS"],
               ["BPHO INPUTS"],["BPHO INPUTS"],
               ["Sphere"], ["Half Sphere"],
               ["Cone"],["Cube"],
               ["Angled Cube"],["Long Cylinder"],
               ["Short Cylinder"],["Streamlined Body"],
               ["Streamlined Half-Body"]]

#Challenge1.plot()
Save = SaveButton("","","")
MMenu = MainMenu(Challenge)


#U = ScaleB(0.00, 100.00, Challenge[0].width, 250,"ProjectileMotion")
#h = ScaleB(0.00, 200.00, U.DistanceX, 250,"ProjectileMotion")
#θ = ScaleB(0.00, 90.00, h.DistanceX, 250,"ProjectileMotion")
#Graph2 = Challenge1(30,10,10)
#Graph2.Calculation()
#Graph2.plot()
#InvertedParabolicArcCalculation(10,45,9.81,4.41,12.03)
mainloop()

