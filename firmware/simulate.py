"""Print wheel speeds for a few example commands."""
from drive_logic import DriveController, mix


def drive_example():
    for label, axes in [('Forward', (1, 0, 0)),
                        ('Sideways', (0, 1, 0)),
                        ('Turn', (0, 0, 1))]:
        print(label, mix(*axes))

    drive = DriveController()
    command = dict(cmd='drive', armed=True, resume=True, vx=.5, vy=0, wz=0)
    drive.receive(command, 0)
    print('Drive:', drive.output(0))
    print('After timeout:', drive.output(401))
    print('Desktop only: no motors are connected.')


if __name__ == "__main__":
    drive_example()
