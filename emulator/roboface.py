import pew
import random
import copy

pew.init()

# Eye animation frames
blinkImg = [
    [
        [0, 0, 1, 1, 1, 1, 0, 0],  # Fully open eye
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0, 0, 0, 0],  # Fully closed eye
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
]


def fill_rect(image, x, y, wx, wy):
    x = int(x)
    y = int(y)
    wx = int(wx)
    wy = int(wy)
    for row in range(y, y + wy):
        for column in range(x, x + wx):
            image[row][column] = 0


screen = pew.Pix()
pew.show(screen)

blinkIndex = [1, 2, 3, 4, 3, 2, 1]  # Blink bitmap sequence
blinkCountdown = 100  # Countdown to next blink (in frames)
gazeCountdown = 75  # Countdown to next eye movement
gazeFrames = 50  # Duration of eye movement (smaller = faster)
eyeX = 3
eyeY = 3  # Current eye position
newX = 3
newY = 3  # Next eye position
dX = 0
dY = 0  # Distance from prior to new position

loop = True
while loop:
    keys = pew.keys()
    if keys & pew.K_X:
        loop = False

    image = copy.deepcopy(blinkImg[blinkIndex[blinkCountdown] if blinkCountdown < len(blinkIndex) else 0])
    blinkCountdown -= 1
    if blinkCountdown == 0:
        blinkCountdown = random.randint(5, 180)

    # Add a pupil(2x2 black square) atop the blinky eyeball bitmap.
    # Periodically, the pupil moves to a new position...
    gazeCountdown -= 1
    if gazeCountdown <= gazeFrames:
        # Eyes are in motion - draw pupil at interim position
        fill_rect(image,
                 newX - (dX * gazeCountdown / gazeFrames),
                 newY - (dY * gazeCountdown / gazeFrames),
                 2, 2)
        if gazeCountdown == 0:  # Last frame?
            eyeX = newX
            eyeY = newY  # Yes.What's new is old, then...
            newX = random.randrange(7)
            newY = random.randrange(7)
            dX = newX - 3
            dY = newY - 3
            while dX * dX + dY * dY >= 10:  # Pick random positions until one is within the eye circle. Thank you Pythagoras
                newX = random.randrange(7)
                newY = random.randrange(7)
                dX = newX - 3
                dY = newY - 3

            dX = newX - eyeX  # Horizontal distance to move
            dY = newY - eyeY  # Vertical distance to move
            gazeFrames = random.randint(3, 15)  # Duration of eye movement
            gazeCountdown = random.randint(gazeFrames, 120)  # Count to end of next movement
    else:  # Not in motion yet - - draw pupil at current static position
        fill_rect(image, eyeX, eyeY, 2, 2)

    pew.show(pew.Pix.from_iter(image))
    pew.tick(1 / 12)
