#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    """class for working with 2d vectors"""
    def __init__(self, x_coord, y_coord):
        if not (isinstance(x_coord, (int, float)) and
                isinstance(y_coord, (int, float))):
            print(type(x_coord))
            print(type(y_coord))
            raise TypeError
        
        self.x_coord = x_coord
        self.y_coord = y_coord
    
    def __add__(self, other):
        return Vec2d(self.x_coord + other.x_coord,
                     self.y_coord + other.y_coord)
    
    def __sub__(self, other):
        return Vec2d(self.x_coord - other.x_coord,
                     self.y_coord - other.y_coord)
    
    def __mul__(self, other):
        return Vec2d(other * self.x_coord, other * self.y_coord)
    
    def __len__(self):
        return int(math.sqrt(self.x_coord**2 + self.y_coord**2))
    
    def int_pair(self):
        return int(self.x_coord), int(self.y_coord)
    
    def x_spin(self):
        self.x_coord = -self.x_coord
    
    def y_spin(self):
        self.y_coord = -self.y_coord
    
    def vector_len(self):
        return math.sqrt(self.x_coord**2 + self.y_coord**2)


class Polyline:
    """class for working with points of polylines"""
    def __init__(self, screen_dim, gameDisplay, delta = 0.1,
                 default_speed = 2, max_speed = 10):
        self.points = []
        self.speeds = []
        self.screen_dim = screen_dim
        self.game_display = gameDisplay
        self.speed_delta = delta
        self.default_speed = default_speed
        self.max_speed = max_speed
    
    def add_point(self, point, speed = None):
        if not isinstance(point, tuple):
            raise TypeError
        if not (isinstance(speed, tuple) or speed is None):
            raise TypeError
        
        if speed is None:
            if len(self.speeds) == 0:
                speed_vec_len = self.default_speed
            else:
                speed_vec_len = (
                    sum([speed.vector_len() for speed in self.speeds]) /
                    len(self.speeds)
                )
            self.speeds.append(Vec2d(random.random() * speed_vec_len,
                                     random.random() * speed_vec_len))
        else:
            self.speeds.append(Vec2d(*speed))
        
        self.points.append(Vec2d(*point))
    
    def set_points(self):
        """method to calculate new position of points"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if (
                self.points[p].x_coord > self.screen_dim[0] or
                self.points[p].x_coord < 0
            ):
                self.speeds[p].x_spin()
            if (
                self.points[p].y_coord > self.screen_dim[1] or
                self.points[p].y_coord < 0
            ):
                self.speeds[p].y_spin()
    
    def draw_points(self, width=3, color=(255, 255, 255)):
        """method to draw points on the screen"""
        for p in self.points:
            pygame.draw.circle(self.game_display, color, p.int_pair(), width)
    
    def clear_points(self):
        """method to delete current points and their speeds"""
        self.points = []
        self.speeds = []
    
    def pop_point(self):
        """pop point from polyline"""
        if len(self.points) > 0:
            self.points.pop(-1)
            self.speeds.pop(-1)
    
    def get_speed_change(self, speed):
        """calculate speed change of speed vector"""
        if speed.vector_len() == 0:
            random_speed = Vec2d(random.random() * 2, random.random() * 2)
            return (random_speed * self.speed_delta *
                    (1/random_speed.vector_len()))
            
        return speed * self.speed_delta * (1/speed.vector_len())
    
    def increase_speed(self):
        """increase speed of points"""
        for s in range(len(self.speeds)):
            speed_change = self.get_speed_change(self.speeds[s])
            if (self.speeds[s].vector_len() + speed_change.vector_len() >
                    self.max_speed):
                continue
            self.speeds[s] += speed_change
    
    def decrease_speed(self):
        """decrease speed of points"""
        for s in range(len(self.speeds)):
            speed_change = self.get_speed_change(self.speeds[s])
            if self.speeds[s].vector_len() <= speed_change.vector_len():
                self.speeds[s] = Vec2d(0, 0)
                continue
            self.speeds[s] -= speed_change


class Knot(Polyline):
    """class for working with closed polylines"""
    def __init__(self, screen_dim, gameDisplay, count = 35):
        super().__init__(screen_dim, gameDisplay)
        self.knot_points = []
        self.count = count
    
    def get_point(self, points, alpha, deg=None):
        """recursive method to calculate polyline point"""
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha +
                self.get_point(points, alpha, deg - 1) * (1 - alpha))


    def get_points(self, base_points):
        """returns polyline points for different alphas"""
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res
    
    def get_knot(self):
        """creates a knot of polyline points"""
        if len(self.points) < 3:
            self.knot_points = []
            return
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn))
        self.knot_points = res
        return self.knot_points
        
    def add_point(self, point, speed = None):
        super().add_point(point, speed)
        self.get_knot()
    
    def set_points(self,):
        super().set_points()
        self.get_knot()
    
    def pop_point(self):
        super().pop_point()
        self.get_knot()
    
    def draw_knot(self, width=3, color=(255, 255, 255)):
        """draws a knot on the screens"""
        for p_n in range(-1, len(self.knot_points) - 1):
            pygame.draw.line(self.game_display, color,
                                self.knot_points[p_n].int_pair(),
                                self.knot_points[p_n + 1].int_pair(), width)


class ScreenSaver:
    def __init__(self, screen_dim, gameDisplay, working = True, pause = True):
        self.screen_dim = screen_dim
        self.game_display = gameDisplay
        self.hue = 0
        self.color = pygame.Color(0)
        self.show_help = False
        self.reset(working, pause)
    
    def reset(self, working = True, pause = True):
        self.knots = [Knot(self.screen_dim, self.game_display)]
        self.current_knot = 0
        self.working = working
        self.pause = pause
    
    def add_knot(self):
        """add knot to screensaver"""
        self.knots.append(Knot(self.screen_dim, self.game_display))
        self.current_knot += 1
    
    def get_current_knot(self):
        return self.knots[self.current_knot]
    
    def remove_point(self):
        """remove point from current knot and remove knot if it is empty"""
        self.knots[self.current_knot].pop_point()
        if (len(self.knots[self.current_knot].points) == 0 and
                len(self.knots) > 1):
            self.knots.pop(self.current_knot)
            if self.current_knot == len(self.knots):
                self.current_knot -= 1
    
    def draw_knots(self):
        self.game_display.fill((0, 0, 0))
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)
        for k in range(len(self.knots)):
            if k == self.current_knot:
                self.knots[k].draw_points(3, (255, 0, 0))
                self.knots[k].draw_knot(3, self.color)
            else:
                self.knots[k].draw_points()
                self.knots[k].draw_knot()
    
    def set_points(self):
        for knot in self.knots:
            knot.set_points()
    
    def next_knot(self):
        """select next knot"""
        self.current_knot += 1
        if self.current_knot == len(self.knots):
                self.current_knot = 0
    
    def previous_knot(self):
        """select previous knot"""
        self.current_knot -= 1
        if self.current_knot == -1:
                self.current_knot = len(self.knots) - 1

    def draw_help(self):
        """function for drawing help screen"""
        self.game_display.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["L Click", "Add node to selected knot"])
        data.append(["R Click", "Remove node from selected knot"])
        data.append(["Middle Click", "Create new knot"])
        data.append(["UP", "Increase speed of selected knot"])
        data.append(["DOWN", "Decrease speed of selected knot"])
        data.append(["LEFT", "Previous knot"])
        data.append(["RIGHT", "Next knot"])
        data.append(["Num+", "Add intermediary points to selected knot"])
        data.append(["Num-", "Remove intermediary points from selected knot"])
        data.append(["", ""])
        data.append([str(self.get_current_knot().count),
                    "Current intermediary points"])

        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.game_display.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.game_display.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    screensaver = ScreenSaver(SCREEN_DIM, gameDisplay)

    while screensaver.working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screensaver.working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screensaver.working = False
                if event.key == pygame.K_r:
                    screensaver.reset()
                if event.key == pygame.K_p:
                    screensaver.pause = not screensaver.pause
                if event.key == pygame.K_KP_PLUS:
                    screensaver.get_current_knot().count += 1
                if event.key == pygame.K_F1:
                    screensaver.show_help = not screensaver.show_help
                if event.key == pygame.K_KP_MINUS:
                    if screensaver.get_current_knot().count > 1:
                        screensaver.get_current_knot().count -= 1
                    else:
                        0
                if event.key == pygame.K_UP:
                    screensaver.get_current_knot().increase_speed()
                if event.key == pygame.K_DOWN:
                    screensaver.get_current_knot().decrease_speed()
                if event.key == pygame.K_LEFT:
                    screensaver.previous_knot()
                if event.key == pygame.K_RIGHT:
                    screensaver.next_knot()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    screensaver.get_current_knot().add_point(event.pos)
                if pygame.mouse.get_pressed()[2]:
                    screensaver.remove_point()
                if pygame.mouse.get_pressed()[1]:
                    screensaver.add_knot()
                    screensaver.get_current_knot().add_point(event.pos)
        
        screensaver.draw_knots()
        if not screensaver.pause:
            screensaver.set_points()
        if screensaver.show_help:
            screensaver.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)