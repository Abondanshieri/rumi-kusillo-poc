import math

# Let's compute Unreal FQuat from Rotator(Pitch=0, Yaw=0, Roll=90)
# Unreal Rotator order: Roll around X, Pitch around Y, Yaw around Z
# For Pitch=0, Yaw=0, Roll=90:
# Quat = (sin(45), 0, 0, cos(45)) = (0.7071, 0, 0, 0.7071)
# Now rotate vector V = (0, 0, 10):
# q * (0, 0, 10) * q^-1:
# Let's do standard quaternion vector rotation:
# v' = v + 2 * r x (r x v + w * v)
# r = (0.7071, 0, 0), w = 0.7071
# r x v = (0.7071, 0, 0) x (0, 0, 10) = (0, -7.071, 0)
# r x v + w * v = (0, -7.071, 7.071)
# r x (...) = (0.7071, 0, 0) x (0, -7.071, 7.071) = (0, -5, -5)
# 2 * (...) = (0, -10, -10)
# v + (...) = (0, 0, 10) + (0, -10, -10) = (0, -10, 0)!
# THE RESULT IS (0, -10, 0)!

print("V=(0, 0, 10) rotated by Roll=90 -> (X=0, Y=-10, Z=0)!")
