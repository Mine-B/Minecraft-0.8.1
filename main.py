from scene import Scene
import taichi as ti
from taichi.math import *

day = False
scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-0.85, (1.0, 1.0, 1.0))
scene.set_background_color((0.5, 0.5, 0.4) if day else (0.01, 0.01, 0.02))
scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6) if day else (0.1, 0.1, 0.2))

@ti.func
def build_tree(location, texture, color):
    for z in ti.ndrange((0, 5)):
        scene.set_voxel(vec3(location[0], location[1] + z, location[2]), 1, vec3(0.35, 0.09, 0.27))#木头
    for x, y, z in ti.ndrange((-2, 3), (-2, 3), (3, 5)):
        if not (x == -2 and y == -2 and z == 4):
            scene.set_voxel(vec3(location[0] + x, location[1] + z, location[2] + y), texture, color)
    for x, y, z in ti.ndrange((-1, 2), (-1, 2), (5, 7)):
        if not (x == 1 and y == 1 and z == 6):
            scene.set_voxel(vec3(location[0] + x, location[1] + z, location[2] + y), texture, color)

@ti.func
def steve(location):
    for foot, height in ti.ndrange((0, 2), (0, 2)):
        scene.set_voxel(vec3(location[0] + foot, location[1] + height, location[2]), 1, vec3(0.00, 0.47, 1.00))
    for body, height in ti.ndrange((0, 2), (2, 4)):
        scene.set_voxel(vec3(location[0] + body, location[1] + height, location[2]), 1, vec3(0.00, 0.70, 1.00))
    for height in ti.ndrange((2, 4)):
        scene.set_voxel(vec3(location[0] - 1, location[1] + height, location[2]), 1, vec3(1.00, 0.67, 0.35))
        scene.set_voxel(vec3(location[0] + 2, location[1] + height, location[2]), 1, vec3(1.00, 0.67, 0.35))
    scene.set_voxel(vec3(location[0], location[1] + 4, location[2]), 1, vec3(1.00, 0.67, 0.35))
    scene.set_voxel(vec3(location[0] + 1, location[1] + 4, location[2]), 1, vec3(1.00, 0.67, 0.35))
    scene.set_voxel(vec3(location[0], location[1] + 5, location[2]), 1, vec3(0.61, 0.30, 0.00))
    scene.set_voxel(vec3(location[0] + 1, location[1] + 5, location[2]), 1, vec3(0.61, 0.30, 0.00))

@ti.func
def wave():
    ti.loop_config(serialize=True)
    light_count = 50
    tree_count = 20
    min_height = -64
    for i, j, k in ti.ndrange((-64, 64), (-64, 64), (-64, 64)):
        h = 4 * ti.sin(ti.cast(i - 64, ti.f32) / (64 * 4) * 3.14) * ti.sin(ti.cast(j + 64, ti.f32) / (64 * 4) * 3.14) - 50
        min_height = min(ti.cast(h, ti.i32), min_height)
        if k < h:#wave()
            scene.set_voxel(vec3(i, k, j), 1, vec3(0.10, 0.44, 0.24))#0.33, 0.71, 0.1
        elif -64 < k < -52:#lake
            scene.set_voxel(vec3(i, k, j), 1, vec3(0.26, ((ti.random(ti.i32) % 50) + 100) / 255, 1.00))
        elif h <= k < h + 1:
            if i == 10 and j == 10:
                steve((i, k, j))
            if light_count >= 0 and ti.random(ti.i32) % 100000 >= 99650:#light block
                scene.set_voxel(vec3(i, k, j), 2, vec3(ti.random(ti.f32), ti.random(ti.f32), ti.random(ti.f32)))
                light_count -= 1
            if tree_count >= 0 and i % 15 == 0 and j % 15 == 0 and -60 < i < 60 and -60 < j < 60:#tree
                build_tree((i + ((ti.random(ti.i32) % 10) - 5) , h, j + ((ti.random(ti.i32) % 10) - 5)), 1, vec3(0.33, 0.71, 0.1))
            # if i == 0 and j == 0:
            #     build_tree((i, h, j), 1, vec3(1, 0.76, 0))
            # elif i == 23 and j == 25:
            #     build_tree((i, h, j), 1, vec3(1, 0.76, 0))
            # elif i == 15 and j == 12:
            #     build_tree((i, h, j), 1, vec3(1, 0.76, 0))

@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    # scene.set_voxel(vec3(0, 0, 0), 2, vec3(0.9, 0.1, 0.1))
    wave()


initialize_voxels()

scene.finish()
