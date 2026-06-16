import torch
import numpy as np

class QuadDynamics:
    def __init__(self, dt=0.01, mass=1.0, arm_length=0.2, inertia=0.01):
        self.dt = dt
        self.mass = mass
        self.arm = arm_length
        self.I = torch.eye(3) * inertia
        self.g = 9.81
        self.kf = 1e-5
        self.km = 1e-6

    def motor_mixing(self, motor_thrusts):
        f1, f2, f3, f4 = motor_thrusts
        thrust = self.kf * (f1 + f2 + f3 + f4)
        tau_x = self.kf * self.arm * (f2 - f4)
        tau_y = self.kf * self.arm * (f3 - f1)
        tau_z = self.km * (f1 - f2 + f3 - f4)
        return thrust, torch.tensor([tau_x, tau_y, tau_z])

    def compute_ego_motion(self, state, motor_thrusts):
        pos, vel, quat, omega = state
        thrust, torques = self.motor_mixing(motor_thrusts)
        R = self._quat_to_rot(quat)
        accel = torch.tensor([0.0, 0.0, -self.g]) + R @ torch.tensor([0.0, 0.0, thrust / self.mass])
        ang_accel = torch.linalg.solve(self.I, torques - torch.linalg.cross(omega, self.I @ omega, dim=-1))
        return torch.cat([vel, ang_accel])

    def step(self, state, motor_thrusts):
        pos, vel, quat, omega = state
        accel = self.compute_ego_motion(state, motor_thrusts)
        new_vel = vel + accel[:3] * self.dt
        new_pos = pos + vel * self.dt
        new_omega = omega + accel[3:] * self.dt
        dq = 0.5 * self._quat_multiply(quat, torch.tensor([0, *new_omega]))
        new_quat = quat + dq * self.dt
        new_quat = new_quat / new_quat.norm()
        return (new_pos, new_vel, new_quat, new_omega)

    @staticmethod
    def _quat_to_rot(q):
        qw, qx, qy, qz = q
        return torch.tensor([
            [1 - 2*(qy**2 + qz**2), 2*(qx*qy - qz*qw), 2*(qx*qz + qy*qw)],
            [2*(qx*qy + qz*qw), 1 - 2*(qx**2 + qz**2), 2*(qy*qz - qx*qw)],
            [2*(qx*qz - qy*qw), 2*(qy*qz + qx*qw), 1 - 2*(qx**2 + qy**2)],
        ])

    @staticmethod
    def _quat_multiply(q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        return torch.tensor([
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2,
        ])
