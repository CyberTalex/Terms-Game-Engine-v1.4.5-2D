#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys, random, time, os, pickle
import text as text
import tkinter as tk
from tkinter import filedialog
from tkinter import Tk
import clip as clip
from floodfill import fill
# Version ---------------------------------------------------- #
version = '3.0'
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Terms Game Engine Pixel Editor v' + version)
global WINDOWWIDTH, WINDOWHEIGHT
WINDOWWIDTH = 700
WINDOWHEIGHT = 500
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)
# Images ----------------------------------------------------- #
def load2x(path):
    img = pygame.image.load('images/' + path + '.png').convert()
    img = pygame.transform.scale(img,(img.get_width()*2,img.get_height()*2))
    img.set_colorkey((0,0,0))
    return img

color_select_img = load2x('color_select')

color_overlay_img = load2x('colors')

color_picker_img = load2x('color_picker')
floodfill_img = load2x('floodfill')
selection_img = load2x('selection')
selection_resize_img = load2x('selection_resize')

play_img = load2x('play')
pause_img = load2x('pause')
delete_img = load2x('delete')
opacity_img = load2x('opacity')
onion_img = load2x('onion')

export_bg_img = load2x('export_bg')

transparency_img = pygame.image.load('images/transparency.png')
# Text ------------------------------------------------------- #
def get_text_width(text,spacing):
    global font_dat
    width = 0
    for char in text:
        if char in font_dat:
            width += font_dat[char][0] + spacing
        elif char == ' ':
            width += font_dat['A'][0] + spacing
    return width

global font_dat
font_dat = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2],'/':[3],'_':[5],'=':[3],'\\':[3],'[':[2],']':[2],'*':[3],'"':[3],'<':[3],'>':[3],';':[1]}
font = text.generate_font('font/small_font.png',font_dat,5,8,(248,248,248))
font_2 = text.generate_font('font/small_font.png',font_dat,5,8,(112,240,77))
# Classes ---------------------------------------------------- #

# canvas contains frames and a frame contains layers that are the canvas_img object

class canvas_img(object):
    def __init__(self,size_x,size_y):
        global colors
        self.size_x = size_x
        self.size_y = size_y
        self.image = pygame.Surface((size_x,size_y))
        self.image.fill(colors[1])
        self.opacity = 255
        self.string_form = ''
    def render(self,surf,pos,zoom,opacity_multiplier):
        global colors
        self.image.set_colorkey(colors[1])
        img_copy = self.image.copy()
        img_copy.set_alpha(int(self.opacity*opacity_multiplier))
        surf.blit(pygame.transform.scale(img_copy,(self.image.get_width()*zoom,self.image.get_height()*zoom)),pos)
    def resize(self,x,y):
        global colors
        self.size_x = x
        self.size_y = y
        new_surf = pygame.Surface((x,y))
        new_surf.fill(colors[1])
        new_surf.blit(self.image,(0,0))
        self.image = new_surf
    def handle_draws(self,pos,zoom,mouse):
        global colors, brush_size, f_key, s_key, selecting, selection
        cancel = False
        if (s_key == True) or (selecting[0] == True) or (selection[0] != None):
            cancel = True
        if (mouse.pos[0] < 134) and (mouse.pos[1] < 344):
            cancel = True
        if mouse.pos[1] < 25:
            cancel = True
        if mouse.pos[1] > WINDOWHEIGHT-130:
            cancel = True
        if cancel == False:
            base_x = mouse.pos[0]-pos[0]
            base_y = mouse.pos[1]-pos[1]
            draw_x = int(base_x/zoom)
            draw_y = int(base_y/zoom)
            if (draw_x >= 0) and (draw_x < self.size_x) and (draw_y >= 0) and (draw_y < self.size_y):
                if mouse.left_click == True:
                    self.last_pos = mouse.pos.copy()
                    if f_key == True:
                        add_log_state()
                        fill(self.image,(draw_x,draw_y),colors[0])
                    elif ctrl == False:
                        add_log_state()
                if mouse.right_click == True:
                    add_log_state()
            else:
                mouse.left_clicking = False
                mouse.right_clicking = False
            base_x = mouse.last_pos[0]-pos[0]
            base_y = mouse.last_pos[1]-pos[1]
            draw_last_x = int(base_x/zoom)
            draw_last_y = int(base_y/zoom)
            if (draw_x >= 0) and (draw_x < self.size_x) and (draw_y >= 0) and (draw_y < self.size_y):
                if mouse.left_clicking == True:
                    if ctrl == False:
                        if f_key == False:
                            pygame.draw.line(self.image,colors[0],(draw_x,draw_y),(draw_last_x,draw_last_y),brush_size)
                    else:
                        color = self.image.get_at((draw_x,draw_y))
                        colors[0] = (color[0],color[1],color[2])
                if mouse.right_clicking == True:
                    pygame.draw.line(self.image,colors[1],(draw_x,draw_y),(draw_last_x,draw_last_y),brush_size)

class frame(object):
    def __init__(self,size_x,size_y,image_list=None):
        global colors
        self.size_x = size_x
        self.size_y = size_y
        if image_list == None:
            self.layers = [canvas_img(size_x,size_y)]
        else:
            self.layers = image_list.copy()
    def resize(self,x,y):
        self.size_x = x
        self.size_y = y
        for img in self.layers:
            img.resize(x,y)
    def render(self,surf,pos,zoom,opacity_multiplier):
        for layer in self.layers:
            layer.render(surf,pos,zoom,opacity_multiplier)
    def copy(self):
        new_frame = frame(self.size_x,self.size_y)
        new_layers = []
        for layer in self.layers:
            new_img = canvas_img(self.size_x,self.size_y)
            new_img.image = layer.image.copy()
            new_layers.append(new_img)
        new_frame.layers = new_layers.copy()
        return new_frame

class canvas(object):
    def __init__(self,size_x,size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.frames = [frame(size_x,size_y)]
        self.frame_num = 0
        self.layer_num = 0
        self.raw_pos = [0,0]
    def prepare_for_pickle(self):
        for frame_obj in self.frames:
            for layer in frame_obj.layers:
                layer.string_form = pygame.image.tostring(layer.image,'RGBA')
    def post_pickle_handling(self):
        for frame_obj in self.frames:
            for layer in frame_obj.layers:
                layer.image = pygame.image.fromstring(layer.string_form,(layer.size_x,layer.size_y),'RGBA').convert()
                layer.image.convert_alpha()
    def render(self,surf,pos,zoom,opacity_multiplier=1):
        global mouse_data
        base_x = mouse_data.pos[0]-pos[0]
        base_y = mouse_data.pos[1]-pos[1]
        draw_x = int(base_x/zoom)
        draw_y = int(base_y/zoom)
        self.raw_pos = [draw_x,draw_y]
        if opacity_multiplier == 1:
            transparency_pos = pos.copy()
            if transparency_pos[0] < 0:
                transparency_pos[0] = 0
            if transparency_pos[1] < 0:
                transparency_pos[1] = 0
            for frame_obj in self.frames:
                n = 0
                for image in frame_obj.layers:
                    image.opacity = self.frames[0].layers[n].opacity
                    n += 1
            surf.blit(clip.clip(transparency_img,transparency_pos[0],transparency_pos[1],self.size_x*zoom,self.size_y*zoom),pos)
        self.frames[self.frame_num].render(surf,pos,zoom,opacity_multiplier)
    def resize(self,x,y):
        self.size_x = x
        self.size_y = y
        for frame in self.frames:
            frame.resize(x,y)
    def copy(self):
        new_canvas = canvas(self.size_x,self.size_y)
        new_canvas.frames = []
        for f in self.frames:
            new_frame_list = []
            for layer in f.layers:
                new_img = canvas_img(self.size_x,self.size_y)
                new_img.image = layer.image.copy()
                new_frame_list.append(new_img)
            new_frame = frame(self.size_x,self.size_y,new_frame_list)
            new_canvas.frames.append(new_frame)
        new_canvas.frame_num = self.frame_num
        new_canvas.layer_num = self.layer_num
        return new_canvas
    def handle_draws(self,pos,zoom,mouse):
        self.frames[self.frame_num].layers[self.layer_num].handle_draws(pos,zoom,mouse)

class GUI_element(object):
    def __init__(self,element_type,pos,size,element_data=None,hidden=False,shift_left=False):
        self.type = element_type
        self.pos = pos
        self.hidden = hidden
        self.size = size
        self.element_data = element_data
        self.selected = False
        self.restrictions = [None,None,None,None]
        self.shift_left = shift_left
    def handle(self,surface,mouse_data):
        if self.hidden == False:
            if self.type == 'image_button':
                collide_test = pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
                clicked = False
                if collide_test.collidepoint(mouse_data.pos):
                    screen.blit(change_color(self.element_data,(248,248,248),(112,240,77)),self.pos)
                    if mouse_data.left_click == True:
                        mouse_data.reset()
                        clicked = True
                else:
                    screen.blit(self.element_data,self.pos)
                return clicked
            if self.type == 'text_button':
                collide_test = pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
                clicked = False
                if collide_test.collidepoint(mouse_data.pos):
                    text.show_text(self.element_data,self.pos[0],self.pos[1],1,99999,font_2,surface,2)
                    if mouse_data.left_click == True:
                        clicked = True
                else:
                    text.show_text(self.element_data,self.pos[0],self.pos[1],1,99999,font,surface,2)
                return clicked
            if self.type == 'text_field':
                if self.shift_left == True:
                    offset_x = get_text_width(self.element_data,1)
                else:
                    offset_x = 0
                collide_test = pygame.Rect(self.pos[0]-offset_x*2,self.pos[1],self.size[0],self.size[1])
                clicked = False
                if collide_test.collidepoint(mouse_data.pos):
                    text.show_text(self.element_data,self.pos[0]-offset_x*2,self.pos[1],1,99999,font_2,surface,2)
                    if mouse_data.left_click == True:
                        clicked = True
                else:
                    text.show_text(self.element_data,self.pos[0]-offset_x*2,self.pos[1],1,99999,font,surface,2)
                if clicked == True:
                    self.element_data = enter_text(self.element_data,self.restrictions)
                    mouse_data.reset()
                return self.element_data
            if self.type == 'slider':
                collide_test = pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
                if collide_test.collidepoint(mouse_data.pos):
                    if mouse_data.left_click == True:
                        self.selected = True
                if mouse_data.left_clicking == False:
                    self.selected = False
                elif self.selected == True:
                    self.element_data = (mouse_data.pos[0]-self.pos[0])/self.size[0]
                    if self.element_data > 1:
                        self.element_data = 1
                    if self.element_data < 0:
                        self.element_data = 0
                c = (248,248,248)
                if self.selected == True:
                    c = (112,240,77)
                pygame.draw.line(surface,(248,248,248),(self.pos[0],self.pos[1]+int(self.size[1]/2)),(self.pos[0]+self.size[0],self.pos[1]+int(self.size[1]/2)),2)
                pygame.draw.line(surface,c,(int(self.pos[0]+self.size[0]*self.element_data),self.pos[1]),(int(self.pos[0]+self.size[0]*self.element_data),self.pos[1]+self.size[1]),2)
                return self.element_data
            if self.type == 'toggle':
                collide_test = pygame.Rect(self.pos[0],self.pos[1],16,16)
                clicked = False
                if collide_test.collidepoint(mouse_data.pos):
                    if mouse_data.left_click == True:
                        clicked = True
                if clicked == True:
                    if self.selected == True:
                        self.selected = False
                    else:
                        self.selected = True
                if self.selected == True:
                    pygame.draw.rect(surface,(112,240,77),collide_test)
                pygame.draw.rect(surface,(248,248,248),collide_test,2)
                text.show_text(self.element_data,self.pos[0]+24,self.pos[1]+2,1,99999,font,surface,2)
                return self.selected

class mouse_data_obj(object):
    def __init__(self):
        self.pos = [0,0]
        self.last_pos = [0,0]
        self.left_click = False
        self.left_clicking = False
        self.right_click = False
        self.right_clicking = False
        self.middle_click = False
        self.middle_clicking = False
        self.last_clear = 0
    def update(self):
        mx,my = pygame.mouse.get_pos()
        self.last_pos = self.pos.copy()
        self.pos = [mx,my]
        self.left_click = False
        self.right_click = False
        self.middle_click = False
        self.last_clear += 1
        if self.last_clear < 3:
            self.reset(True)
    def reset(self,soft_clear=False):
        global ctrl
        ctrl = False
        if soft_clear == False:
            self.last_clear = 0
        self.pos = [0,0]
        self.left_click = False
        self.left_clicking = False
        self.right_click = False
        self.right_clicking = False
        self.middle_click = False
        self.middle_clicking = False
        self.last_pos = [0,0]

# Functions -------------------------------------------------- #
def change_color(image,old_color,new_color):
    new_surf = image.copy()
    new_surf.fill(new_color)
    new_img = image.copy()
    new_img.set_colorkey(old_color)
    new_surf.blit(new_img,(0,0))
    new_surf.set_colorkey((0,0,0))
    return new_surf

def read_f(path):
    f = open(path + '.txt','r')
    dat = f.read()
    f.close()
    return dat

def write_f(path,dat):
    f = open(path + '.txt','w')
    f.write(dat)
    f.close()

def enter_text(base_text,input_restrictions=[None,None,None,None]):
    global WINDOWWIDTH, WINDOWHEIGHT
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    special_chars = [';']
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    number_specials = ['-','.']
    global last_frame
    entering = True

    original_text = base_text

    backspace_hold = False
    backspace_hold_timer = 0
    
    while entering:
        screen.fill((0,0,0))
        screen.blit(last_frame,(0,0))

        box = pygame.Surface((get_text_width(base_text,1)*2+8,22))
        box.fill((0,17,32))

        pos =(int(WINDOWWIDTH/2-box.get_width()/2),int(WINDOWHEIGHT/2-box.get_height()/2))

        screen.blit(box,pos)
        text.show_text(base_text,pos[0]+4,pos[1]+4,1,99999,font,screen,2)

        if backspace_hold == True:
            backspace_hold_timer += 1
        else:
            backspace_hold_timer = 0
        if backspace_hold_timer > 30:
            if base_text != '':
                base_text = base_text[:-1]
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if input_restrictions[0] == None:
                    for char in alphabet:
                        if event.key == ord(char):
                            base_text += char
                if input_restrictions[1] == None:
                    for char in special_chars:
                        if event.key == ord(char):
                            base_text += char
                if input_restrictions[2] == None:
                    for char in numbers:
                        if event.key == ord(char):
                            base_text += char
                if input_restrictions[3] == None:
                    for char in number_specials:
                        if event.key == ord(char):
                            base_text += char
                if event.key == K_SPACE:
                    base_text += ' '
                if event.key == K_BACKSPACE:
                    backspace_hold = True
                    if base_text != '':
                        base_text = base_text[:-1]
                if event.key == K_RETURN:
                    entering = False
                if event.key == K_ESCAPE:
                    entering = False
                    base_text = original_text
            if event.type == KEYUP:
                if event.key == K_BACKSPACE:
                    backspace_hold = False

        pygame.display.update()
        mainClock.tick(60)

    return base_text

def str_sum(l,split_char='',add_at_end=True):
    new_str = ''
    for part in l:
        new_str += part + split_char
    if add_at_end == False:
        new_str = new_str[:-1]
    return new_str

def render_colors(surface,pos):
    global colors
    color_1_R = pygame.Rect(pos[0],pos[1],40,40)
    color_2_R = pygame.Rect(pos[0]+54,pos[1]+8,32,32)
    pygame.draw.rect(surface,colors[0],color_1_R)
    pygame.draw.rect(surface,colors[1],color_2_R)
    surface.blit(color_overlay_img,pos)

def simple_text(t,pos):
    text.show_text(t,pos[0],pos[1],1,99999,font,screen,2)

def add_log_state():
    global canvas_log, log_state, main_canvas
    if log_state != None:
        canvas_log = canvas_log[:log_state]
    canvas_log.append(main_canvas.copy())
    log_state = None

def undo():
    global canvas_log, log_state, main_canvas
    if log_state == None:
        canvas_log.append(main_canvas.copy())
        log_state = -2
    else:
        log_state -= 1
    if abs(log_state) >= len(canvas_log):
        log_state = -len(canvas_log)
def redo():
    global canvas_log, log_state
    if log_state != None:
        if log_state < -1:
            log_state += 1
        else:
            canvas_log.pop(-1)
            log_state = None

def get_image_colors(img):
    colors = []
    for y in range(img.get_height()):
        for x in range(img.get_width()):
            color = img.get_at((x,y))
            if color not in colors:
                colors.append(color)
    return colors

def color_str(color,reverse=False):
    if reverse == False:
        return str(color[0]) + ';' + str(color[1]) + ';' + str(color[2])
    else:
        parts = color.split(';')
        return (int(parts[0]),int(parts[1]),int(parts[2]))

def in_color_range(color,mode='rgb'):
    if mode == 'rgb':
        color = color.split(';')
        if len(color) != 3:
            return False
        else:
            good = True
            try:
                for val in color:
                    if int(val) < 0:
                        good = False
                    if int(val) > 255:
                        good = False
            except:
                good = False
            return good

def select_color():
    global mouse_data, colors, last_frame
    mouse_data.reset()

    save_b = GUI_element('text_button',(2,2),(40,18),'save')
    cancel_b = GUI_element('text_button',(52,2),(60,18),'cancel')
    raw_rgb_b = GUI_element('text_field',(120,70),(76,18),color_str(colors[0]))
    raw_rgb_b.restrictions = [False,None,None,False]
    red_slider = GUI_element('slider',(10,90),(255,18),colors[0][0])
    green_slider = GUI_element('slider',(10,122),(255,18),colors[0][1])
    blue_slider = GUI_element('slider',(10,154),(255,18),colors[0][2])
    original_colors = colors.copy()
    selecting_color = True
    
    while selecting_color:
        screen.fill((0,0,0))

        render_colors(screen,(2,22))
        clicked = save_b.handle(screen,mouse_data)
        if clicked == True:
            selecting_color = False
        clicked = cancel_b.handle(screen,mouse_data)
        if clicked == True:
            selecting_color = False
            colors = original_colors.copy()
        simple_text('raw RGB value:',(2,70))
        raw_rgb_b.element_data = color_str(colors[0])
        new_raw_value = raw_rgb_b.handle(screen,mouse_data)
        if in_color_range(new_raw_value,'rgb'):
            colors[0] = color_str(new_raw_value,True)
        simple_text('R\n\nG\n\nB',(2,94))
        red_slider.element_data = colors[0][0]/255
        green_slider.element_data = colors[0][1]/255
        blue_slider.element_data = colors[0][2]/255
        r = red_slider.handle(screen,mouse_data)*255
        g = green_slider.handle(screen,mouse_data)*255
        b = blue_slider.handle(screen,mouse_data)*255
        colors[0] = (int(r),int(g),int(b))

        mouse_data.update()
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    selecting_color = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_data.left_click = True
                    mouse_data.left_clicking = True
                if event.button == 2:
                    mouse_data.middle_click = True
                if event.button == 3:
                    mouse_data.right_click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_data.left_clicking = False

        pygame.display.update()
        mainClock.tick(60)
        last_frame = screen.copy()
        
    mouse_data.reset()

def save_file(path,extension,types):
    root = tk.Tk()
    root.withdraw()
    f = filedialog.asksaveasfile(initialdir=path,mode='w',defaultextension=extension,filetypes=types.copy())
    if f is None:
        return None
    else:
        return f.name

# Setup ------------------------------------------------------ #
global mouse_data
mouse_data = mouse_data_obj()
select_color_b = GUI_element('text_button',(2,2),(100,16),'select color')
save_to_palette_b = GUI_element('text_button',(2,66),(100,16),'save color')
import_palette_b = GUI_element('text_button',(2,86),(100,16),'import palette')
save_palette_b = GUI_element('text_button',(2,106),(100,16),'save palette')
canvas_size_b = GUI_element('text_field',(WINDOWWIDTH-4,20),(76,18),'32;32',shift_left=True)
add_layer_b = GUI_element('text_button',(4,WINDOWHEIGHT-125),(70,16),'add layer')
add_frame_b = GUI_element('text_button',(84,WINDOWHEIGHT-125),(70,16),'add frame')
animation_controls_b = GUI_element('image_button',(164,WINDOWHEIGHT-128),(16,18),play_img)
onion_skin_b = GUI_element('image_button',(360,WINDOWHEIGHT-128),(16,18),onion_img)
frame_pause_b = GUI_element('text_field',(300,WINDOWHEIGHT-125),(50,18),'6')
save_b = GUI_element('text_button',(160,2),(40,16),'save')
save_as_b = GUI_element('text_button',(210,2),(60,16),'save as')
export_b = GUI_element('text_button',(280,2),(50,16),'export')
load_b = GUI_element('text_button',(340,2),(40,16),'load')
canvas_size_b.restrictions = [False,None,None,False]
frame_pause_b.restrictions = [False,False,None,False]
#test_text_field = GUI_element('text_field',(2,60),(100,16),'sample text field')
#test_slider = GUI_element('slider',(2,80),(100,16),0)
#test_toggle = GUI_element('toggle',(2,100),(50,50),'sample toggle button')

global colors
colors = [(0,0,0),(255,255,255)]

palette = []
palette_drag = [False,0,None]
paletteR = pygame.Rect(0,126,137,218)

global last_frame
last_frame = screen.copy()

visible = False

global main_canvas
main_canvas = canvas(32,32)

canvas_drag = (0,0)
canvas_scroll = [200,100]
canvas_zoom = 2

animation_playing = False
animation_pause_time = 6
animation_timer = 0

onion_skin = False

frame_drag = [False,None] # active, origin

last_save = None

clipboard = None

global selecting
selecting = [False,[0,0]]
global selection
selection = [None,[0,0]] # sets to the selected image and coords
selection_drag = [False,[0,0]]

global ctrl
ctrl = False
global f_key
f_key = False
global s_key
s_key = False
global r_key
r_key = False

shift_key = False

global brush_size
brush_size = 1

global canvas_log, log_state
canvas_log = [] # log of canvas states - used for undos/redos
log_state = None # number in the log - None is for a new state nonexistent in the log
# Loop ------------------------------------------------------- #
while True:
    # Background --------------------------------------------- #
    screen.fill((0,0,0))
    # Run Animation ------------------------------------------ #
    if animation_playing == True:
        animation_timer += 1
        if animation_timer >= animation_pause_time:
            animation_timer = 0
            main_canvas.frame_num += 1
            if main_canvas.frame_num >= len(main_canvas.frames):
                main_canvas.frame_num = 0
    # Canvas ------------------------------------------------- #
    if log_state != None:
        main_canvas = canvas_log[log_state]
    main_canvas.render(screen,canvas_scroll,canvas_zoom)
    if onion_skin == True:
        main_canvas.frame_num -= 1
        main_canvas.render(screen,canvas_scroll,canvas_zoom,0.5)
        main_canvas.frame_num += 1
    main_canvas.handle_draws(canvas_scroll,canvas_zoom,mouse_data)
    if mouse_data.middle_click == True:
        canvas_drag = mouse_data.pos
    if mouse_data.middle_clicking == True:
        offset_x = mouse_data.pos[0]-canvas_drag[0]
        offset_y = mouse_data.pos[1]-canvas_drag[1]
        canvas_drag = mouse_data.pos
        canvas_scroll[0] += offset_x
        canvas_scroll[1] += offset_y
    # Selection ---------------------------------------------- #
    if selecting[0] == True:
        top_left = [selecting[1][0],selecting[1][1]]
        if main_canvas.raw_pos[0] < top_left[0]:
            top_left[0] = main_canvas.raw_pos[0]
        if main_canvas.raw_pos[1] < top_left[1]:
            top_left[1] = main_canvas.raw_pos[1]
        selection_size = [abs(selecting[1][0]-main_canvas.raw_pos[0]),abs(selecting[1][1]-main_canvas.raw_pos[1])]
        selection_rect = pygame.Rect(top_left[0],top_left[1],selection_size[0],selection_size[1])
        overlay = pygame.Surface((main_canvas.size_x,main_canvas.size_y))
        pygame.draw.rect(overlay,(0,34,64),selection_rect,1)
        overlay.set_colorkey((0,0,0))
        overlay.set_alpha(150)
        screen.blit(pygame.transform.scale(overlay,(main_canvas.size_x*canvas_zoom,main_canvas.size_y*canvas_zoom)),(canvas_scroll[0],canvas_scroll[1]))
    if selection[0] != None:
        screen.blit(pygame.transform.scale(selection[0],(selection_size[0]*canvas_zoom,selection_size[1]*canvas_zoom)),(selection[1][0]*canvas_zoom+canvas_scroll[0],selection[1][1]*canvas_zoom+canvas_scroll[1]))
        selection_rect = pygame.Rect(top_left[0],top_left[1],selection_size[0],selection_size[1])
        overlay = pygame.Surface((main_canvas.size_x,main_canvas.size_y))
        pygame.draw.rect(overlay,(0,34,64),selection_rect,1)
        overlay.set_colorkey((0,0,0))
        overlay.set_alpha(150)
        screen.blit(pygame.transform.scale(overlay,(main_canvas.size_x*canvas_zoom,main_canvas.size_y*canvas_zoom)),(canvas_scroll[0],canvas_scroll[1]))
        if mouse_data.left_click == True:
            selection_drag = [True,mouse_data.pos.copy()]
        if mouse_data.left_clicking == False:
            if selection_drag[0] == True:
                selection_drag[0] = False
                selection[0] = pygame.transform.scale(selection[0],selection_size)
        if selection_drag[0] == True:
            dif_x = int((mouse_data.pos[0]-selection_drag[1][0])/canvas_zoom)
            dif_y = int((mouse_data.pos[1]-selection_drag[1][1])/canvas_zoom)
            if dif_x != 0:
                selection_drag[1][0] = mouse_data.pos[0]
            if dif_y != 0:
                selection_drag[1][1] = mouse_data.pos[1]
            if r_key == False:
                top_left[0] += dif_x
                top_left[1] += dif_y
                selection[1] = top_left.copy()
            else:
                selection_size[0] += dif_x
                selection_size[1] += dif_y
    if mouse_data.right_click == True:
        if selection[0] != None:
            selection[0].set_colorkey(colors[1])
            main_canvas.frames[main_canvas.frame_num].layers[main_canvas.layer_num].image.blit(selection[0],selection[1])
            selection[0] = None
            mouse_data.right_clicking = False
    # Palette ------------------------------------------------ #
    screen.blit(color_select_img,(0,0))
    n = 0
    remove = None
    for color in palette:
        bgR = pygame.Rect(color[1]+4,color[2]+130,20,20)
        colorR = pygame.Rect(color[1]+6,color[2]+132,16,16)
        if bgR.collidepoint(mouse_data.pos):
            if mouse_data.left_click == True:
                palette_drag = [True,1,n]
            if mouse_data.middle_click == True:
                if palette_drag[0] == False:
                    remove = n
            if mouse_data.right_click == True:
                colors[1] = color[0]
        pygame.draw.rect(screen,(0,34,64),bgR)
        pygame.draw.rect(screen,color[0],colorR)
        n += 1
    if remove != None:
        palette.pop(remove)
    if palette_drag[0] == True:
        if palette_drag[1] > 10:
            if palette_drag[1] == 11:
                color_copy = palette[palette_drag[2]].copy()
                palette.pop(palette_drag[2])
                palette_drag[2] = -1
                palette.append(color_copy.copy())
            palette[palette_drag[2]][1] = mouse_data.pos[0]-14
            palette[palette_drag[2]][2] = mouse_data.pos[1]-140
            if palette[palette_drag[2]][1] < 0:
                palette[palette_drag[2]][1] = 0
            if palette[palette_drag[2]][1] > 104:
                palette[palette_drag[2]][1] = 104
            if palette[palette_drag[2]][2] < 0:
                palette[palette_drag[2]][2] = 0
            if palette[palette_drag[2]][2] > 190:
                palette[palette_drag[2]][2] = 190
        if mouse_data.left_clicking == False:
            if palette_drag[1] <= 10:
                colors[0] = palette[palette_drag[2]][0]
            palette_drag[1] = 0
            palette_drag[0] = False
        palette_drag[1] += 1
    # GUI ---------------------------------------------------- #
    canvas_size_b.element_data = str(main_canvas.size_x) + ';' + str(main_canvas.size_y)
    new_canvas_size = canvas_size_b.handle(screen,mouse_data)
    try:
        new_canvas_size = [int(new_canvas_size.split(';')[0]),int(new_canvas_size.split(';')[1])]
        if (new_canvas_size[0] != main_canvas.size_x) or (new_canvas_size[1] != main_canvas.size_y):
            main_canvas.resize(new_canvas_size[0],new_canvas_size[1])
            add_log_state()
    except:
        pass
    simple_text('brush_size: ' + str(brush_size),(WINDOWWIDTH-get_text_width('brush_size: ' + str(brush_size),1)*2-4,4))
    clicked = select_color_b.handle(screen,mouse_data)
    if clicked:
        select_color()
    clicked = save_to_palette_b.handle(screen,mouse_data)
    if clicked:
        palette.append([colors[0],0,0])
    clicked = import_palette_b.handle(screen,mouse_data)
    if clicked:
        mouse_data.reset()
        palette_find_path = read_f('save/palette_path')
        if os.path.exists(palette_find_path) != True:
            palette_find_path = ''
        Tk().withdraw()
        palette_path = filedialog.askopenfilename(initialdir=palette_find_path,title='Load Palette',filetypes=[('PNG or PXEP',('*.png','*.PNG','*.pxep'))])
        if palette_path not in ['',None]:
            base_path = palette_path.split('/')[:-1]
            file_type = palette_path.split('.')[-1]
            write_f('save/palette_path',str_sum(base_path,'/'))
            palette = []
            if file_type != 'pxep':
                color_list = get_image_colors(pygame.image.load(palette_path))
                x = 0
                y = 0
                for color in color_list:
                    palette.append([(color[0],color[1],color[2]),x,y])
                    x += 12
                    #y += 1
                    if x > 100:
                        x = 0
                        y += 22
                    if y > 190:
                        break
            else:
                f = open(palette_path,'r')
                dat = f.read()
                f.close()
                color_dat = dat.split('|')
                for color in color_dat:
                    if color != '':
                        color = color.split(';')
                        palette.append([(int(color[0]),int(color[1]),int(color[2])),int(color[3]),int(color[4])])

    clicked = save_palette_b.handle(screen,mouse_data)
    if clicked:
        mouse_data.reset()
        palette_find_path = read_f('save/palette_path')
        if os.path.exists(palette_find_path) != True:
            palette_find_path = ''
        Tk().withdraw()
        palette_path = filedialog.asksaveasfile(mode='w',initialdir=palette_find_path,title='Save Palette',defaultextension='pxep',filetypes=[('PXE palette','*.pxep')])
        if palette_path != None:
            palette_path = palette_path.name
            if palette_path not in ['',None]:
                base_path = palette_path.split('/')[:-1]
                write_f('save/palette_path',str_sum(base_path,'/'))
                write_str = ''
                for color in palette:
                    write_str += str(color[0][0]) + ';' + str(color[0][1]) + ';' + str(color[0][2]) + ';' + str(color[1]) + ';' + str(color[2]) + ';|'
                f = open(palette_path,'w')
                f.write(write_str)
                f.close()
    render_colors(screen,(2,20))
    # Animation / Layer GUI ---------------------------------- #
    bg_surf = pygame.Surface((WINDOWWIDTH,130))
    bg_surf.fill((0,17,32))
    screen.blit(bg_surf,(0,WINDOWHEIGHT-130))
    pygame.draw.line(screen,(0,34,64),(-4,WINDOWHEIGHT-130),(WINDOWWIDTH+4,WINDOWHEIGHT-130),2)
    clicked = onion_skin_b.handle(screen,mouse_data)
    if clicked:
        if onion_skin == False:
            onion_skin = True
        else:
            onion_skin = False
    simple_text('frame pause:',(200,WINDOWHEIGHT-125))
    new_frame_delay = frame_pause_b.handle(screen,mouse_data)
    try:
        new_frame_delay = int(new_frame_delay)
        animation_pause_time = new_frame_delay
    except:
        pass
    clicked = add_layer_b.handle(screen,mouse_data)
    if clicked:
        if len(main_canvas.frames[0].layers) < 4:
            add_log_state()
            for frame_obj in main_canvas.frames:
                frame_obj.layers.append(canvas_img(main_canvas.size_x,main_canvas.size_y))
    clicked = add_frame_b.handle(screen,mouse_data)
    if clicked:
        add_log_state()
        main_canvas.frames.insert(main_canvas.frame_num+1,main_canvas.frames[main_canvas.frame_num].copy())
        main_canvas.frame_num += 1
    clicked = animation_controls_b.handle(screen,mouse_data)
    if clicked:
        if animation_playing == True:
            animation_playing = False
            animation_controls_b.element_data = play_img
        else:
            animation_playing = True
            animation_controls_b.element_data = pause_img
    blank_surface = pygame.Surface((20,20))
    blank_surface.fill(colors[1])
    if frame_drag[0] == True:
        new_pos = int(mouse_data.pos[0]/24)-2
        if new_pos > len(main_canvas.frames):
            new_pos = len(main_canvas.frames)
        if new_pos < 0:
            new_pos = 0
        if (new_pos != frame_drag[1]) and (new_pos != frame_drag[1]+1):
            pygame.draw.line(screen,(112,240,77),((new_pos+2)*24-3,WINDOWHEIGHT-112),((new_pos+2)*24-3,WINDOWHEIGHT),2)
        if mouse_data.left_clicking == False:
            frame_drag[0] = False
            if (new_pos != frame_drag[1]) and (new_pos != frame_drag[1]+1):
                add_log_state()
                main_canvas.frames.insert(new_pos,main_canvas.frames[frame_drag[1]].copy())
                if new_pos < frame_drag[1]:
                    main_canvas.frames.pop(frame_drag[1]+1)
                    main_canvas.frame_num = new_pos
                else:
                    main_canvas.frames.pop(frame_drag[1])
                    main_canvas.frame_num = new_pos-1
    x = 2
    for frame_obj in main_canvas.frames:
        frame_rect = pygame.Rect(x*24,WINDOWHEIGHT-len(frame_obj.layers)*24,24,len(frame_obj.layers)*24)
        if frame_rect.collidepoint(mouse_data.pos):
            if mouse_data.left_click == True:
                frame_drag = [True,x-2]
        y = 1
        for image in frame_obj.layers:
            preview_img = pygame.transform.scale(image.image,(20,20))
            screen.blit(blank_surface,(x*24,WINDOWHEIGHT-y*24))
            screen.blit(preview_img,(x*24,WINDOWHEIGHT-y*24))
            preview_rect = pygame.Rect(x*24,WINDOWHEIGHT-y*24,20,20)
            if main_canvas.frame_num == x-2:
                bar_color = ((255,0,0))
                if main_canvas.layer_num == y-1:
                    bar_color = ((0,255,0))
                pygame.draw.line(screen,bar_color,(x*24,WINDOWHEIGHT-y*24+18),(x*24+19,WINDOWHEIGHT-y*24+18),2)
            if preview_rect.collidepoint(mouse_data.pos):
                if mouse_data.left_click == True:
                    mouse_data.left_click = False
                    main_canvas.layer_num = y-1
                    main_canvas.frame_num = x-2
                elif mouse_data.middle_click == True:
                    mouse_data.middle_click = False
                    if len(main_canvas.frames) > 1:
                        add_log_state()
                        main_canvas.frames.pop(x-2)
                        if main_canvas.frame_num >= len(main_canvas.frames):
                            main_canvas.frame_num = len(main_canvas.frames)-1
            if x == 2:
                delete_b = GUI_element('image_button',(4,WINDOWHEIGHT-y*24),(16,18),delete_img)
                opacity_b = GUI_element('image_button',(24,WINDOWHEIGHT-y*24),(16,18),opacity_img)
                clicked = delete_b.handle(screen,mouse_data)
                if clicked:
                    if len(main_canvas.frames[0].layers) > 1:
                        for frame_obj2 in main_canvas.frames:
                            add_log_state()
                            frame_obj2.layers.pop(y-1)
                            if main_canvas.layer_num >= len(frame_obj2.layers):
                                main_canvas.layer_num = len(frame_obj2.layers)-1
                clicked = opacity_b.handle(screen,mouse_data)
                if clicked:
                    new_opacity = enter_text(str(image.opacity),[False,False,None,False])
                    try:
                        new_opacity = int(new_opacity)
                        if new_opacity > 255:
                            new_opacity = 255
                        if new_opacity < 0:
                            new_opacity = 0
                        image.opacity = new_opacity
                    except:
                        pass
            y += 1
        x += 1
    # Export/Save GUI ---------------------------------------- #
    screen.blit(export_bg_img,(150,0))
    clicked = save_b.handle(screen,mouse_data)
    if clicked:
        if last_save == None:
            img_path = read_f('save/image_path')
            file_path = save_file(img_path,'.pxe',[('PXE file','*.pxe')])
            if file_path not in [None,'']:
                file_base_path = file_path.split('/')[:-1]
                file_base_path = str_sum(file_base_path,'/')
                write_f('save/image_path',file_base_path)
                main_canvas.prepare_for_pickle()
                pickle.dump(main_canvas,open(file_path,'wb'))
                last_save = file_path
        else:
            main_canvas.prepare_for_pickle()
            pickle.dump(main_canvas,open(last_save,'wb'))
    clicked = save_as_b.handle(screen,mouse_data)
    if clicked:
        img_path = read_f('save/image_path')
        file_path = save_file(img_path,'.pxe',[('PXE file','*.pxe')])
        if file_path not in [None,'']:
            file_base_path = file_path.split('/')[:-1]
            file_base_path = str_sum(file_base_path,'/')
            write_f('save/image_path',file_base_path)
            main_canvas.prepare_for_pickle()
            pickle.dump(main_canvas,open(file_path,'wb'))
            last_save = file_path
    clicked = export_b.handle(screen,mouse_data)
    if clicked:
        img_path = read_f('save/image_path')
        file_path = save_file(img_path,'.png',[('PNG/PNG Sequence','*.png')])
        if file_path not in [None,'']:
            file_base_path = file_path.split('/')[:-1]
            file_base_path = str_sum(file_base_path,'/')
            write_f('save/image_path',file_base_path)
            export_num = 0
            for frame_obj in main_canvas.frames:
                export_surface = pygame.Surface((main_canvas.size_x,main_canvas.size_y))
                export_surface.fill(colors[1])
                for layer in frame_obj.layers:
                    layer.image.set_alpha(layer.opacity)
                    export_surface.blit(layer.image,(0,0))
                if len(main_canvas.frames) != 1:
                    new_file_path = file_path.split('.')
                    new_file_path[-2] += str(export_num)
                    new_file_path = str_sum(new_file_path,'.',False)
                    pygame.image.save(export_surface,new_file_path)
                    print(new_file_path)
                    try:
                        os.remove(file_path)
                    except:
                        pass
                else:
                    pygame.image.save(export_surface,file_path)
                export_num += 1
    clicked = load_b.handle(screen,mouse_data)
    if clicked:
        img_path = read_f('save/image_path')
        if os.path.exists(img_path) != True:
            img_path = ''
        Tk().withdraw()
        file_path = filedialog.askopenfilename(initialdir=img_path,title='Load Project/Image',filetypes=[('PNG or PXE',('*.png','*.PNG','*.pxe'))])
        if file_path not in [None,'']:
            file_base_path = file_path.split('/')[:-1]
            file_base_path = str_sum(file_base_path,'/')
            write_f('save/image_path',file_base_path)
            if file_path.split('.')[-1] == 'pxe':
                main_canvas = pickle.load(open(file_path,'rb'))
                main_canvas.post_pickle_handling()
                last_save = None
                canvas_log = []
                log_state = None
            else:
                img = pygame.image.load(file_path).convert()
                main_canvas = canvas(img.get_width(),img.get_height())
                main_canvas.frames[0].layers[0].image = img.copy()
                last_save = None
                canvas_log = []
                log_state = None
    # Mouse Icon --------------------------------------------- #
    if f_key == True:
        screen.blit(floodfill_img,(mouse_data.pos[0]-22,mouse_data.pos[1]-18))
    elif ctrl == True:
        screen.blit(color_picker_img,(mouse_data.pos[0]-16,mouse_data.pos[1]-18))
    elif s_key == True:
        screen.blit(selection_img,(mouse_data.pos[0]-16,mouse_data.pos[1]-16))
    elif (r_key == True) and (selection[0] != None):
        screen.blit(selection_resize_img,(mouse_data.pos[0]-24,mouse_data.pos[1]-24))
    if selecting[0] == True:
        if mouse_data.left_clicking == False:
            selecting[0] = False
            selection = [clip.clip(main_canvas.frames[main_canvas.frame_num].layers[main_canvas.layer_num].image,top_left[0],top_left[1],selection_size[0],selection_size[1]),top_left.copy()]
            pygame.draw.rect(main_canvas.frames[main_canvas.frame_num].layers[main_canvas.layer_num].image,colors[1],selection_rect)
    if s_key == True:
        if selection[0] == None:
            if mouse_data.left_click == True:
                add_log_state()
                selecting = [True,main_canvas.raw_pos.copy()]
    # Input -------------------------------------------------- #
    mouse_data.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                main_canvas.frame_num += 1
                if main_canvas.frame_num >= len(main_canvas.frames):
                    main_canvas.frame_num = 0
            if event.key == K_LEFT:
                main_canvas.frame_num -= 1
                if main_canvas.frame_num < 0:
                    main_canvas.frame_num = len(main_canvas.frames)-1
            if event.key == K_LCTRL:
                ctrl = True
            if event.key == K_f:
                if selection[0] != None:
                    if shift_key == False:
                        selection[0] = pygame.transform.flip(selection[0],True,False)
                    else:
                        selection[0] = pygame.transform.flip(selection[0],False,True)
                f_key = True
            if event.key == K_s:
                s_key = True
            if event.key == K_r:
                r_key = True
            if event.key == K_LSHIFT:
                shift_key = True
            if ctrl == True:
                if event.key == K_x:
                    selection[0] = None
                if event.key == K_c:
                    if selection[0] != None:
                        clipboard = selection[0].copy()
                if event.key == K_v:
                    if clipboard != None:
                        if selection[0] == None:
                            add_log_state()
                            selection = [clipboard.copy(),[0,0]]
                            selection_size = [clipboard.get_width(),clipboard.get_height()]
                            top_left = [0,0]
        if event.type == KEYUP:
            if event.key == K_LCTRL:
                ctrl = False
            if event.key == K_f:
                f_key = False
            if ctrl == True:
                if event.key == K_z:
                    undo()
                if event.key == K_y:
                    redo()
            if event.key == K_s:
                s_key = False
            if event.key == K_r:
                r_key = False
            if event.key == K_LSHIFT:
                shift_key = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_data.left_click = True
                mouse_data.left_clicking = True
            if event.button == 2:
                mouse_data.middle_click = True
                mouse_data.middle_clicking = True
            if event.button == 3:
                mouse_data.right_click = True
                mouse_data.right_clicking = True
            if event.button == 4:
                if ctrl == False:
                    canvas_zoom += 1
                else:
                    brush_size += 1
            if event.button == 5:
                if ctrl == False:
                    canvas_zoom -= 1
                    if canvas_zoom < 1:
                        canvas_zoom = 1
                else:
                    brush_size -= 1
                    if brush_size < 1:
                        brush_size = 1
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                mouse_data.left_clicking = False
            if event.button == 2:
                mouse_data.middle_clicking = False
            if event.button == 3:
                mouse_data.right_clicking = False
    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)
    last_frame = screen.copy()
    
