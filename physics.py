

import random
import pygame
import math
from constants import *

class Planet: # Assuming all the planets have the same density
    
    def __init__(self, x_pos, y_pos, planet_radius, color, choice, planets):
        self.x = x_pos
        self.y = y_pos
        self.radius = planet_radius
        self.mass = DENSITY * (planet_radius**3) * SCALE
        self.color = color
        if choice:
            if choice == 1:
                planet = planets[0]
                mass = DENSITY * (planet.radius**3) * SCALE
                distance = math.sqrt((planet.x - x_pos)**2 + (planet.y - y_pos)**2)
                orbital_vel = math.sqrt(GRAVITATIONAL_CONSTANT * mass / distance)
                theta = planet.angle_calc(self)
                self.vel_x = orbital_vel * math.sin(theta)
                self.vel_y = -1 * orbital_vel * math.cos(theta)
            elif choice == 2:
                planet = planets[0]
                mass = DENSITY * (planet.radius**3) * SCALE
                distance = math.sqrt((planet.x - x_pos)**2 + (planet.y - y_pos)**2)
                escape_vel = math.sqrt(2*GRAVITATIONAL_CONSTANT * mass / distance)
                theta = planet.angle_calc(self)
                self.vel_x = escape_vel * math.sin(theta)
                self.vel_y = -1 * escape_vel * math.cos(theta)
            elif choice == 3:
                # random launch
                ###
                planet = planets[0]
                mass = DENSITY * (planet.radius**3) * SCALE
                distance = math.sqrt((planet.x - x_pos)**2 + (planet.y - y_pos)**2)
                orbital_vel = math.sqrt(GRAVITATIONAL_CONSTANT * mass / distance)
                escape_vel = math.sqrt(2) * orbital_vel
                ###
                theta = (random.random())*2*math.pi
                vel_total = (random.random())*(escape_vel - orbital_vel) + orbital_vel
                self.vel_x = vel_total * math.sin(theta)
                self.vel_y = -1 * vel_total * math.cos(theta)
            elif choice == 4:
                planet = planets[0]
                theta = planet.angle_calc(self) - math.pi/2
                vel_total = 100
                self.vel_x = vel_total * math.sin(theta)
                self.vel_y = -1 * vel_total * math.cos(theta)
        else:
            self.vel_x = 0
            self.vel_y = 0
                
    
    @classmethod # general function so needs to be class function
    def sq_distance_bw_2pts(cls, planet1, planet2):
        sqrd_distance = (planet1.x - planet2.x)**2 + (planet1.y - planet2.y)**2
        return sqrd_distance
    
    def angle_calc(self, planet2): # angle from a planet to another so calculated for each planet seperately
        if planet2.x < self.x:
            theta = (math.atan((planet2.y - self.y)/(planet2.x - self.x))) # will be +ve
            theta = math.pi + theta
        else:   
            theta = math.atan((planet2.y - self.y)/(planet2.x - self.x)) # in radians
        
        return theta

    def cal_F_xy(self, planet2): # F is a vector so calculated for each planet seperately
        sqrd_distance = Planet.sq_distance_bw_2pts(self, planet2)
        F_total = (GRAVITATIONAL_CONSTANT * planet2.mass * self.mass) / sqrd_distance
        theta = self.angle_calc(planet2)
        F_x = F_total * math.cos(theta)
        F_y = F_total * math.sin(theta)
        return (F_x, F_y)
    
    @classmethod # all the planets are passed so need to be a class function
    def motion(cls, planets):
        for planet in planets:
            F_x_net = 0
            F_y_net = 0
            for x in planets:
                if x != planet:
                    F_net = planet.cal_F_xy(x)
                    F_x_net += F_net[0]
                    F_y_net += F_net[1]
            acc_x = F_x_net/planet.mass
            acc_y = F_y_net/planet.mass
            planet.vel_x += acc_x
            planet.vel_y += acc_y
            planet.x += planet.vel_x
            planet.y += planet.vel_y

    @classmethod
    def circleCollision(cls, planet1, planet2):
        r1 = planet1.radius
        r2 = planet2.radius

        distance_between_centers = math.sqrt(Planet.sq_distance_bw_2pts(planet1, planet2))

        if r2>r1: # exchanging r1 and r2 values
            temp = r1
            r1 = r2
            r2 = temp
        
        if distance_between_centers < (r1+r2):
            print("collision")
            return True
        else:
            return False
        


    @classmethod
    def SeperateSmall(cls, planet1, planet2): # changes the distance after collision but not their velocities
        #changes the distance wrt to the velocities (along the line of impact) directions so that furthur collision can be avoided
        small_distance = 5 # 5px
        planet1.x += planet1.vel_x
        planet2.x += planet2.vel_x
        planet1.y += planet1.vel_y
        planet2.y += planet2.vel_y


                
    @classmethod
    def planetCollision(cls, planets): # returns true if planets collide
        for planet in planets:
            for x in planets:
                if x != planet:
                    if Planet.circleCollision(planet, x):
                        Planet.elasticCollision(planet, x) #They have collided time to seperate them along the line of collision
                        Planet.SeperateSmall(planet, x)


    
    @classmethod
    def elasticCollision(cls, planet1, planet2): # change the velocities of the bodies after the elastic collision according to physics
        # we need to calculate the velocities along the line of collision
        # theta1 = planet1.angle_calc(planet2)
        # theta2 = planet2.angle_calc(planet1)
        m1 = planet1.mass
        m2 = planet2.mass

        u1_x = planet1.vel_x
        u2_x = planet2.vel_x

        u1_y = planet1.vel_y
        u2_y = planet2.vel_y


        # Physics calculations -------- Based on conservation of linear momentum and conservation of energy
        v1_x = ((m1-m2)/(m1+m2))*u1_x + ((2*m2)/(m1+m2))*u2_x
        v1_y = ((m1-m2)/(m1+m2))*u1_y + ((2*m2)/(m1+m2))*u2_y

        v2_x = ((2*m1)/(m1+m2))*u1_x - ((m1-m2)/(m1+m2))*u2_x
        v2_y = ((2*m1)/(m1+m2))*u1_y - ((m1-m2)/(m1+m2))*u2_y
        # Physics calculations -------- Based on conservation of linear momentum and conservation of energy


        planet1.vel_x = v1_x
        planet1.vel_y = v1_y

        planet2.vel_x = v2_x
        planet2.vel_y = v2_y
