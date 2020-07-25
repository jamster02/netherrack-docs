# Netherrack
Welcome to the Netherrack documentation. Netherrack is a tool to convert Python code into DF code templates. This project is based on [Prismarine](https://dfprismarine.github.io/), another tool to convert JavaScript code into DF. [Skip to Documentation](#Reference).

Here's a basic example of using Netherrack:
```py
from netherrack import netherrack as df

# Creates a new line with Player Event: RightClick
line = df.Line('event', 'RightClick')
player = line.playerAction # Ease of use

line.ifPlayer("IsLookingAt", df.Location(25.5, 5, 30.0)) # checks if player is looking at a location
player("SendMessage", "You're looking at the Sacred Netherrack!")
line.close() # ends the if statement

cmd, data, enc = line.build() # Builds the line and outputs a give command and json data
print(cmd)
```

# When to use Netherrack?
Netherrack is meant to be used in parallel with DFs coding system. This is because _some_ things are easier to do in text-based programming, while others are not.
### When you SHOULD NOT use Netherrack
- Inventory GUIs
- Basic Systems & Tag-intensive stuff
- Mob spawning
- Location checks
- etc

### When you SHOULD use Netherrack
- Quest / XP Systems
- Dialogue
- Tedious tasks with multiple outcomes
- Heavy calculations
- Encryption & Complicated text manipulation
- etc

# Reference
_*argument_ = argument is optional.
**value** = the default value.

## Important
- [Events](#Events)
- [Optional](#Optional-Variables)
- [Actions](#Actions)
- [Building](#Building)

## Add-ons
- [Netherite](Netherite.md)

## Variable Items
- [Variable](#Variable)
- [Location](#Location)
- [Game Value](#Game-Value)
- [Particle](#Particle)
- [Potion](#Potion)
- [Sound](#Sound)

## IF / Repeat
- [IFs](#IF-Variable)
- [Else](#Else)
- [Repeat](#Repeat)

## Misc
- [Call Functions](#Calling-Functions)
- [Select Object](#Select-Object)
- [Tags](#Tags)
- [Discord](#Discord)

# Important
To start a Netherrack program you must first import netherrack. You can do this with `from netherrack import netherrack`, or to have a special variable name: `from netherrack import netherrack as df`.

## Events
To initialise a codeline, you can use the `df.Line(eventType, eventName)` class.
- eventType - the type of event. Supported types are `event`, `entity_event`, `func` and `process`.
- eventName - the name of the event. For example, `Join` or `Jump`. This can be anything for functions and processes.

## Optional Variables
It's also recommened to set up some variables, although it is purely up to you. For ease of use however, you should set variables for some or all of the following functions:

`line.playerAction`, `line.ifVar`, `line.setVar`, `etc`.

## Actions
Most codeblocks require the `action` parameter, followed by the chest parameters. Valid action codeblocks are `playerAction`, `gameAction`, `entityAction`, `Control` and `setVar`.
### Usage
```py
# It supports numbers...
line.playerAction("LaunchFwd", 10)

# And text...
line.playerAction("SendMessage", "Woosh!")

# And all of the other data types!
line.playerAction("Teleport", df.Location(15, 70, 15))
```

### Targets
You can also target groups of players by appending `.target` to the action!
```py
line = df.Line("func", "xp")
line.playerAction("SendMessage", r"%default has leveled up!").target("All Players")
```

## Building
To build your line and convert it into a template, you must use the `line.build` function. This will return a /give command, followed by the raw json data and encrypted data. You can get the template into minecraft with something like this:
```py
cmd, data, encrypted = line.build()
print(cmd)
```
Note that you must specify variables for all three returns.

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
### Usage
```py
loc = Location(15.5, 70, 20)

line = df.Line('event', 'Join')
line.playerAction("Teleport", loc)
```

## Game Value
Represents a Game Value variable.
### Class
```py
GameValue(type, *target)
```
- type - The name of the value.
- _*target_ - The target of the value, defaults to **Default**.

The `GameValue.target` function can set the target even after initialisation.
### Usage
```py
line = df.Line("process", "loop")
line.playerAction("ActionBar", "There are", GameValue("Player Count"), "players online!")
```

## Particle
Represents a particle item in-game.
### Class
```py
Particle(type)
```
- type - The particle effect.

Additional manipulation of particles will be added in the future.
### Usage
```py
line = df.Line("event", "Join")
line.gameAction("SpawnParticle", Particle("Smoke"), Location(15.5, 20, 3))
```
## Potion
Represents a potion item in-game.
### Class
```py
Potion(effect, length, *amplifier)
```
- effect - The potion effect name.
- length - The length of the potion effect in ticks.
- _*amplifier_ - The potion amplifier, defaults to **1**.

### Usage
```py
line = df.Line("event", "Join")
line.playerAction("GiveEffect", Potion("Blindness", 40), Potion("Slowness", 40, 5))
# Supports as many items as you want! ^
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

### Usage
```py
line = df.Line("func", "xp")
player = line.playerAction

player("PlaySound", Sound("Pling"))
player("SendMessage", r"You gained 5 XP!")
```

# IFs & Repeats
Note that with this system, nesting IFs & Repeats inside each other can be a bit messy. For now, use special whitespace between IFs for better readability. We may come up with a better system in the future, however python cannot have functions inside functions, so nothing's certain.
## IF Variable
If variable works much like other actions, however it takes an operation as an argument. Anything after the If Variable will be evaluated as being inside of it, until reaching a `line.close()` function.
### Usage
```py
line = df.Line('event', 'Join')
player = line.playerAction

joined = df.Variable(r"%default joined", "saved")

line.ifVar("=", joined, 0)
line.setVar("+=", joined)
player("SendMessage", r"%default joined for the first time!").target("All Players")
line.close()

cmd, data = line.build()
```
## IF Player
If player, If entity and If game behave much like If variable, except with actions instead of operations as arguments. Valid actions are `IsSprinting`, `NameEq`, `etc`.
### Usage
Note here that `line.close()` can also be used as a custom variable:
```py
line = df.Line('event', 'Jump')
player = line.playerAction
c = line.close

line.ifPlayer('IsSneaking')
player("SendMessage", "You jumped while sneaking!")
c()
```
## Else
Else executes different code when an IF statement isn't true.
### Usage
Else can be used at the end of any close statement like so:
```py
line = df.Line('event', 'Jump')
player = line.playerAction

line.ifPlayer('IsSneaking')
player("SendMessage", "You jumped while sneaking!")
line.close()._else()
player("SendMessage", "You are not sneaking!")
line.close()
```
## NOT
NOT inverts the IF statement, e.g. `IsSprinting` becomes `Is Not Sprinting`.
### Usage
NOT is used in the same manner as else, but at the beginning of the statement rather than the end.
```py
line = df.Line('event', 'Jump')
player = line.playerAction

line.ifPlayer('IsSprinting')._not
player("SendMessage", "You are not sprinting!")
line.close()
```
## Repeat
Works the same as IFs, with some changed arguments.
```py
<line>.repeat(action, items)
```
### Usage
Here's a simple case of repeating some code multiple times:
```py
line = df.Line("event", "Join")
repeat = line.repeat

repeat("Multiple", 10)
line.playerAction("SendMessage", "This is the power of repeats!")
line.close()
```

# Misc
## Select Object
Select Object is much like other action block types, but it requires a sub-action.
### Class
```py
<line>.selectObj(action, sub-action, *items)
```
- action - The first selection of the block. e.g. `Shooter`, `Killer`, `etc.`
- sub-action - This is only used for IF selections, leave a random action if not used. e.g. `EStandingOn`, `VarExists`, `etc.`
- items - Chest parameters, if necessary
### Usage
```py
line = df.Line('event', 'KillPlayer')

line.selectObj('Killer')
line.playerAction('SendMessage', 'Not cool!')
line.playerAction('Damage', 10)
```
## Calling functions
It's possible to call functions and processes using `line.callFunc(name)` and `line.callProc(name)`.
## Color codes
Color codes are now supported! `&` is automatically converted when passed in to the `Text` class or as an argument.
## Tags
Tags are automatically added as their default option where needed. Currently, there is no way to modify tags, as it would be confusing for the user. We may add a way to change them in the future.

Thanks to EnjoyYourBan for providing an [action list](https://raw.githubusercontent.com/EnjoyYourBan/enjoyyourban.github.io/master/actions.json) with all the tags!
## Discord
Netherrack has a [Discord](https://discord.gg/dXsXKXX)!
