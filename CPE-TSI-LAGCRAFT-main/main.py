from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
import random
from Consts import *

def randomneg():
    return 0 if random.randrange(0,2) == 0 else -1

def main():
    viewer = ViewerGL()

    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.translation.z = 7
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    # Generation de Steve
    m = Mesh.load_obj('objects/Steve.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([1, 2, 1, 1]))
    tr = Transformation3D()
    tr.translation.y = 10 # -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = 25
    tr.translation.x = 25
    tr.rotation_center.z = 0.2
    
    texture = glutils.load_texture('objects/Steve_texture.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)



    # Generation du sol
    m = Mesh()
    p0, p1, p2, p3 = [-MAP_SIZE, 0, -MAP_SIZE], [MAP_SIZE, 0, -MAP_SIZE], [MAP_SIZE, 0, MAP_SIZE], [-MAP_SIZE, 0, MAP_SIZE]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('objects/Grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D(),name="sol", type="sol", scale=[MAP_SIZE*2,0.1,MAP_SIZE*2])
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 = [-MAP_SIZE, 0, -MAP_SIZE], [MAP_SIZE, 0, -MAP_SIZE], [MAP_SIZE, 0, MAP_SIZE], [-MAP_SIZE, 0, MAP_SIZE]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('objects/Grass.jpg')
    tr = Transformation3D()
    tr.translation.y = -10
    tr.translation.z = 0
    tr.translation.x = 0
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr,name="sol", type="sol", scale=[MAP_SIZE*2,10,MAP_SIZE*2])
    viewer.add_object(o)

    # Generation de la map
    relief = []
    center = [random.randrange(5,MAP_SIZE) * randomneg(),random.randrange(5,MAP_SIZE) * randomneg()]
    size = random.randrange(4,15)
    viewer = add_relief(viewer, program3d_id, size=size, center=center)
    relief.append( [center,size])
    for i in range(0,N_RELIEF):
        for o_center, o_size in relief:
            isGood= False # Eviter que deux relief fusionne
            while not isGood:
                center = [random.randrange(5,MAP_SIZE) * randomneg(),random.randrange(5,MAP_SIZE) * randomneg()]
                size = random.randrange(4,15)
                min_a = np.array(center) - np.array([size+1,size+1])/2
                max_a = np.array(center) + np.array([size+1,size+1])/2
                min_o = np.array(o_center) - np.array([o_size,o_size])/2
                max_o = np.array(o_center) + np.array([o_size,o_size])/2
                min_point = np.maximum(min_o, min_a)
                max_point = np.minimum(max_o, max_a)
                intersection = max_point-min_point
                if not (intersection[0] > 0 and  intersection[1] > 0):      
                    isGood = True
        
        viewer = add_relief(viewer, program3d_id, size=size, center=center)
        relief.append( [center,size])
    for i in range(0,random.randrange(3,N_MAX_TREE)):
        center = [random.randrange(5,MAP_SIZE) * randomneg(),random.randrange(5,MAP_SIZE) * randomneg()]
        viewer = add_tree(viewer, program3d_id, center=center)

    '''
    vao = Text.initalize_geometry()
    texture = glutils.load_texture('objects/font.jpg')
    o = Text('Hello', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 10, programGUI_id, texture)
    viewer.add_object(o)
    o = Text(GAME_NAME, np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    '''

    # Generation du ciel et des murs
    viewer = add_skywall(viewer,program3d_id)

  


    
    viewer.run()


def add_relief(viewer : ViewerGL, program3d_id, size : int, center: list = [0,0],block_type : str ="Grass"):
    m = Mesh.load_obj('objects/GrassBlock.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
    texture = glutils.load_texture(f'objects/{block_type}Block_texture.png')
    for y in range(1,5,2):
        for x in range(y,size+1-y*2,2):
            for z in range(0,size+1-y*2,2):
                tr = Transformation3D()
                tr.translation.y = y
                tr.translation.z = center[1] + z
                tr.translation.x = center[0] + x
                tr.rotation_center.z = 0.2
                o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr,scale = [1,1,1],name=f"block_{x}-{y}-{z}",type="block")
                viewer.add_object(o)
    return viewer

def add_tree(viewer : ViewerGL, program3d_id, center: list = [0,0], height=10, size=3):
    m = Mesh.load_obj('objects/GrassBlock.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
    texture = glutils.load_texture(f'objects/WoodBlock_texture.png')
    for y in range(1,height,2):
        tr = Transformation3D()
        tr.translation.y = y
        tr.translation.z = center[1] 
        tr.translation.x = center[0] 
        tr.rotation_center.z = 0.2 
        o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr,scale = [1,1,1],name=f"block_{center[0]}-{y}-{center[1]}",type="block")
        viewer.add_object(o)

    m = Mesh.load_obj('objects/GrassBlock.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
    texture = glutils.load_texture(f'objects/HerbeBlock_texture.png')  
    for y in range(height,height+7,2):
        for x in range(-size,size,2):
            for z in range(-size,size,2):
                tr = Transformation3D()
                tr.translation.y = y
                tr.translation.z = center[1] + z
                tr.translation.x = center[0] + x
                tr.rotation_center.z = 0.2
                o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr,scale = [1,1,1],name=f"block_{x}-{y}-{z}",type="block")
                viewer.add_object(o)
    return viewer

def add_skywall(viewer : ViewerGL, program3d_id):
    m = Mesh()
    p0, p1, p2, p3 = [-MAP_SIZE, 0, -MAP_SIZE], [-MAP_SIZE, 20, -MAP_SIZE], [MAP_SIZE, 20, -MAP_SIZE], [MAP_SIZE, 0, -MAP_SIZE]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('objects/LAGCraft_REVERSE.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D(),name="sol")
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 =  [MAP_SIZE, 0, -MAP_SIZE], [MAP_SIZE, 20, -MAP_SIZE],[MAP_SIZE, 20, MAP_SIZE], [MAP_SIZE, 0, MAP_SIZE]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('objects/LAGCraft_REVERSE.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D(),name="sol")
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 = [MAP_SIZE, 0, MAP_SIZE], [MAP_SIZE, 20, MAP_SIZE], [-MAP_SIZE, 20, MAP_SIZE], [-MAP_SIZE, 0, MAP_SIZE]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('objects/LAGCraft_REVERSE.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D(),name="sol")
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 = [-MAP_SIZE, 0, MAP_SIZE], [-MAP_SIZE, 20, MAP_SIZE], [-MAP_SIZE, 20, -MAP_SIZE], [-MAP_SIZE, 0, -MAP_SIZE]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('objects/LAGCraft_REVERSE.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D(),name="sol")
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 = [-MAP_SIZE, 20, -MAP_SIZE], [-MAP_SIZE, 20, MAP_SIZE], [MAP_SIZE, 20, MAP_SIZE], [MAP_SIZE, 20, -MAP_SIZE]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('objects/sky.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D(),name="sol")
    viewer.add_object(o)
    
    return viewer

if __name__ == '__main__':
    main()

