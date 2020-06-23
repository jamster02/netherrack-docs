# Netherrack
Welcome to the Netherrack documentation. Netherrack is a tool to convert Python code into DF code templates. This project is based on [Prismarine](https://dfprismarine.github.io/), another tool to convert JavaScript code into DF.

Here's a basic example of using Netherrack:
```py
import netherrack as df

# Creates a new line with Player Event: Join
line = df.Line('event', 'Join')
player = line.playerAction # Ease of use

joins = df.Variable("joins", "saved") # Initialises a SAVE "joins" variable
line.setVar("+=", joins)
player("SendMessage", joins, "players have joined this plot so far.")

cmd, data = line.build() # Builds the line and outputs a give command and json data
print(cmd)
```
# Reference
_*argument_ = argument is optional.
**value** = the default value.

# Important
To start a Netherrack program you must first import netherrack. You can do this with `import netherrack`, or to have a special variable name: `import netherrack as df`.
## Line Variable
To initialise a codeline, you can use the `df.Line(eventType, eventName)` class.
- eventType - the type of event. Currently `event` and `entity_event` are supported.
- eventName - the name of the event. For example, `Join` or `Jump`.
## Optional Variables
It's also recommened to set up some variables, although it is purely up to you. For ease of use however, you should set variables for some or all of the following functions:

`line.playerAction`, `line.ifVar`, `line.setVar`, `etc`.
## Actions
Most codeblocks require the `action` parameter, followed by the chest parameters. Valid action codeblocks are `playerAction`, `gameAction` and `setVar`.
### Usage
```py
<line>.playerAction("SendMessage", "This supports numbers!", 1337)

<line>.gameAction("CancelEvent")

# You can also use variables and other data types as arguments!
joins = df.Variable("joins", "saved")

<line>.setVar("+=", joins)
<line>.playerAction("SendMessage", r"Hello %default! You joined at position", joins)
```
### Targets
You can also target groups of players by appending `.target` to the action!
```py
line = df.Line("event", "Join")
line.playerAction("SendMessage", r"%default has joined!").target("All Players")
```

## Building
To build your line and convert it into a template, you must use the `line.build` function. This will return a /give command, followed by the raw json data. You can get the template into minecraft with something like this:
```py
cmd, data = line.build()
print(cmd)
```

# Variable Items
Numbers and text passed to actions are automatically converted to the correct format. However, you can still create variable items for those types using the `df.Text(text)` and `df.Num(value)` classes.
## Variable
Represents a dynamic variable item.
### Class
```py
Variable(name, *type)
```
- name - The name of the variable item.
- _*type_ - The type of the variable. Can be **"unsaved"**, "saved" or "local".
## Location
Represents a location in-game.
### Class
```py
Location(x, *y, *z, *pitch, *yaw)
```
Locations are relative to the plot, meaning `(x=0, z=0)` is the bottom left corner of the plot.
### Example
```py
loc = Location(15.5, 70, 20)

line = df.Line('event', 'Join')
line.playerAction("Teleport", loc)
```
## Particle
Represents a particle item in-game.
### Class
```py
Particle(type)
```
- type - The particle effect.
Additional manipulation of particles will be added in the future.
### Example
```py
line = df.Line("event", "Join")
line.playerAction("GiveItems", Particle("Cloud")
```
## Potion
Represents a potion item in-game.
### Class
```py
Potion(effect, length, *amplifier)
```
- effect - The potion effect name.
- length - The length of the potion effect in seconds.
- _*amplifier_ - The potion amplifier, defaults to **1**.
### Example
```py
line = df.Line("event", "Join")
line.playerAction("GiveEffect", Potion("Blindness", 60))
```
## Sound
Represents a sound item.
### Class
```py
Sound(noise, *pitch, *volume)
```
- noise - The sound that is represented.
- _*pitch_ - The pitch the sound is at, defaults to **1**.
- _*volume_ - The volume the sound is at, defaults to **1**.
### Example
```py
line = df.Line("event", "Join")
player = line.playerAction

player("PlaySound", Sound("Pling"))
player("SendMessage", r"%default has joined!").target("All Players")
```

