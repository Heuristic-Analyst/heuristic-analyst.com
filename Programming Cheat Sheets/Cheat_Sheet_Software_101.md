# Event-Driven Programming Pattern

*"How most of the software is run, it fist initialising some code, then many callbacks are created, and then a window or something is created that waits until the x button to close the program is pressed and the program is then closed, but until then every callback can be triggered*"

Most software follows this event-driven pattern:
## General Flow

1. Initialize program
2. Set up event listeners (callbacks)
3. Start main loop that waits for events
4. Run until exit condition

## Practical Example

Here's how a simple Julia GUI works:
```julia
# 1. INITIALIZATION
using Pkg
Pkg.activate(".")
import GLMakie as plt

# Create GUI elements
fig = plt.Figure(size = (400, 300))
input_field = plt.Textbox(fig[1, 1])
button = plt.Button(fig[2, 1], label="Print")

# 2. REGISTER CALLBACKS
plt.on(button.clicks) do _
    println(input_field.displayed_string[])
end

# 3. START MAIN EVENT LOOP
wait(display(fig))
# 4. Program runs until window is closed (the "wait" will not close the displayed window unitil the window is closed by the user in this case)
```

## Where You'll See This Pattern

- Desktop apps (like our Julia example)
- Web browsers
- Game engines
- Mobile apps
- Server applications

This structure lets programs respond to user actions (clicks, key presses) or external events (network requests) while staying responsive.
