"""
Snake Game
This program simulates the classic snake game using a doubly-linked list

File Name: howry_snake_game.py
Author: Ken Howry
Date: 10.4.23
Course: COMP 1353
Assignment: Project I
Collaborators: N/A
Internet Source: N/A
"""
#imports
import dudraw
import random

#classes
#Class: Node
class Node:
    def __init__(self, v, p, n):
        """
            Description of Function:
                initializes an empty node
            Parameters:
                v: value of node
                p: reference to prev node
                n: reference to next node
            Return:
                None
        """
        self.value = v
        self.prev = p
        self.next = n

    def __str__(self):
        """
            Description of Function: 
                returns a string representing the node
            Parameters: 
                None
            Return: 
                str
        """
        return str(self.value)

#Class: DoublyLinkedList 
class DoublyLinkedList:
    def __init__(self):
        """
            Description of Function:
                initializes an empty list
            Parameters:
                None
            Return:
                None
        """
        self.header = Node(None, None, None)
        self.trailer = Node(None, self.header, None)
        self.header.next = self.trailer
        self.size = 0

    def __str__(self):
        """
            Description of Function: 
                returns a string representing the list
            Parameters: 
                None
            Return: 
                str
        """
        #handle empty list case
        if self.header.next.value is None:
            return '[]'
        
        result = '['
        #create a reference to the first value in list
        temp_node = self.header.next

        #stop before the trailer so we don't add an extra space
        while temp_node.next.value is not None:
            result += str(temp_node) + " "
            temp_node = temp_node.next
        
        return result + str(temp_node) + ']'
    
    def is_empty(self):
        """
            Description of Function: 
                returns True if the list is empty, False otherwise
            Parameters: 
                None
            Return: 
                bool
        """
        return self.header.next is self.trailer

    def get_size(self):
        """
            Description of Function: 
                returns the size of the list
            Parameters: 
                None
            Return: 
                int
        """
        return self.size

    def add_between(self, v, n1, n2):
        """
            Description of Function: 
                adds value v between n1 and n2
            Parameters:
                v: type is the generic type E of the list
                n1: node in list
                n2: second node in list
            Return: 
                None
        """
        #checks if n1 or n2 is None
        if n1 is None or n2 is None:
            raise ValueError("Invaild n1 or n2 - can't be None.")
        
        #checks if n1 and n2 are not next to each other
        if n1.next is not n2:
            raise ValueError("Second node must come before first node")
        
        #step 1: make a new node
        new_node = Node(v, n1, n2)

        #step 2: fix n1.next and n2.prev
        n1.next = new_node
        n2.prev = new_node

        #step 3: increment sixe
        self.size += 1
    
    def remove_between(self, node1, node2):
        """
            Description of Function: 
                removes and returns value of node between n1 and n2
                there can only be one node between n1 and n2
            Parameters:
                n1: node in list
                n2: second node list
            Return: 
                int
        """
        # check if either node1 or node2 is None. Raise a ValueError if so.
        if node1 is None or node2 is None:
            raise ValueError("Invaild node1 or node2 - can't be None.")
        
        # Check that node1 and node 2 has exactly 1 node between them
        # raise a ValueError if not
        elif node1.next.next is not node2 and node2.prev.prev is not node1:
            raise ValueError("There is not only one node between node1 and node2.")

        else:
            #step 1: store the value being removed
            return_value = node1.next.value

            #step 2: delete the node by removing the references to it
            node1.next = node2
            node2.prev = node1
            
            #step 3: decrement size
            self.size -= 1

            #step 4: return the value
            return return_value

    def add_first(self, v):
        """
            Description of Function: 
                adds a the value v at the head of the list
            Parameters:
                v: type is the generic type E of the list
            Return:
                None
        """
        self.add_between(v, self.header, self.header.next)

    def add_last(self, v):
        """
            Description of Function:
                adds a the value v at the tail of the list
            Parameters:
                v: type is the generic type E of the list
            Return:
                None
        """
        self.add_between(v, self.trailer.prev, self.trailer)

    def remove_first(self):
        """
            Description of Function:
                removes and returns the first value in the list
            Parameters:
                None
            Return:
                None
        """
        return self.remove_between(self.header, self.header.next.next)

    def remove_last(self):
        """
            Description of Function:
                removes and returns the last value in the list
            Parameters:
                None
            Return:
                None
        """
        return self.remove_between(self.trailer.prev.prev, self.trailer)
    
    def first(self):
        """
            Description of Function:
                returns the first value in the list
            Parameters:
                None
            Return:
                int
        """
        return self.header.next.value

    def last(self):
        """
            Description of Function:
                returns the last value in the list
            Parameters:
                None
            Return:
                int
        """
        return self.trailer.prev.value

    def search(self, value):
        """
            Description of Function:
                returns the index of the value if found and -1 otherwise
            Parameters:
                value: int value being searched for in the list
            Return:
                int
        """
        #variable to track index
        index = 0

        #set a temporary node to the first value in the list
        temp_node = self.header.next

        #iterate through list until value is reached, then return index
        while temp_node.value is not None:
            if temp_node.value == value:
                return index
            else:
                index += 1
                temp_node = temp_node.next
        #if the value is not found, return -1
        return -1
    
    def get(self, index):
        """
            Description of Function:
                returns the value at index i
            Parameters:
                i: the index
            Return:
                int
        """
        #IndexError
        if index >= self.size:
            raise IndexError("Index is out of range.")
        
        #step 1: create variable to track the index
        idx_value = 0

        #step 2: create a second variable to traverse the list 
        temp_node = self.header.next

        #step 3: traverse list until the given index and return value
        while True:
            if idx_value == index:
                return temp_node.value
            temp_node = temp_node.next
            idx_value += 1

#Class: Snake
class Snake:
    #class attributes for directions
    DIRECTION_NONE = ' '
    DIRECTION_RIGHT = 'd'
    DIRECTION_LEFT = 'a'
    DIRECTION_UP = 'w'
    DIRECTION_DOWN = 's'

    def __init__(self, x, y):
        """
        Description of Function:
            initializes an empty doubly-linked list with sentinel nodes
            appends a tuple of (x, y)
            sets direction to class attribute: Snake.DIRECTION_NONE
        Parameters:
            x: x-coordinate
            y: y-coordinate 
        Return:
            None
        """
        self.body = DoublyLinkedList()
        self.body.add_first((x, y))
        self.direction = Snake.DIRECTION_NONE

    def move(self):
        """
            Description of Function:
                moves the snake by appending a new tuple 
                to the beginning of the list 
                and removing the last value in the list
            Parameters:
                None
            Return:
                None
        """
        #getting the value of the head of the snake
        head = self.body.first()

        #variable assignment
        x = head[0]
        y = head[1]
        
        #assigning a new tuple according to snake direction
        if self.direction == Snake.DIRECTION_LEFT:
            (x, y) = head[0] - 1, head[1]
        elif self.direction == Snake.DIRECTION_RIGHT:
            (x, y) = head[0] + 1, head[1]
        elif self.direction == Snake.DIRECTION_DOWN:
            (x, y) = head[0], head[1] - 1
        elif self.direction == Snake.DIRECTION_UP:
            (x, y) = head[0], head[1] + 1

        #appending new tuple
        self.body.add_first((x, y))

        #removing last value
        self.body.remove_last()

    def eat_and_grow(self):
        """
            Description of Function:
                increases the length of the snake 
                by adding to the end of the list
            Parameters:
                None
            Return:
                None
        """
        #getting the value of the tail of the snake
        tail = self.body.last()

        #variable assignment
        x = tail[0]
        y = tail[1]
        
        #adding the to tail in the opposite direction of head
        if self.direction == Snake.DIRECTION_LEFT:
            (x, y) = tail[0] + 1, tail[1]
        elif self.direction == Snake.DIRECTION_RIGHT:
            (x, y) = tail[0] - 1, tail[1]
        elif self.direction == Snake.DIRECTION_DOWN:
            (x, y) = tail[0], tail[1] + 1
        elif self.direction == Snake.DIRECTION_UP:
            (x, y) = tail[0], tail[1] - 1

        #appending to the end of the list
        self.body.add_last((x, y))

    def check_crash(self):
        """
            Description of Function:
                checks if the snake crashes into the wall of the canvas
                or into itself
            Parameters:
                None
            Return:
                bool
        """
        #the value of the head of the snake
        head = self.body.first()
        
        #checking if the snake has passed the walls of the canvas
        if (
            head[0] + .5 < 0
            or head[0] + .5 > 20 
            or head[1] + .5 > 20
            or head[1] + .5 < 0
        ):
            return True
        
        #variable assignemnt
        x = head[0]
        y = head[1]

        #checking if the head of the snake has the same (x, y) value as another Node
        for i in range(1, self.body.size):
            if self.body.get(i)[0] == x and self.body.get(i)[1] == y:
                return True 

        #if neither condition is True
        return False
    
    def draw(self):
        """
            Description of Function:
                draws the snake on the canvas
            Parameters:
                None
            Return:
                None
        """
        #variable assignment
        temp_node = self.body.header.next

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        #while loop to draw each Nose of the snake
        while temp_node.value is not None:
            dudraw.set_pen_color_rgb(r, g, b)
            dudraw.filled_square(temp_node.value[0], temp_node.value[1], .5)
            temp_node = temp_node.next

# Class: Food
class Food:
    def __init__(self):
        """
            Description of Function:
                setting the location of the food
                and spawning food
            Parameters:
                None
            Return:
                None
        """
        self.loc = (0, 0)
        self.spawn_food()

    def draw(self):
        """
            Description of Function:
                draws the food of the canvas
            Parameters:
                None
            Return:
                None
        """
        dudraw.set_pen_color(dudraw.BOOK_RED)
        dudraw.filled_circle(self.loc[0], self.loc[1], .5) 

    def spawn_food(self):
        """
            Description of Function:
                sets the food coordinates to a random (x, y)
                and ensures it is not the same value as a (x, y) in the snake
            Parameters:
                None
            Return:
                None
        """
        while True:
            #generating a random (x, y)
            x = random.randint(0 ,19)
            y = random.randint(0, 19)

            #checking the snake does not have the same (x, y)
            if snake.body.search((x, y)) == -1:
                self.loc = (x, y)
                break

#variable assignment
scale = 500

#creating canvas
dudraw.set_canvas_size(scale, scale)
dudraw.set_x_scale(-.5, 19.5)
dudraw.set_y_scale(-.5, 19.5)

#variable assignment
key = ' '

snake = Snake(10, 10)
food = Food()
game_over = False

#main code block
limit = 20 #number of frames to allow to pass before snake moves
timer = 0  #a timer to keep track of number of frames that passed

while not game_over:
    timer += 1

    #processing keyboard presses here

    #changes key when new key typed
    if dudraw.has_next_key_typed():
        key = dudraw.next_key_typed()

    if key == 'w':
        snake.direction = Snake.DIRECTION_UP
    elif key == 'a':
        snake.direction = Snake.DIRECTION_LEFT
    elif key == 's':
        snake.direction = Snake.DIRECTION_DOWN
    elif key == 'd':
        snake.direction = Snake.DIRECTION_RIGHT

    if timer == limit:
        dudraw.clear(dudraw.WHITE)
        timer = 0

        #draws and moves the snake
        #checks to see if snake ate the fruit
        #checks if the snake self intersects or hits edge of canvas

        snake.draw()
        food.draw()
        snake.move()

        if snake.body.first() == food.loc:
            snake.eat_and_grow()
            food.spawn_food()
        
        if snake.check_crash() == True:
            game_over = True

        snake.draw()

    dudraw.show(40)