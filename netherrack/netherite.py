from netherrack import netherrack as df

def setVars(line, **kwargs):
    for arg in kwargs:
        line.setVar("=", arg, kwargs[arg])
    
    return line

def animateTitle(line, initialDelay, delay, sound, prefix, content, suffix, subTitle=None):
    if not subTitle:
        subTitle = ""

    delayVar = df.Variable("delay")
    prefixVar = df.Variable("prefix")
    contentVar = df.Variable("content")
    suffixVar = df.Variable("suffix")
    updateText = df.Variable('updateText')
    sub = df.Variable('subTitle')

    line.setVar("=", delayVar, delay)
    line.setVar("=", prefixVar, prefix)
    line.setVar("=", contentVar, content)
    line.setVar("=", suffixVar, suffix)
    line.setVar("=", sub, subTitle)

    textList = df.Variable("text")
    currentText = df.Variable("currentText")
    letter = df.Variable("letter")

    line.setVar("=", currentText, "")
    line.setVar("SplitText", textList, contentVar)
    line.control("Wait", initialDelay)

    line.repeat('ForEach', letter, textList)

    line.setVar("SplitText", textList, contentVar)

    line.setVar("Text", currentText, currentText, letter)
    line.setVar("Text", updateText, prefixVar, currentText, suffixVar)
    line.playerAction("SendTitle", updateText, sub, delayVar, 0, delayVar)
    line.playerAction("PlaySound", sound)
    line.control("Wait", delayVar)

    line.close()

    return line

def animateBar(line, initialDelay, delay, sound, prefix, content, suffix):
    if not subTitle:
        subTitle = ""

    delayVar = df.Variable("delay")
    prefixVar = df.Variable("prefix")
    contentVar = df.Variable("content")
    suffixVar = df.Variable("suffix")
    updateText = df.Variable('updateText')

    line.setVar("=", delayVar, delay)
    line.setVar("=", prefixVar, prefix)
    line.setVar("=", contentVar, content)
    line.setVar("=", suffixVar, suffix)

    textList = df.Variable("text")
    currentText = df.Variable("currentText")
    letter = df.Variable("letter")

    line.setVar("=", currentText, "")
    line.setVar("SplitText", textList, contentVar)
    line.control("Wait", initialDelay)

    line.repeat('ForEach', letter, textList)

    line.setVar("SplitText", textList, contentVar)

    line.setVar("Text", currentText, currentText, letter)
    line.setVar("Text", updateText, prefixVar, currentText, suffixVar)
    line.playerAction("ActionBar", updateText)
    line.playerAction("PlaySound", sound)
    line.control("Wait", delayVar)

    line.close()

    return line