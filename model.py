import matplotlib
matplotlib.use('TkAgg')
import tkinter
import random
import matplotlib.pyplot
import matplotlib.animation 
import datetime
import agentframework
import csv
import requests
import bs4


#Parameters for the model
num_of_agents = 10
num_of_iterations = 100
neighbourhood = 20
agents = []

#Setup for the animation function
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

#Reads in csv file to represent the environment
f = open('in.txt', newline='') 
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
environment = []
for row in reader: 
    rowlist = []			# A list of rows
    for value in row:	
        rowlist.append(value)
    environment.append(rowlist) 		# A list of value
print(value) 				# Floats 
f.close() 	# Don't close until you are done with the reader;
        		# the data is read on request.

#Used for testing
'''matplotlib.pyplot.imshow(environment)
matplotlib.pyplot.show()#testofinputdata'''


#Timing of the model run
def getTimeMS():
    dt = datetime.datetime.now()
    return dt.microsecond + (dt.second * 1000000) + \
    (dt.minute * 1000000 * 60) + (dt.hour * 1000000 * 60 * 60)
    
#Pythag function
def distance_between(self, agent):
    return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5


#Reads in web data to initialise model
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})

#Used for testing
'''print(td_ys)
print(td_xs)'''

#Begin timing
start = getTimeMS()  

# Make the agents based on the web data and add them to the agents array.
for i in range(num_of_agents):  
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)
    agents.append(agentframework.Agent(environment, agents, y, x))


#For loop to update model for each iteration
def update(frame_number):
    # Move the agents.
    for j in range(num_of_iterations):
        random.shuffle(agents)
        for i in range (num_of_agents):
            agents[i].move()
            agents[i].eat()
            agents[i].share_with_neighbours(neighbourhood)
    #Graph agents
    matplotlib.pyplot.ylim(0, 99)
    matplotlib.pyplot.xlim(0, 99)
    matplotlib.pyplot.imshow(environment)
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)

#Animation function
def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, repeat=False, frames=num_of_iterations)
    canvas.show()
   
#Sets up the GUI window    
root = tkinter.Tk() 
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)    

#Adds menu and option to run model to GUI window
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)   

#For loop to test each agent against each other
for j in range(0, num_of_agents - 1):
    for i in range(j + 1, num_of_agents):
        test = distance_between(agents[j],agents[i])
        print(test)
 
#End timing       
end = getTimeMS()  

#Prints time taken to run
print("time = " + str(end - start))

tkinter.mainloop()