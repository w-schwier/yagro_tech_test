# Factory Simulation Tech Test

[Introduction](#introduction) | [Installation](#installation) | [How to Run](#how-to-run) | [The Challenge](#the-challenge) | [Glossary](#glossary) | [Assumptions](#assumptions) |  [Requirements](#requirements) | [Possible Future Updates](#possible-future-updates) | [Approach](#approach) | [Summary](#summary)

## Introduction
Will Schwier's YAGRO tech test submission. Requires python: 3.10.

## Installation
1. In terminal, navigate to where you want the project. 
2. Clone the repository using: `git clone https://github.com/w-schwier/yagro_tech_test.git`
3. Change into the cloned directory with: `cd yagro_tech_test`
4. Set up venv:
    ```commandline
    python -m venv ./venv
    source venv/bin/activate
    ```
5. Install the necessary requirements in the venv, and run the tests with:
    ```commandline
    python -m pip install -r requirements.txt
    pytest
    ```

## How to Run
1. Navigate to the project's root directory.
2. Activate the venv.
3. Run the following code:
```commandline
python -m factory_simulator
```
There are a few optional CLI arguments, these can be seen by running the command above with an `-h` flag

## The Challenge
There is a factory production line around a single a conveyor belt.  

Components (of type A and B) come onto the start of the belt at random intervals; workers must take one component of each type from the belt as they come past, and combine them to make a finished product.

The belt is divided into fixed-size slots; each slot can hold only one component or one finished product.  There are a number of worker stations on either side of the belt, spaced to match the size of the slots on the belt, like this (fixed-width font ASCII pic):

```
       v   v   v   v   v          workers
     ---------------------
  -> | A |   | B | A | P | ->     conveyor belt
     ---------------------
       ^   ^   ^   ^   ^          workers
```
In each unit of time, the belt moves forwards one position, and there is time for a worker on one side of each slot to EITHER take an item from the slot or replace an item onto the belt.  The worker opposite them can't touch the same belt slot while they do this.(So you can't have one worker picking something from a slot while their counterpart puts something down in the same place).

Once a worker has collected one of both types of component, they can begin assembling the finished product.  This takes an amount of time, so they will only be ready to place the assembled product back on the belt on the fourth subsequent slot.  While they are assembling the product, they can't touch the conveyor belt.  Workers can only hold two items (component or product) at a time: one in each hand.

Create a simulation of this, with three pairs of workers.  At each time interval, the slot at the start of the conveyor belt should have an equal (1/3) chance of containing nothing, a component A or a component B.

Run the simulation for 100 steps, and compute how many finished products come off the production line, and how many components of each type go through the production line without being picked up by any workers.

A few pointers:
 - The code does not have to be 'production quality', but we will be looking for evidence that it's written to be somewhat flexible, and that a third party would be able to read and maintain it. 
 - Be sure to state (or comment) your assumptions.
 - During the interview, we may ask about the effect of changing 
certain aspects of the simulation. (E.g. the length of the conveyor belt.)
 - Flexibility in the solution is preferred, but we are also looking for a sensible decision on where this adds too much complexity. (Where would it be better to rewrite the code for a different scenario, rather than spending much more than the allotted time creating an overly complicated, but very flexible simulation engine?)

## Glossary
* Tick: One unit of time.
* Simulation: The running of the whole program, for the total required number of ticks.
* Component: Of type 'A' or 'B'. They can be combined to make a product.
* Product: Created by combining and assembling components 'A' and 'B'. Shorthand - P.
* Item: Used to refer to either a component or product. In the code, it is also used for "empty" items.
* Worker: The heart of the factory! Workers stand either side of a belt slot. They pick up one of each component, assemble them into products, then place them on the belt.
* Belt: Comprised of one to many slots. Used to move items in front of the workers. Allowing them to pick up components, and place assembled products.
* Slot: Each belt slot is capable of containing one item, including empty items.
* Input: These are either components, or empty items, randomly selected, that are added to the start of the belt.
* Output: Any item that is moved off the end of the belt.

## Assumptions
* The belt is empty at the start, with the first tick putting a random input on the first slot of the belt.
* The belt is horizontal, mainly for ease of referencing which worker of a pair is being referred to.
* Per tick, the belt moves, then the workers interact with it.
* If both workers at a belt slot need the component, preference will be given to the top row.
* It takes 1 tick to assemble a product - This specification was derived from the brief and could have been interpreted in two ways. In the interest of keeping things as simple as possible, until necessary, the first interpretation (i) will be assumed and the second (ii) will be mentioned further below:
  1) 4 ticks from picking up the first component.
  2) 4 ticks from starting assembly.
* While assembling, workers can't do anything else until they finish. However, since they can hold a completed product in one hand, this allows them to pick up a component with the other, while waiting to be able to place the finished product on the belt.
* Workers can only place products on the belt.
* Workers shouldn't hold two of the same component.

## Requirements:
* A belt that has inputs added to it one at a time, and only has as many items on it, as its length.
* The number of slots on the belt, is equal to the pairs of workers. (3)
* The belt has an equal (1/3) chance of the incoming slot containing 'A', 'B' or 'EMPTY'
* Slots can only contain one item.
* Workers can only hold two items at one time.
* Only one worker can interact with a belt slot per tick.
* Workers can't take and place items in the same tick.
* Workers combine components A + B -> P
* The simulation runs for 100 ticks.
* Order of operations per tick:
  1. Belt moves up one slot, with a new random input in the first slot.
  2. Item in the last slot moves off the end of the belt and gets added to the output to be tallied.
  3. Iterates through workers; having them perform only one action, with the following order of preference:
     1. Worker tries to place assembled product if finished and there's space.
     2. Worker tries to take a required component, if possible.
     3. Worker tries to assemble a product, if they have the needed components.
* Keeps track of what outputs come off the end of the belt, then reports the total tally.

## Possible Future Updates
Below are some possible updates that could be added given more time, or if the code was actually going into production:
* Add Docstrings everywhere.
* Requirements section transformed into user stories.
* A nice GUI to neatly and clearly show what's happening per factory tick.
* More functionality extracted/abstracted to belt class, possibly such as worker interactions.
* Full implementation of configurable assembly ticks. I.e. Changing how long (how many ticks) it takes a worker to assemble a product.
* Worker tracking - How long waiting for components, how long waiting to place product on belt, how many products assembled, etc.
* Ability to easily change name of core components - This was actually done after most of the code was finished. Very simple with my IDE, but not allowed for in code.

## Approach
The first thing I did was to read the challenge brief thoroughly; trying to understand all the moving parts and what needs to happen at a high level, making notes as I went about what I will need, possible classes and solutions. The culmination of which is effectively the glossary, assumptions and requirements sections.

With more of an understanding of what I needed to do now, I moved on to trying to spike the solution, in a very simple and easily readable way. Although this code definitely didn't follow best practices, it helped me to get a better understanding of what my ultimate solution would look like. For the spike, I wrote the program to step through the ticks one by one, rather than flying through 100. This was to get more visibility on what was happening, and to ensure my code was behaving as expected. However, the code was written in a way that it was easy to add the functionality to go through 100 ticks automatically. As mentioned above, also applying the KISS design pattern concept to how many ticks it takes to assemble a product, meant assuming it took only one tick. This simplified the worker class, as it meant all actions were only one tick, and therefore the class had no need to track such things.  

As possibly evident, I'm a big believer in the saying "Spend 90% of your time sharpening the axe, 10% chopping the tree." Having spiked working code, I then finished final planning, before finally starting the 'final' code. I considered using the factory design pattern for my final version; however, once again applying the KISS philosophy, I decided it added unnecessary complexity, for relatively little gain. This was the same for configparser for the CLI section.

When writing the main code, I tried not to reference the spike code too much. Instead, opting to TDD the classes based on what I had learnt in the prior preparation. Thanks to all that, this part was fairly quick and straightforward. I was also a lot more mindful of best practices as I went this time. Refactoring as necessary any time I noticed code smells. I then went through all the code once I'd finished to see if I could simplify or add readability/maintainability anywhere. 

## Summary
In summary, I thought I prepared and planned well. This allowed me to, hopefully, keep the code simple, highly readable and maintainable. I think I did well trying not to add unnecessary complexity when not enough of a benefit was gained, although I'm sure there are area's that could be improved on. The original spike was ~100 lines of code. I'm sure my final version is considerably more than 100 lines, and considerably more robust and follows a lot more of the best practices.

I do think the Worker class could have been refactored more or simplified slightly, perhaps with more abstraction. Although I did manage to remove the need for a Worker to have a belt property using dependency injection, which I was quite happy with. It would have also been nice to implement the ticks to assemble functionality, but ultimately it was too much complexity for a feature that wasn't requested yet.  


