# Netherite
Netherite is an add-on to the Netherrack library. It allows you to use basic templates and functions in your code, by saving them to the current line!
## Example
```py
line = df.Line("event", "Join")

line = nt.example(line, "hi")
```

## Installation
Netherite comes built into netherrack! To use it, you can use the same syntax as netherrack:
```py
from netherrack import netherite as nt
```

# Reference
## Set Vars
This function can set multiple vars easily, without having to type the command over and over again.
### Usage
```py
line = nt.setVars(line, **variables)
```
- `line` is the line to append to.
- `**variables` represents a kwarg-style argument.
### Example
```py
line = nt.setVars(line, variable=value, variable2=value2)
```

## Animate Title / Animate Action Bar
This function can animate titles and action bars, much like in Infinite Dungeons II.
### Usage
```py
line = nt.animateTitle(line, initialDelay, delay, sound, prefix, content, suffix, *subTitle)
line = nt.animateBar(line, initialDelay, delay, sound, prefix, content, suffix)
```
- `line` is the line to append to.
- `initialDelay` represents the delay before the first letter is displayed.
- `delay` represents the delay between appending letters.
- `sound` represents a Netherrack `Sound` class to play when appending letters.
- `prefix` is the prefix that will appear before the content on every iteration.
- `content` is the final text to be displayed.
- `suffix` is the suffix that will appear after the content on every iteration.
- `*subTitle` is an optional argument, only available for `animateTitle`.
### Example
```py
line = nt.animateTitle(line, 20, 5, df.Sound("Wooden Pressure Plate Click On"), "&5<< &d", "S p a c e", " &5>>")
```
