from robots.clever import CleverRobot
# from robots.chatter import ChatterRobot 

import sys

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("Usage: ./robanon.py <robot> <id> [response ids...]")

    robot = sys.argv[1]
    token = sys.argv[2]
    ids = sys.argv[3:]

    if robot == 'clever':
        cls = CleverRobot
    # elif robot == 'chatter':
    #     cls = ChatterRobot
    else:
        print("Unknown robot '{}'".format(robot))
        sys.exit(1)

    obj = cls(token, ids)
    obj.run()
