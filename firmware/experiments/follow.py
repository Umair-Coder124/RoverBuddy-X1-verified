"""Try a follow decision with pretend camera and distance readings."""


def follow_action(person_visible, distance_cm):
    if not person_visible or distance_cm is None:
        return "stop"
    if distance_cm > 30:
        return "follow"
    return "stop"


if __name__ == "__main__":
    print("Person ahead, path clear:", follow_action(True, 80))
    print("Obstacle close:", follow_action(True, 20))
    print("Lost sight of person:", follow_action(False, 80))
