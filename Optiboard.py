import pygame
import random
from pygame.locals import *
import time
import numpy as np
import sys


pygame.init()
window_size = (640, 580)
screen = pygame.display.set_mode(window_size)
#screen = pygame.display.set_mode(window_size, flags=pygame.HIDDEN)

##################################### 

def draw_plane_rowsq(start_x, start_y, distance_between, square_size):
    # Calculate the top-left corner of the square given the center coordinates and size
    def square_top_left(center_x, center_y, size):
        return center_x - size // 2, center_y - size // 2
    
    # Draw a square at the given x and y coordinates with the given size
    def draw_square(x, y, size):
        pygame.draw.rect(screen, (255, 0, 0), (x, y, size, size))
    
    # Calculate the top-left corners of the squares based on the center coordinates and size
    top_left_1 = square_top_left(start_x + distance_between, start_y, square_size)
    top_left_2 = square_top_left(start_x + distance_between * 2, start_y, square_size)
    top_left_3 = square_top_left(start_x + distance_between * 3, start_y, square_size)
    top_left_4 = square_top_left(start_x - distance_between, start_y, square_size)
    top_left_5 = square_top_left(start_x - distance_between * 2, start_y, square_size)
    top_left_6 = square_top_left(start_x - distance_between * 3, start_y, square_size)
    
    # Draw the squares at the calculated top-left corners
    draw_square(*top_left_1, square_size)
    draw_square(*top_left_2, square_size)
    draw_square(*top_left_3, square_size)
    draw_square(*top_left_4, square_size)
    draw_square(*top_left_5, square_size)
    draw_square(*top_left_6, square_size)
    
def draw_text(font_size, text, x_coord, y_coord):
    font = pygame.font.Font(None, font_size)
    color = (255, 255, 255)
    text_image = font.render(text, True, color)

    # Get the size of the text image
    text_width, text_height = text_image.get_size()

    # Calculate the top-left corner of the text image
    text_x = x_coord - text_width // 2
    text_y = y_coord - text_height // 2

    # Draw the text image on the screen
    screen.blit(text_image, (text_x, text_y))
    
def draw_seat_nums(seat_num, x_coord, y_coord,col_names):
        
    draw_text(36, "A" , start_x - distance_between * 3 , start_y - distance_between)
    draw_text(36, "F" , start_x + distance_between * 3 , start_y - distance_between)
    
    draw_text(36, "B" , start_x - distance_between * 2 , start_y - distance_between)
    draw_text(36, "E" , start_x + distance_between * 2 , start_y - distance_between)
        
    draw_text(36, "C" , start_x - distance_between * 1 , start_y - distance_between)
    draw_text(36, "D" , start_x + distance_between * 1 , start_y - distance_between)
    
    for i in range(seat_num):
        draw_text(25, str(i + 1) , start_x - distance_between * 4 , start_y + distance_between * i)
        
def seat_coord_finder(seat_label, seat_num, x_coord, y_coord, distance_between,col_names):
    ass_dist = [-3,-2,-1,1,2,3]
    
    the_index = col_names.index(seat_label)
    ret_x = x_coord + distance_between * ass_dist[the_index]
    ret_y = y_coord + distance_between * (seat_num - 1)
    return   (ret_x,ret_y)
#zz = seat_coord_finder("A", 3, start_x, start_y, distance_between)
#pygame.draw.circle(screen, (122, 110, 50), (zz[0] ,zz[1]), dot_radius )

def update_checkarrived(psnger):
    psnger.update(0,p_speed)
    #if the passenger arrived, set them up a wait time while placing their baggage
    if not (psnger.y < desty):
        psnger.putbag(bag_placment_time)
        psnger.setcolor((204, 255, 205))
        
def find_closest_pass_Y(psnger): #pass the current passenger
    the_pass = None
    for i in passengers:
        if (i.y - psnger.y < distance_between + 1) and (i.y - psnger.y  > 0) and ( abs(i.x - psnger.x) < distance_between) :
            the_pass = i
    return the_pass
   
#Returns a passengers [seat lablel, seat number] 
# A_3 --> [A,3]

def extract_seat_label(psnger):
    return psnger.seat_num.split("_")[0],psnger.seat_num.split("_")[1]

#When a passenger is about to enter their row, computes how many people are on the way. 
# "on the way" is how many people needs to be removed for the passenger to be physically able to sit to their seat
def check_pass_ontheway(psnger):
    num_sitting = 0 #return variable
    sitting_plan= [0,0,0]
    psl,psn =  extract_seat_label(psnger)
    search_array = []
    
    if ( psl in ["A","B","C"] ):
        search_array =  ["A","B","C"]
    else:
        search_array =   ["D","E","F"]

    for i in passengers:
        nsl,nsn = extract_seat_label(i)
        if (nsn == psn) and (psl != nsl) and ((i.seated == 1)) and (nsl in search_array):
            sitting_plan[search_array.index(nsl)] = 1
    
    #the summation is reversed until the passengers seat label this if nest handles the symetric reflection problem the two sides of the plane creates
    if  search_array ==   ["D","E","F"]:
        for i in range(search_array.index(psl)):
            num_sitting += sitting_plan[i]
    else:
        sitting_plan = sitting_plan[::-1]
        for i in range(len(search_array) - search_array.index(psl)):
            num_sitting += sitting_plan[i]
    return num_sitting
    
def check_same_row(psnger):
    num_sitting = 0
    psl,psn =  extract_seat_label(psnger)
    label_search = []
    
    if ( psl in ["A","B","C"] ):
        label_search = [f"{x}_{psn}" for x in  ["A","B","C"]]
    else:
        label_search = [f"{x}_{psn}" for x in  ["D","E","F"]]
        
    for i in passengers:
        if (i.seat_num in label_search) and (i.seat_num != psnger.seat_num) and ((i.seated == 1)):
            num_sitting += 1
    return num_sitting

#closest_pass_sl,closest_pass_sn = closest_pass.seat_num[i].split("_")
##################################### 

def shuffle_with_priority(arr):
    group1 = [s for s in arr if (s.startswith("A") or s.startswith("F")) and int(s.split("_")[1]) > 8 ]
    group2 = [s for s in arr if (s.startswith("A") or s.startswith("F")) and int(s.split("_")[1]) <= 8 ]
    group3 = [s for s in arr if  (s.startswith("B") or s.startswith("E")) and int(s.split("_")[1]) > 8]
    group4 = [s for s in arr if  (s.startswith("B") or s.startswith("E") )and int(s.split("_")[1]) <= 8]
    group5 = [s for s in arr if  (s.startswith("C") or s.startswith("D") )and int(s.split("_")[1]) > 8 ]
    group6 = [s for s in arr if  (s.startswith("C") or s.startswith("D")) and int(s.split("_")[1]) <= 8]

    random.shuffle(group1)
    random.shuffle(group2)
    random.shuffle(group3)
    random.shuffle(group4)
    random.shuffle(group5)
    random.shuffle(group6)


    return group1 + group2 +group3 + group4 + group5 + group6

def shuffle_no_rule(arr):
    print(arr)
    random.shuffle(arr)
    random.shuffle(arr)
    random.shuffle(arr)
    return arr


##################################### 

#Creating a Dot class for passengers
class Dot:
    def __init__(self, x, y, color, speed, radius, seat_num,dest_xx,dest_yy):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.radius = radius
        self.seat_num = seat_num
        self.destx = dest_xx
        self.desty = dest_yy
        self.placing = 0
        self.seated = 0 #
        
    def update(self,xadd,yadd):
        self.x += xadd
        self.y += yadd
        
    def putbag(self,waittime):
        self.placing += waittime
        
    def seated_status(self,status):
        self.seated = status #1 is actively waiting 0 is not waiting 
    def setcolor(self,color):
        self.color = color 


p_rad = 10 #radius of the passenger node
speed_multiplier = 10
onesec_pixel_speed = 0.1666667 #default speed, corresponds to real world speed of simulation
currently_seated = 0 
p_speed = (onesec_pixel_speed) * speed_multiplier
dist_treshold = 10 #the distance between the edges oaf seats and passengers
distance_between = p_rad * 2 + dist_treshold #dist of seats from one another
square_size = 20
start_x = window_size[0]/2 #start of the first seats x coord
start_y = window_size[1]/10 #start of the first seats y coord
seat_num = 15

#Creating the passengers
# Create a list to store the passengers

#Seat Combinations
col_names = ["A","B","C","D","E","F"]
#Creates the seat combinations 
combinations = []
for col in col_names:
    for i in range(1, seat_num+1):
        combinations.append(f"{col}_{i}")


# combinations = ['D_2', 'F_9', 'A_2', 'B_6', 'D_4', 'A_13', 'A_7', 'A_9', 'D_7', 'C_14', 'D_15', 'D_8', 'F_15', 'F_11', 'B_3', 'B_2', 'C_4', 'C_5', 'D_6', 'E_1', 'B_8', 'E_10', 'A_4', 'C_13', 'E_12', 'E_2', 'F_10', 'A_15', 'A_8', 'D_13', 'C_7', 'A_12', 'E_5', 'A_6', 'B_15', 'A_14', 'E_9', 'B_5', 'F_6', 'B_7', 'E_15', 'E_8', 'C_8', 'D_11', 'B_9', 'D_10', 'D_1', 'E_7', 'B_10', 'F_8', 'A_3', 'C_3', 'C_11', 'C_15', 'D_3', 'A_11', 'B_14', 'F_13', 'D_14', 'C_2', 'D_9', 'C_10', 'E_4', 'F_5', 'F_3', 'A_10', 'D_12', 'F_14', 'C_1', 'E_3', 'B_1', 'A_1', 'C_6', 'D_5', 'F_2', 'F_1', 'B_13', 'E_6', 'E_13', 'B_4', 'C_9', 'A_5', 'B_11', 'B_12', 'C_12', 'F_12', 'E_11', 'F_4', 'F_7', 'E_14']

#######################################################
#Here if you choose to use this combination you will demonstrate a the -First window, middle and lastly cooridor approach.
#combinations = shuffle_with_priority(combinations)

#Here if you choose to use this combination you will demonstrate a completely random method, so represents no specific model.
combinations = shuffle_no_rule(combinations)

#Here is an example seat rule that is an actual case of a plane, same as no model, just a specific instance
# combinations = ['D_2', 'F_9', 'A_2', 'B_6', 'D_4', 'A_13', 'A_7', 'A_9', 'D_7', 'C_14', 'D_15', 'D_8', 'F_15', 'F_11', 'B_3', 'B_2', 'C_4', 'C_5', 'D_6', 'E_1', 'B_8', 'E_10', 'A_4', 'C_13', 'E_12', 'E_2', 'F_10', 'A_15', 'A_8', 'D_13', 'C_7', 'A_12', 'E_5', 'A_6', 'B_15', 'A_14', 'E_9', 'B_5', 'F_6', 'B_7', 'E_15', 'E_8', 'C_8', 'D_11', 'B_9', 'D_10', 'D_1', 'E_7', 'B_10', 'F_8', 'A_3', 'C_3', 'C_11', 'C_15', 'D_3', 'A_11', 'B_14', 'F_13', 'D_14', 'C_2', 'D_9', 'C_10', 'E_4', 'F_5', 'F_3', 'A_10', 'D_12', 'F_14', 'C_1', 'E_3', 'B_1', 'A_1', 'C_6', 'D_5', 'F_2', 'F_1', 'B_13', 'E_6', 'E_13', 'B_4', 'C_9', 'A_5', 'B_11', 'B_12', 'C_12', 'F_12', 'E_11', 'F_4', 'F_7', 'E_14']
#######################################################


#Creates each passenger
passengers = []
for i in range(len(combinations)):
    #each passengers seat coordinates are computed
    sl,sn = combinations[i].split("_")
    dest_x,dest_y = seat_coord_finder(sl, int(sn), start_x, start_y, distance_between,col_names)
    
    passenger = Dot(start_x  ,  start_y - distance_between * (i + 1), (204,204,255) ,p_speed , p_rad, combinations[i],dest_x,dest_y)
    passengers.append(passenger)

clock = pygame.time.Clock()
 #draw_plane_row(start_x,start_y,distance_between,dot_radius)

bag_placment_time = 60
time_counter = 0

switch_to_zero_the_time = 0 #turns 1, used to get the start extra time on the simulation at the start to avoid adding up as the speed is increased
quitte = True

while quitte:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 0, 0))

#Creates a Counter to keep the time
    if switch_to_zero_the_time == 0:
        start_time = pygame.time.get_ticks()
        switch_to_zero_the_time = 1
        start_time= start_time* speed_multiplier
        

        
        
    real_time = pygame.time.get_ticks() #tracks real world seconds
    total_seconds_elapsed = (pygame.time.get_ticks() * speed_multiplier) - start_time #Based on the simulation speed adujst the simulation time 
    seconds = (total_seconds_elapsed/1000) % 60
    minutes = int((total_seconds_elapsed/1000) // 60)
    elapsed_time_text = f"Elapsed time: {format(minutes, '02d')}:{seconds:.0f} minutes"
    font = pygame.font.Font(None, 30)
    text = font.render(elapsed_time_text, 1, (255,255,255))
    screen.blit(text, (10, 550))


#Draws the plane seat layout
    plane_y = start_y
    for i in range(seat_num):
        draw_plane_rowsq(start_x, plane_y, distance_between, square_size)
        plane_y += distance_between

    draw_seat_nums(seat_num,start_x,start_y,col_names)
#Layout is ended

#Draw initiate passg
# Draw the dots
#     seat_coord_finder(seat_label, seat_num, x_coord, y_coord, distance_between,col_names)

    
    for idx,psnger in enumerate(passengers):
        time_counter += 1
        x, y = psnger.x, psnger.y
        destx,desty = psnger.destx ,  psnger.desty
        
        pygame.draw.circle(screen, psnger.color, (x, y), psnger.radius)
        

        #move forward
        closest_pass = find_closest_pass_Y(psnger)
        passenger_seat_label = extract_seat_label(psnger)[0]
        
        if y < desty:
            if closest_pass == None:
                update_checkarrived(psnger)
            else:
                pass

                
                
                   
        #if applies move left         
        elif x > destx and (passenger_seat_label in ["A","B","C"]) :
            num_ppl_sitting_in_row = check_pass_ontheway(psnger) 
            if psnger.placing > 0:
                psnger.putbag(-onesec_pixel_speed * speed_multiplier)
                if ( num_ppl_sitting_in_row > 0):
                    psnger.putbag(onesec_pixel_speed* 0.4*num_ppl_sitting_in_row * speed_multiplier)
                    psnger.setcolor((255,255,0))
            else:
                psnger.setcolor((255, 255, 255))
                psnger.update(-1*p_speed/2,0) #divided by 2 because a person moves slower allocating in seats
                
                
        #if applies move right         
        elif x < destx and (passenger_seat_label in ["D","E","F"]):
            num_ppl_sitting_in_row = check_pass_ontheway(psnger) 
            if psnger.placing > 0:
                psnger.putbag(-onesec_pixel_speed * speed_multiplier)
                if ( num_ppl_sitting_in_row > 0):
                    psnger.putbag(onesec_pixel_speed*0.40* num_ppl_sitting_in_row * speed_multiplier)
                    psnger.setcolor((255,255,0))
            else:
                psnger.setcolor((255, 255, 255))
                psnger.update(p_speed/2,0) #divided by 2 because a person moves slower allocating in seats
                
        else:
            if ( psnger.seated == 0):
                psnger.seated_status(1)
                currently_seated += 1
            
        #print(idx, psnger.placing)
        clock.tick(10000.00)
        if currently_seated >= len(combinations):
            total_seconds_elapsed = (pygame.time.get_ticks() * speed_multiplier) - start_time
            print("tsss",total_seconds_elapsed,"starttime: ", start_time)
            print("loop time:", time_counter)
            #pygame.quit()
            #sys.exit()
            quitte = False
 

    pygame.display.update()
