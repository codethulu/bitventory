# bitventory
## A simple, flexible inventory engine for pygame projects.
<img width="614" alt="image" src="https://user-images.githubusercontent.com/45674799/177220622-65de8fa0-9898-4b02-93a7-cd8d87de23d4.png">

**This project uses Python3.10 as it uses ``match`` - you could manually replace this with an ugly if statement if you *really* wanted to**

(This project is still a work in progress and was the product of a train journey back home - further development is planned to make incorporating into projects much easier!)

## How to use

To create a new inventory window, initialise as so:

NAME- Name of the window

ROWS - The amount of columns the inventory window has

COLUMNS - The amount of columns the inventory window has

X - x position of the window

Y - y position of the window

SCALE - The size of the inventory window (3 default)

STACK_LIMIT - The maximum size items in the inventory can stack to (99 default)

``inventory = Inventory(NAME, ROWS, COLUMNS, X, Y, SCALE, STACK_LIMIT)``

## Example

The ``main()`` method provided initialises an example playground. Two inventory windows are initialised with scale 3. By running the program, you should be able to move items between the two windows and experiment with the sorting buttons. You can press [C] to randomly add new items to your inventory to experiment with the features.

## Features

⭐️ Flexible framework for any pygame project

🔠 Name inventory windows

✨ Visual effects such as multiple item stacking and animations 

⏳ Sort by name and stack size using the buttons!

🧲 Holding [SHIFT] while an item is picked up will allow you to automatically pick similar items up on hover!

🖖 You can split item stacks using [RIGHT CLICK]

![magent-inventory](https://user-images.githubusercontent.com/45674799/177222020-514542d9-7000-4451-b60a-628e1aa62f42.gif)

