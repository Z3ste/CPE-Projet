#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
from Consts import *
# from threading import Thread
import numpy as np
# from time import sleep
# import time

from mesh import Mesh
from cpe3d import Transformation3D, Object3D
import glutils

frame_count = 0
start_time = 0

class ViewerGL:
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_NAME, None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.set_input_mode(self.window, glfw.RAW_MOUSE_MOTION, glfw.TRUE)
        self.old_pos_x = 0     
        self.old_pos_y = 0   
        glfw.set_cursor_pos_callback(self.window, self.cursor_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_callback)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.touch = {}
        
        self.isBuilding = False
        self.listBuildingTextures = ["Sand","Grass","Water","Lave","Tnt","Blé","Table","Wood","Herbe"]
        self.buildingTexture = 0
        self.isDestructing = False

        self.isJumping = False
        self.frame = glfw.get_time()
        self.time_jump = 0


    def initiateBuildingCalc(self):
        m = Mesh.load_obj('objects/GrassBlock.obj')
        m.normalize()
        m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 0]))
        tr = Transformation3D()
        tr.translation.y = 0
        tr.translation.z = 0
        tr.translation.x = 0
        tr.rotation_center.z = 0
        
        texture = glutils.load_texture('objects/CalcBlock_texture.png')
        self.buildingObject = Object3D(m.load_to_gpu(), m.get_nb_triangles(), self.objs[0].program, texture, tr,type="block", scale=[0.25,0.25,0.25])

        texture = glutils.load_texture('objects/RmBlock_texture.png')
        self.destructingObject = Object3D(m.load_to_gpu(), m.get_nb_triangles(), self.objs[0].program, texture, tr,type="block", scale=[0.25,0.25,0.25])

        self.refreshBuildingObjectPreview()

 

    def run(self):
        # boucle d'affichage
        counter = 0
        self.initiateBuildingCalc()
        isFalling = False
        isJumping = False
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            # _start_time = time.time()
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            self.update_key()

            dt = glfw.get_time()-self.frame
            self.frame = glfw.get_time()

            self.time_jump-= dt
            if(self.time_jump > 0):
                if not isJumping:
                    jumpEndTime = glfw.get_time() + self.time_jump
                    isJumping = True
                if jumpEndTime-self.frame > 0: # au cas où
                    self.objs[0].transformation.translation.y += 8*(jumpEndTime-self.frame)**2
            
            elif not isFalling and not self.check_collsion(self.objs[0].transformation.translation - [0,dt*3,0]):
                if isJumping: isJumping = False
                isFalling = True
                fallStartTime = glfw.get_time()
                
            elif isFalling and not self.check_collsion(self.objs[0].transformation.translation - [0,(self.frame-fallStartTime)**2 + 0.3,0]):
                self.objs[0].transformation.translation.y -= (self.frame-fallStartTime)**2 + 0.3
            else:
                isFalling = False
                isJumping = False
            
            for obj in self.objs:
                GL.glUseProgram(obj.program)
                obj.draw()
            
            if self.isBuilding:
                self.refreshBuildingCalc()
                GL.glUseProgram(self.buildingObject.program)
                self.buildingObject.draw()
                self.previewbuildingObject.draw()
            
            if self.isDestructing:
                self.refreshDeletingCalc()
                GL.glUseProgram(self.destructingObject.program)
                self.destructingObject.draw()

            self.update_camera(self.objs[0].program)
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()


    
    def add_object(self, obj : Object3D):
        self.objs.append(obj)

    def set_camera(self, cam : Object3D):
        self.cam = cam

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    
    ##########################################################################################################
    #
    # Gestion des evenements utilisateurs (souris/clavier)
    #
    ##########################################################################################################    
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        if key == glfw.KEY_SPACE and action == glfw.PRESS and self.time_jump <= 0:
            self.time_jump = 0.5
        self.touch[key] = action

    def update_key(self):
        if glfw.KEY_W in self.touch and self.touch[glfw.KEY_W] > 0:
            self.avancer("avant",HERO_SPEED)
        if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0:
            self.avancer("arriere",HERO_SPEED)
        if glfw.KEY_A in self.touch and self.touch[glfw.KEY_A] > 0:
            self.avancer("gauche",HERO_SPEED)
        if glfw.KEY_D in self.touch and self.touch[glfw.KEY_D] > 0:
            self.avancer("droite",HERO_SPEED)
        if glfw.KEY_T in self.touch and self.touch[glfw.KEY_T] > 0: # Debug
            self.isBuilding = not self.isBuilding
            self.isDestructing = False
        if glfw.KEY_R in self.touch and self.touch[glfw.KEY_R] > 0: # Debug
            self.isDestructing = not self.isDestructing
            self.isBuilding = False  
        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
            self.buildingTexture = (self.buildingTexture + 1) % len(self.listBuildingTextures)
            self.refreshBuildingObjectPreview()
        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
            self.buildingTexture = (self.buildingTexture + 1) % len(self.listBuildingTextures)
            self.refreshBuildingObjectPreview()

        if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.1
        if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1
        if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1


    def mouse_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and self.isBuilding:
            pos = [self.cam.transformation.translation[0]+1, self.cam.transformation.translation[1], self.cam.transformation.translation[2]+2]
            self.add_block(pos)
        if button == glfw.MOUSE_BUTTON_LEFT and self.isDestructing:
            self.remove_bloc()

    def cursor_callback(self, arg1, pos_x, pos_y):
        if self.old_pos_x - pos_x > 0:
            self.rotation(-0.07)
            #self.refraichir_cam()
        elif self.old_pos_x - pos_x < 0:
            self.rotation(0.07)
            #self.refraichir_cam()
        if self.old_pos_y - pos_y > 0:
                self.rotation(-0.1,'y')
        elif self.old_pos_y - pos_y < 0:
            self.rotation(0.1,'y')       
        self.refresh_cam_pos()
        self.old_pos_x, self.old_pos_y = pos_x, pos_y


    ##########################################################################################################
    #
    # Gestion des deplacements du personnage (translation/rotation)
    #
    ##########################################################################################################

    def rotation(self,angle,axe='x'):
        if axe == 'x':
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += angle
        else:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += angle
    
    def avancer(self,direction : str,speed : int):
        if direction == "arriere":
            new_coord = self.objs[0].transformation.translation + \
    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, speed]))
        if direction == "avant":
            new_coord = self.objs[0].transformation.translation - \
    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, speed]))
        if direction == "gauche":
            new_coord = self.objs[0].transformation.translation - \
    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([speed, 0, 0]))
        if direction == "droite":
            new_coord = self.objs[0].transformation.translation + \
    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([speed, 0, 0]))
        if not self.check_collsion(new_coord):
            self.objs[0].transformation.translation = new_coord
        self.refresh_cam_pos()    
    
    def check_collsion(self,coords_player : list) -> bool:
        scale_player = np.array([2.2,2,2.2])
        coords_player = coords_player - [0,1,0]
        for block in self.objs[1:]: # objs[0] et objs[1] sont reservé pour le sol et le player
            if (block.type != "block") and (block.type != "sol"):
                continue
            
            coords_block = np.array(block.transformation.translation)
            
            min_player = coords_player - scale_player/2
            max_player = coords_player + scale_player/2

            min_block = coords_block - np.array(block.scale)/2
            max_block = coords_block + np.array(block.scale)/2

            min_point = np.maximum(min_player, min_block)
            max_point = np.minimum(max_player, max_block)

            intersection = max_point-min_point
            if intersection[0] > 0 and  intersection[1] > 0 and  intersection[2] > 0:
                #print(f"{block.name} intersaction")
                return True
        return False

    def refresh_cam_pos(self):
        self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
        self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 2, POS_CAMERA*-1])

    ##########################################################################################################
    #
    # Partie Construction (Pose de bloc/ Destruction de bloc)
    #
    ##########################################################################################################


    def refreshBuildingObjectPreview(self):
        '''
        Change la texture du bloc de prévisualisation
        '''
        m = Mesh.load_obj('objects/GrassBlock.obj')
        m.normalize()
        m.apply_matrix(pyrr.matrix44.create_from_scale([0.1, 0.1, 0.1, 0]))
        tr = Transformation3D()
        tr.translation.y = 0
        tr.translation.z = 0
        tr.translation.x = 0
        tr.rotation_center.z = 0
        
        texture = glutils.load_texture(f'objects/{self.listBuildingTextures[self.buildingTexture]}Block_texture.png')
        self.previewbuildingObject = Object3D(m.load_to_gpu(), m.get_nb_triangles(), self.objs[0].program, texture, tr,type="block", scale=[0.25,0.25,0.25])

    def refreshDeletingCalc(self):
        '''
        Rafraichis la position/l'orientation du bloc de destruction (rouge)
        '''
        # Refraichis la position du block indiquant la position des blocs qui vont être posées
        self.destructingObject.transformation.rotation_center  = self.objs[0].transformation.rotation_center.copy()
        self.destructingObject.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.destructingObject.transformation.translation = self.objs[0].transformation.translation + \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.destructingObject.transformation.rotation_euler), pyrr.Vector3([0, -1, -3]))


    def refreshBuildingCalc(self):
        '''
        Rafraichis la position/l'orientation du bloc de création (vert) et du bloc de prévisualisation
        '''
        # Refraichis la position du block indiquant la position des blocs qui vont être posées
        self.buildingObject.transformation.rotation_center  = self.objs[0].transformation.rotation_center.copy()
        self.buildingObject.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.buildingObject.transformation.translation = self.objs[0].transformation.translation + \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.buildingObject.transformation.rotation_euler), pyrr.Vector3([0, -1, -3]))

        # Affiche en bas de l'écran le type de block qui va être posé
        self.previewbuildingObject.transformation.rotation_center  = self.objs[0].transformation.rotation_center.copy()
        self.previewbuildingObject.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.previewbuildingObject.transformation.translation = self.objs[0].transformation.translation + \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.buildingObject.transformation.rotation_euler), pyrr.Vector3([0, 0, 6]))

    def add_block(self, pos : list):
        '''
        Ajouter un bloc
        '''
        m = Mesh.load_obj('objects/GrassBlock.obj')
        m.normalize()
        m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 0]))
        tr = Transformation3D()
        tr.translation.y = 0
        tr.translation.z = 0
        tr.translation.x = 0
        tr.rotation_center.z = 0
        
        texture = glutils.load_texture(f'objects/{self.listBuildingTextures[self.buildingTexture]}Block_texture.png')
        o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), self.objs[0].program, texture, tr,type="block", scale=[0.25,0.25,0.25])
        
        o.transformation.rotation_center  = self.objs[0].transformation.rotation_center.copy()
        o.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        o.transformation.translation = self.objs[0].transformation.translation + \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(o.transformation.rotation_euler), pyrr.Vector3([0, -1, -3]))

        self.add_object(o)

    def remove_bloc(self):
        '''
        Ajouter un bloc
        '''
        scale_calc = np.array([2,2,2])
        coord_calc = self.destructingObject.transformation.translation
        for id_block in range(0,len(self.objs[1:])): # objs[0] et objs[1] sont reservé pour le sol et le player
            if (self.objs[id_block].type != "block"):
                continue
            
            coords_block = np.array(self.objs[id_block].transformation.translation)
            
            min_player = coord_calc - scale_calc/2
            max_player = coord_calc + scale_calc/2

            min_block = coords_block - np.array(self.objs[id_block].scale)/2
            max_block = coords_block + np.array(self.objs[id_block].scale)/2

            min_point = np.maximum(min_player, min_block)
            max_point = np.minimum(max_player, max_block)

            intersection = max_point-min_point
            if intersection[0] > 0 and  intersection[1] > 0 and  intersection[2] > 0:
                del self.objs[id_block]
                break