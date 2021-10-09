#### Welcome to 
# Sadge

The single best, and worst, programming language you'll ever find, or not, I don't know what you look at on the internet...

[insert image]

## How it started

So, why would anyone make such an atrocity? Well it's quite simple actually; school. Or rather; my brain after being told to come up with my own programming language.

Why name it "Sadge" of all things?
I started without a name, but had named my first test file `test.sadge`, and it stuck.

The goal was ___memes & dreams, horrible Japengrish, and Nihongo Jouzu™___. Inpsired by a strange mix between c++ and python.

## How it's going

These goals were largely achieved through ~~forcing~~ _suggesting_ __the__ _most intuitive, comfortable, readable, easy, intuitive, totally-not-forcing-you-to-change-windows-keyboard-layouts-between-US-and-JP-constantly-while-programming_ syntax you'll ever see.

Concrete examples include:
- Starting function defintions with a capital letter ___F___ (because we all need so respect in our lives).
- ~~Forcing~~ _Requesting_ every identifier (variable name, function name, etc.) to end on one of the supported honorifics (more respect!);
  - さん
  - ちゃん
  - さま
  - くん
  - たん
  - せんぱい
  - せんせい
  - 先生
  - 先輩
  - 君
  - 様
  - 王女様
  - 殿
  - どの
  - との
  - ばか
  - ぱいせん
- Using the characters `「` and `」` instead of `(` and `)` for the parameterlists of functions (I dunno they just look cool ¯\\\_(ツ)\_/¯).
- Using the characters `【` and `】` instead of `(` and `)` in expressions (because why would we just use one set of brackets if we can have more).
- Writing variable assignments and if statements using ___Completely Correct Japanese Grammar™___;
  - variableNameさんはvalueです (just like you would say "私はNHK-manです")
  - variableNameさんはvalueですか？ (I know they look similar, just deal with it :) )
  - But why end it here! The full if-statement syntax is as follows:
    ```
    variableNameさんはvalueですか？
    ね～ //True code block.
    え！？ //Else code block.
    ```
  - Intuitive right? :D
- Over at Sadge Inc. (not a real incorporation) we don't care if you want to put all you code on one line (there may be exceptions), so we need an endline character.
  - For assignments and if statements the `です` and `ですか？` already cover you on this front.
  - But for other instances you need to use `山` (yama; mountain), if this doesn't make sense to you, just don't ask questions and live your life you ignorant ~~f̼̞͔͒͑̌̒ͬr͔̺͔͋̇ͮ͆ͯ͆͌́i̷̤̤̘ͥ̑ͪ̋̅͜ç̳̓̾͛ͤ̉̆͗ͅk̠̩̜͚͍̄́ͯ́̋̀̊ͅ~~ , if you are that one person who might know why, yes that's why, ofcourse it is.
- The numbers Mason, what do they mean!?
  - All numbers (only positive ints really supported, can get negative by subtracting from 0 :) ) must be written in ___Completely Correct Japanese™___.
  - The maximum lexable single number is 九万九千九百九十九 (99999), if you need something higher, it's basic math :).
- Code blocks are c++ style (indents dont matter) so we need code block open and closing characters...
  - For code block open we use `OwO` instead of `{`&nbsp;&nbsp;&nbsp;&nbsp;(I swear I am not a furry it's just that... I think something in me broke when I imagined a c++ file
  - For code block close we use `UwU` instead of `}`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;but all curly brackets are replaced with UwUs and OwOs... I sincerely apologise for my misconduct.)

Oh.

OH I almost forgor 💀.

We have for-loops.

Oh boi do we have for-loops.

( ͡° ͜ʖ ͡°)

Once again in the designing of our for-loops we used our patented _most intuitive, comfortable, readable, easy, intuitive, totally-not-forcing-you-to-know-an-entire-copy-pasta-of-the-top-of-your-head_ syntax you'll ever see.

Let's jump straight into an example _(Raid: Shadow Legends ad starts playing)_. Okay now let's jump right into it.

```
1. Well Crabs let me ask you a question.
2. If I *startingValue*, is it *comparisonOperator* enough?
3. When I throw it back, is *loopBody* fast enough?
4. If I *increment* it up, can *controlValue* handle that?
5. tHe fOrMuLA
```
Looks simple enough right? Surely I don't even need to explain... I do? Well alright then.

`startingValue`, `increment` and `controlValue` can be any expression. (An expression can contain any of the following: a number or bool, a sum, a variable, a function call, or even another expression)

`comparisonOperator` has to be some logic operator (>, <, >=, <=) and `loopBody` has to be a code block (OwO & UwU and everthing).

Alternatively there are a couple of default values:
- Starting line 2 with `If I back it up` for a default `startingValue` of `0`
- Starting line 4 with `If I speed it up` for a default `increment` of `1`
- Starting line 4 with `If I speed it up` for a default `increment` of `-1`

*Note: the mOcKiNG on `tHe fOrMuLA` is case sensitive! (as well as the rest of Sadge)

Generally you will want to use your incrementer in your loop-body in some fashion.
For this purpose it is defined as a variable under the name `Crabsさん`.
This is a fully-fledged variable. So you can use it's value in expressions, assignments, etc. or change it!
The variable will still be available after leaving the for-loop, so long as you remain within the same scope.

On that note, scopes are function bound, not code block bound. I.E. calling a function creates a new scope, leaving the function leaves the scope. At no time can anything outside of the current scope be accessed, not even if it is in a scope "under" the current one.

*Note: function bound means that specific instance/call of the function, you cannot access something from a previous recursion loop, for example.

## Running the interpreter

You can run the interpreter with the following command:

`python source/Sadge.py programFileName.supportedFileExtension arg1 arg2 argEtc. -DTIR`

The arguments you pass after the file name should match the number of arguments your main function expects.

After the arguments you can pass any number of flags prefixed by a __single__ `-` (this means all the flags must be attached).

The following are all current flags and their functionality:

- D, will print "Running lexer.", "Running parser." and "Running code." debug messages, allowing you to see at which stage the interpreter may be failing.
- T, will print how long each of the steps (lexing, parsing and running) took, as well as the total run time.
- L, will print the token list output by the lexer.
- P, will print the list of ASTs output by the parser.
- I, will __actually run the interpreter__. (In future there will also be a compiler, which will be called through the same python file but with the `C` flag)

The main function should be called sadge (all lower case) followed by any of the supported honorifics, although it doesn't matter which. There may only be one function called sadge (even if you use a different honorific, this _will_ mess the interpreter).

You can use any of the following file extensions for your Sadge code files:
- .sadge
- .pain
- .suffering
- .painandsuffering
- .yabe
- .crabs
- .plankton
- .planktonthrowsitback
- .formula
- .theformula

*Note: Depending on where you are running this from, you might need to adjust the directory for Sadge.py, the example is from the perspective of this repo's root.

**Note: Depending on your setup you might need to use the command `python3` instead. This project has been made and tested with python version 3.9.1 but should work on most python3 versions.

***Note: All regular arguments must be passed _before_ the flags, and cannot start with a `-`.

---

The following part is mostly only for that one person who knows the reason behind the endline character :).

## === README CHECKLIST ===

Gekozen taal: Sadge (eigen taal)

Turing-compleet omdat: het (minstens) dezelfde functionaliteit heeft als brainfuck, I.E.
- Een arbitrary hoeveelheid data (variabelen) opslaan en aanpassen
- Flow control in de vorm van
  - If/else statments
  - For loops

---

Code is geschreven in functionele stijl.

---

Taal ondersteunt:

Loops? Ja, Voorbeeld: [examples/print_argument.yabe] - [regels 2-6]

Goto-statements? Nee.

Lambda-calculus? Nee.

---

Bevat:

Classes met inheritance: bijvoorbeeld [source/Tokens.py] - [regel 39]

Object-printing voor elke class: [ja (deels inherited)]

Decorator: functiedefinitie op [source/utilities.py] - [regel 58], toegepast op [source/Interpreter.py] - [230]

Type-annotatie: Haskell-stijl in comments: [ja (behalve de \_\_init\_\_ functies, maar die ontbreken ook in het voorbeeld, dus ik neem dat die niet hoeven)]; 
Python-stijl in functiedefinities: [ja]

Minstens drie toepassingen van hogere-orde functies:

1. [source/AST_classes.py] - [regel 58]

2. [source/Lexer.py] - [regel 16 (de reduce)]

3. [source/Lexer.py] - [regel 16 (de zipWith)]

---

Interpreter-functionaliteit Must-have:

Functies: [~~één per file~~ / __meer per file__]

Functie-parameters kunnen aan de interpreter meegegeven worden door: ze mee te geven op de commandline als bijvoorbeeld:<br/>
`python source/Sadge.py examples/print_argument.yabe 101 5 -DTIR` <br/>
De `101` en `5` zijn hier parameters. De `-DTIR` zijn optie flags, zie __TODO KOPJE OVER OPTIE FLAGS!!!!!!!!!!!!__

Functies kunnen andere functies aanroepen: zie voorbeeld [examples/print_argument.yabe] - [regel 10]

Functie resultaat wordt op de volgende manier weergegeven: Geprint naar de terminal.

---

Interpreter-functionaliteit (should/could-have):

[Gekozen functionaliteit] geïmplementeerd door middel van de volgende functies: a) [functie] in [file] op regel [regel]

[Extra functionaliteit overlegd met docent, goedkeuring: datum e-mail; overeengekomen max. aantal punten: X]