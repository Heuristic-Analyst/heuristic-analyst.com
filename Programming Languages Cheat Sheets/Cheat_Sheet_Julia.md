# 1. Unique Julia Things
- Julia is designed specifically for high-performance scientific computing and data manipulation
- Uses Just-In-Time (JIT) compilation - no explicit compilation step needed
- Multiple dispatch: functions can have different methods based on argument types
- 1-based indexing (unlike i.e. Python's 0-based)
- No explicit class definitions with methods inside - functions are separate from types

# 2. Basic Syntax
```julia
# Variables and basic types
x = 3        # Integer
y = 3.0      # Float64
s = "Hello"  # String
b = true     # Boolean

# Functions - two ways to define
function add(x, y)
    return x + y
end

# One-line function
subtract(x, y) = x - y

# Arrays (1-based indexing!)
arr = [1, 2, 3]           # 1D array
matrix = [1 2; 3 4]       # 2D matrix

# String interpolation with $
name = "Julia"
println("Hello, $name")
```

# 3. Key Features

## Multiple Dispatch
```julia
# Same function name, different types
function process(x::Int64)
    return x + 1
end

function process(x::String)
    return uppercase(x)
end
```

## Type System
```julia
# Declare types
a::Float64 = 3.0

# Create custom type (like a class)
struct Point
    x::Float64
    y::Float64
end

# Create instance
p = Point(1.0, 2.0)
```

## Subtype operator
The `<:` operator in Julia is the subtype operator - it checks if one type is a subtype of another.
```julia
# Basic subtype check
Int64 <: Number        # true  (Int64 is a subtype of Number)
Float64 <: Number      # true  (Float64 is a subtype of Number)
String <: Number       # false (String is not a subtype of Number)

# Common uses in function definitions
# Only accept numeric types
function process_number(x::T) where T <: Number
    return x + 1
end

process_number(1)      # works
process_number(1.0)    # works
process_number("1")    # error: String is not a subtype of Number

# Custom types example
abstract type Animal end
struct Dog <: Animal   # Dog is a subtype of Animal
    name::String
end

# Check relationships
Dog <: Animal         # true
String <: Animal      # false
```

The opposite operator is `>:` which checks if something is a supertype
```julia
Number >: Int64      # true
Animal >: Dog        # true
```

This is particularly useful for:

1. Type constraints in function definitions
2. Generic programming
3. Creating type hierarchies
4. Runtime type checks
## Arrays and Matrix Operations
```julia
# Create arrays
zeros(3)      # [0.0, 0.0, 0.0]
ones(2, 2)    # 2x2 matrix of ones
rand(3, 3)    # Random 3x3 matrix

# Array operations
A = [1 2; 3 4]
B = [5 6; 7 8]
A * B         # Matrix multiplication
A .* B        # Element-wise multiplication
```

## Control Flow
```julia
# Loops
for i in 1:5
    println(i)
end

while condition
    # do something
end

# Conditionals
if x > 0
    println("Positive")
elseif x < 0
    println("Negative")
else
    println("Zero")
end
```

## Package Management
```julia
# Enter package mode with ]
# Add package
] add PackageName

# Use package
using PackageName
```

## File I/O
```julia
# Write to file
open("file.txt", "w") do f
    write(f, "Hello Julia")
end

# Read from file
content = read("file.txt", String)
```

# 4. Unique Julia Features
## Unicode support for variable names
```julia
α = 0.5  # Type \alpha + TAB
β = 2.0  # Type \beta + TAB
```

## Broadcasting with dot syntax
```julia
A = [1, 2, 3]
A .^ 2  # Square each element
```

## Comprehensions
```julia
squares = [x^2 for x in 1:10]
```

## Little Summary
1. Arrays are 1-based indexed (arr[1] is first element)
2. No explicit return needed, but can be - last expression is returned
```julia
function add(a, b)
    a + b
end

result = add(5, 3)
println(result)  # Output: 8

# or 

function add(a, b)
    c = a + b
    return c
end

result = add(5, 3)
println(result)  # Output: 8
```
1. No need for self/this in type methods
2. Functions are not defined inside types/classes
3. Multiple dispatch instead of traditional OOP method overloading
4. Type declarations are optional but can improve performance
5. More functional programming features available out of the box

Julia is particularly good for:

- Scientific computing
- Numerical analysis
- Data science
- High-performance computing
- Mathematical programming

# 5. Keywords
## Modules
`module` - Creates a new module (similar to a namespace)
```julia
# mymath.jl
module MyMath
    # Everything inside here is in the MyMath module
    export add, subtract  # Functions we want to make public
    
    function add(x, y)
        return x + y
    end
    
    function subtract(x, y)
        return x - y
    end
    
    # Helper function (not exported, so private to module)
    function _helper()
        println("I'm a helper function")
    end
end
```

## Export
`export` - Makes names available for importing when using the module
```julia
module MyLibrary
    export MyType, my_function  # These will be available when using MyLibrary
    
    struct MyType
        x::Int
    end
    
    my_function() = println("Hello")
    
    # Not exported, only accessible with MyLibrary._private_function
    _private_function() = println("I'm private")
end
```

## Using
`using` - Imports all exported names from a module into current namespace
```julia
# Main script
using MyMath  # Imports add and subtract
println(add(2, 3))  # Works directly
# _helper() would fail as it's not exported
```

## Import
`import` - More specific than `using`, brings in specific names or requires qualification (Qualification: It refers to whether you need to use the module name as a prefix when calling a function)
```julia
# Different ways to import
import MyMath              # Must use MyMath.add(2, 3)
import MyMath: add        # Can use add(2, 3) directly
import MyMath.add        # Same as above
```

### Qualification
With `using`
```julia
using MathUtils
add(1, 2)          # Works directly - no qualification needed
```

With `import`
```julia
import MathUtils
MathUtils.add(1, 2)  # Must "qualify" with MathUtils. prefix
```

BUT if you do
```julia
import MathUtils: add
add(1, 2)          # Works directly because we specifically imported 'add'
```

## Include
`include` - Loads and runs source from another file
```julia
# utils.jl
function helper_function()
    println("I'm helping!")
end

# main.jl
include("utils.jl")  # Brings in all definitions from utils.jl
helper_function()    # Works because it was included
```

## Using .
`using .` and relative imports
```julia
module ParentModule
    module ChildModule
        export child_function
        child_function() = println("I'm the child")
    end
    
    # Use relative import with dot notation
    using .ChildModule
    
    function parent_function()
        child_function()  # Can use it because we imported it
    end
end
```

# 6. Important patterns and tips:

Module file structure
```julia
# myproject/
#   src/
#     MyProject.jl       # Main module file
#     submodule1.jl      # Submodules
#     submodule2.jl
```

Combining include with modules
```julia
# MyProject.jl
module MyProject
    include("submodule1.jl")
    include("submodule2.jl")
    
    # Can use things from included files here
end
```

Selective importing
```julia
using Statistics: mean, median  # Only import specific functions
using DataFrames: DataFrame    # Only import specific type
```

Re-exporting imported names
```julia
module MyWrapper
    using OtherModule: some_function
    export some_function  # Re-export it for users of MyWrapper
end
```

Handling name conflicts
```julia
# If two modules have the same function name
using Module1
using Module2: function_name as module2_function  # Alias to avoid conflict
```

Submodules
```julia
module MainModule
    module SubModule
        export sub_function
        sub_function() = println("I'm in a submodule")
    end
    
    using .SubModule  # Note the dot for relative import
end
```

# 7. Common practices

1. Keep one module per file for large projects
2. Use clear naming conventions
3. Export only what users of your module need
4. Use underscores for private functions (by convention)
5. Use relative imports within a package
6. Put frequently used code in a module for reuse

The module system is crucial for:

- Organizing large codebases
- Creating reusable packages
- Managing namespaces
- Controlling scope
- Separating implementation details from public interface

using modules is generally the more organized way to structure Julia code. Not recommended way (with just `include`)
```julia
# math_functions.jl
function add(x, y)
    return x + y
end

function subtract(x, y)
    return x - y
end

# main.jl
include("math_functions.jl")
# Functions are just dumped into global namespace
println(add(2, 3))
```

Better way (using modules)
```julia
# math_functions.jl
module MathFunctions
    export add, subtract  # Explicitly choose what to make available
    
    function add(x, y)
        return x + y
    end
    
    function subtract(x, y)
        return x - y
    end
    
    # Helper function that stays private to module
    function _validate(x)
        @assert typeof(x) <: Number
    end
end

# main.jl
using .MathFunctions  # The dot means it's a local module
# or
using MathFunctions  # If it's an installed package

println(add(2, 3))
```

The module approach is better because:

1. It prevents name conflicts (functions are namespaced)
2. Provides clear public/private interface
3. Makes dependencies explicit
4. Follows Julia's package structure conventions

You still might use `include` within modules for organizing large modules
```julia
# MathLib.jl
module MathLib
    # Include implementation files
    include("basic_operations.jl")
    include("advanced_operations.jl")
    
    # Re-export specific functions
    export add, subtract, multiply, divide
end
```


# 8. Project Environments
## Why Use Project Environments?

Project environments in Julia provide several key benefits:

- **Dependency Isolation**: Each project can have its own unique set of packages and versions
- **Reproducibility**: Ensures consistent package configurations across different machines
- **Version Control**: Easily manage and track project-specific dependencies
## Creating a Project Environment

### 1. Initializing a New Project Environment (using Julia REPL)
```julia
# Press ']' to enter Pkg mode
] generate MyProject

# Creates Project.toml in current directory
```
### 2. Activate the Project Environment
```julia
# Press ']' to enter Pkg mode
] activate MyProject
```

### 3. Add Packages to Project Environment
```julia
# Still in Pkg mode
] add DataFrames Plots
] add DataFrames@1.5.0  # Specific version
```

### View Project Status
```julia
# In Pkg mode
] status
```

### Remove Packages
```julia
# In Pkg mode
] rm Plots
```

### Return to Julia Mode
```julia
# Press Backspace or Ctrl+C to exit Pkg mode
```

### Manifest.toml - Instantiate Project
`Pkg.instantiate()` does two critical things:

1. Reads the `Manifest.toml` file in your project
2. Downloads and installs EXACTLY the package versions specified in that manifest file

This ensures:

- Exact reproduction of the project's dependency environment
- Consistent package versions across different machines
- Recreates the precise development setup originally used

Example scenario:

- You share a project with a colleague
- They run `Pkg.instantiate()`
- They get the IDENTICAL package versions you used
- Prevents "works on my machine" dependency issues
```julia
# Back in Julia mode
using Pkg
Pkg.instantiate()  # Installs exact dependencies
```

### Project.toml - Nice to know:
`Project.toml` is a declarative file that:

- Defines project metadata (name, authors, version)
- Lists direct package dependencies
- Specifies minimum/compatible package versions
- Serves as a lightweight, human-readable dependency specification

Key differences from `Manifest.toml`:

- `Project.toml`: High-level, user-specified dependencies
- `Manifest.toml`: Exact, resolved dependencies with precise versions
### Using Project Environment in Code
In your code you first need to activate the project environment. Just write this at the beginning of you code:
```julia
using Pkg
Pkg.activate(".")
```

### Run Project
After writing your whole code, you should open your your cmd/terminal in the HelloWorldProject folder:
```Folder Structure
HelloWorldProject/ 
│ 
├── Project.toml 
├── Manifest.toml 
│ 
├── src/ 
│    └── HelloWorldProject.jl
```

In cmd:
```cmd
C:\Programming\Julia\HelloWorldProject>
```

Write the following code into the cmd/terminal to run this project in the created environment with all of its packages etc: 
```command
julia --project=. "./src/HelloWorldProject.jl"
```
