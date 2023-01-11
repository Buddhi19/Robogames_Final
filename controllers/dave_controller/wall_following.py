from dave_lib import SENSOR_UNIT_VECTORS, Dave
import numpy as np

DISTANCE_TO_PS5 = 0.031
DISTANCE_TO_PS6 = 0.033
AVERAGE_RADIUS = np.mean([DISTANCE_TO_PS5, DISTANCE_TO_PS6])
V=3 #maximum velocity


def simple_left_wall_following(dave):
    left_wall_distance = dave.wall_dis[5]
    left_up_wall_distance = dave.wall_dis[6]
    forward_wall0_distance = dave.wall_dis[0]
    forward_wall7_distance = dave.wall_dis[7]

    if forward_wall0_distance <= 0.04 or forward_wall7_distance <= 0.04:
        dave.simple_turn_right(6.28)
    else:
        if left_wall_distance <= 0.06:
            if left_up_wall_distance >= 0.01:
                dave.simple_forward(6.28)
            else:
                dave.simple_turn_right(6.28)
        elif left_wall_distance > 0.06 and left_up_wall_distance > 0.06:
            dave.simple_turn_left(6.28)
        else:
            dave.simple_forward(6.28)

#sensor_1=sensors 5 or 2
#sensor_2=sensors 6 or 1
def calculate_angle_wall_following(dave,sensor_1,sensor_2):
    wall_distance_from_sensor1 = dave.wall_dis[sensor_1]+DISTANCE_TO_PS5
    wall_distance_from_sensor2 = dave.wall_dis[sensor_2]+DISTANCE_TO_PS6
    v5 = wall_distance_from_sensor1*SENSOR_UNIT_VECTORS[sensor_1]
    v6 = wall_distance_from_sensor2*SENSOR_UNIT_VECTORS[sensor_2]
    difference = v6-v5
    angle = -np.arctan2(difference[1], difference[0])
    return(angle)


def calculate_perpendicular_distance_wall_following(dave,sensor_1,sensor_2):
    wall_distance_from_sensor1 = dave.wall_dis[sensor_1]+DISTANCE_TO_PS5
    wall_distance_from_sensor2 = dave.wall_dis[sensor_2]+DISTANCE_TO_PS6
    v5 = wall_distance_from_sensor1*SENSOR_UNIT_VECTORS[sensor_1]
    v6 = wall_distance_from_sensor2*SENSOR_UNIT_VECTORS[sensor_2]
    dot_product_v5_v6 = np.dot(v5.flatten(), v6.flatten())
    lamba = (np.linalg.norm(v5)**2-dot_product_v5_v6) / \
        (np.linalg.norm(v6)**2-dot_product_v5_v6)
    print(lamba)
    perpendicular_distance_vector = (v5+lamba*v6)/(lamba+1)
    perpendicular_distance = np.linalg.norm(perpendicular_distance_vector)
    return(perpendicular_distance-AVERAGE_RADIUS)

def defining_equation(dave: Dave,sensor_1,sensor_2):
    if dave.wall_dis[sensor_1] <= 100 and dave.wall_dis[sensor_2] <= 100:
        alpha = 2
        beta = -1
        gamma = 3
        n_angle = calculate_angle_wall_following(dave,sensor_1,sensor_2)/np.pi*2
        n_distance = calculate_perpendicular_distance_wall_following(
            dave,sensor_1,sensor_2)/0.07
        error = alpha*n_angle + beta*n_distance
        omega = gamma*error
        print(f"{n_angle=} {n_distance=} {error=} {omega=}")
        return omega
    if dave.wall_dis[sensor_1] > 100 and dave.wall_dis[sensor_2] > 100:
        return -V
    return 0

def going_towards_a_corner(dave):
    if dave.wall_dis[0] <= 0.06 and dave.wall_dis[1] <= 0.06 and dave.wall_dis[7] <= 0.06 and dave.wall_dis[6] <= 0.06:
        return True
    if dave.wall_dis[0] <= 0.06 and dave.wall_dis[1] <= 0.06 and dave.wall_dis[7] <= 0.06:
        return True
    if dave.wall_dis[0] <= 0.06 and dave.wall_dis[7] <= 0.06 and dave.wall_dis[6] <= 0.06:
        return True
    return False

def attempt2_left_wall_following(dave: Dave):
    if going_towards_a_corner(dave):
        dave.simple_turn_right(V)
    else:
        omega=defining_equation(dave,5,6)
        lv = V+omega
        rv = V-omega
        dave.set_velcoity(lv, rv)

    
def attempt2_right_wall_following(dave: Dave):
    omega=defining_equation(dave,2,1)
    lv = V+omega
    rv = V-omega
    dave.set_velcoity(lv, rv)

