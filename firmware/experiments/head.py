"""Try two head angles on a computer. All angles are in degrees."""


def head_angles(current, pan, tilt, command_age_ms):
    if not 0 <= command_age_ms <= 400:
        return current
    return max(-180, min(180, pan)), max(-30, min(30, tilt))


if __name__ == "__main__":
    position = head_angles((0, 0), 20, 45, 0)
    print("Tilt limited to 30 degrees:", position)
    print("Late command holds position:", head_angles(position, 0, 0, 401))
