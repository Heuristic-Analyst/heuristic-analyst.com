# 1. Java Basics & Environment

## What is Java?

Java is a high-level, object-oriented programming language designed for platform independence through its "Write Once, Run Anywhere" philosophy.

### Core Components:

- **JDK (Java Development Kit)**: Contains tools for developing Java applications
- **JRE (Java Runtime Environment)**: Required to run Java applications
- **JVM (Java Virtual Machine)**: Executes Java bytecode

### Basic File Types:

- **.java files**: Source code files written by programmers
- **.class files**: Compiled bytecode files that JVM can execute

## Basic Program Structure

Every Java program needs at least one class. Here's the minimal structure:

```java
public class MyProgram {
    public static void main(String[] args) {
        // Program code goes here
    }
}
```

Let's break down each component:

- `public`: Access modifier that makes the class accessible from anywhere
- `class`: Keyword declaring a class
- `MyProgram`: Class name (must match filename MyProgram.java)
- `main`: The entry point method that JVM looks for to start execution
- `static`: Makes method accessible without creating class instance
- `void`: Indicates method returns nothing
- `String[] args`: Command line arguments passed to program

## Java Packages & Imports

### Packages

- Packages are folders that organize related Java classes
- Each .java file must declare its package at the top
- Package names match folder structure
- Common naming: `com.company.project.category`

### Basic Structure Example:
```
src/
├── com.school.students/
│   ├── Student.java         // package com.school.students;
│   └── StudentGrades.java   // package com.school.students;
└── com.school.teachers/
    └── Teacher.java         // package com.school.teachers;
```

## Import Rules

1. No import needed if:
    - Classes are in the same package
    - Using java.lang package (String, System, etc.)
2. Import needed when:
    - Using classes from different packages
    - Using Java library classes

```java
// Ways to import
import com.school.students.Student;     // Single class
import com.school.students.*;           // All classes (not recommended)
```

### Example Usage:
```java
// Student.java
package com.school.students;
public class Student {
    String name;
}

// Teacher.java
package com.school.teachers;
import com.school.students.Student;  // Need import - different package

public class Teacher {
    Student student;  // Can use Student class after import
}

// StudentGrades.java
package com.school.students;
// No import needed - same package as Student
public class StudentGrades {
    Student student;  // Works without import
}
```

## Package Declaration

Packages organize classes into namespaces. Must be first line in file:
```java
package com.example.myproject;
```

## Import Statements

Used to access classes from other packages:
```java
import java.util.Scanner;  // Import specific class
import java.util.*;       // Import all classes from package
```

# 2. Basic Syntax Elements

## Comments

Three types of comments in Java:
```java
// Single line comment

/* Multi-line comment
   spanning multiple lines */

/** JavaDoc comment for documentation
 * @author Name
 * @version 1.0
 */
```

## Statement Termination

Every Java statement must end with a semicolon:
```java
int x = 10;
System.out.println("Hello");
```

## Code Blocks

Code blocks are defined using curly braces {}:
```java
public class Example {
    // Class block
    public void method() {
        // Method block
        if (true) {
            // if statement block
        }
    }
}
```

## Case Sensitivity

Java is case-sensitive. These are all different:
```java
int number = 1;
int Number = 2;
int NUMBER = 3;
```

## Keywords

Reserved words that cannot be used as identifiers:
- Control flow: `if`, `else`, `while`, `for`, `switch`, `case`, etc.
- Data types: `int`, `boolean`, `char`, `double`, etc.
- Access modifiers: `public`, `private`, `protected`
- Class-related: `class`, `interface`, `extends`, `implements`
- Others: `new`, `this`, `super`, `return`, etc.

## Naming Conventions

- Classes: Start with uppercase, CamelCase (Example: `MyClass`)
- Methods and variables: Start with lowercase, camelCase (Example: `myMethod`)
- Constants: All uppercase with underscores (Example: `MAX_VALUE`)
- Packages: All lowercase, separated by dots (Example: `com.example.project`)

## Code Formatting

Best practices for readability:
```java
public class FormattingExample {
    // Indent class members
    private int number;
    
    public void method() {
        // Indent method body
        if (condition) {
            // Further indent nested blocks
            doSomething();
        }
    }
}
```

## Access Modifiers

These determine the visibility and accessibility of classes, methods, and fields:

1. `public`
- Accessible from anywhere
- Any other class can use this
- Most open access level
```java
public class Dog { // Any class can use Dog
    public void bark() { // Any class can call this method
        System.out.println("Woof!");
    }
}
```

Best practices for readability:
```java
public class FormattingExample {
    // Indent class members
    private int number;
    
    public void method() {
        // Indent method body
        if (condition) {
            // Further indent nested blocks
            doSomething();
        }
    }
}
```

2. `private`
- Only accessible within the same class
- Cannot be accessed from outside
- Most restrictive access level
```java
public class BankAccount {
    private double balance; // Only accessible within BankAccount class
    
    private void updateBalance() { // Only callable within BankAccount class
        // balance calculations
    }
}
```

3. `protected`
- Accessible within:
    - Same class
    - Same package
    - Subclasses (even in different packages)
```java
public class Animal {
    protected String name; // Accessible in Animal class and any subclasses
    
    protected void eat() { // Can be used by Animal and its subclasses
        System.out.println("Eating...");
    }
}
```

4. Default (no modifier)
- Package-private access
- Only accessible within same package
- Used when no access modifier is specified
```java
class Helper { // Only classes in same package can use this
    void helperMethod() { // Only accessible within same package
        // code
    }
}
```

## Important Keywords

1. `extends`
- Used for inheritance
- Creates a subclass of another class
- A class can only extend one class
```java
public class Animal {
    protected String name;
    private int age;
    
    public void eat() {
        System.out.println(name + " is eating");
    }
    
    public void sleep() {
        System.out.println(name + " is sleeping");
    }
}

public class Dog extends Animal {
    // Dog inherits name, eat(), and sleep() from Animal
    // but NOT age (because it's private)
    
    // Can add new methods
    public void bark() {
        System.out.println(name + " says Woof!");
    }
    
    // Can override inherited methods
    @Override
    public void eat() {
        System.out.println(name + " is chomping dog food");
    }
}
```

2. `implements`
- Used to implement interfaces: An interface in Java is like a contract or blueprint that defines what a class must be able to do, but not how to do it. Think of it as a list of promises - if a class implements an interface, it's promising to provide certain functionality.
- A class can implement multiple interfaces
```java
// This is an interface
public interface Flyable {
    void takeOff();
    void land();
    void fly();
}

// A class implementing the interface
public class Bird implements Flyable {
    // Must provide ALL these methods
    public void takeOff() {
        // Bird-specific takeoff code
    }
    
    public void land() {
        // Bird-specific landing code
    }
    
    public void fly() {
        // Bird-specific flying code
    }
}
```

3. `this`
- References the current object
- Used to:
    - Differentiate between field and parameter names
    - Call another constructor
```java
public class Student {
    private String name;
    
    public Student(String name) {
        this.name = name; // this.name refers to field, name refers to parameter
    }
}
```

4. `super`
- References the parent class
- Used to:
    - Call parent class methods
    - Call parent class constructor
```java
public class Dog extends Animal {
    public Dog(String name) {
        super(name); // Call Animal's constructor
    }
    
    public void makeSound() {
        super.makeSound(); // Call Animal's makeSound method
        System.out.println("Woof!");
    }
}
```

5. `static`
- Belongs to the class rather than any instance
- Shared among all instances of a class

Think of a school class with multiple students. Each student (instance) has their own name and age (non-static variables), but they all share the same classroom number (static variable).
```java
public class Counter {
    private static int count = 0; // Shared by all Counter objects
    
    public static void increment() { // Can be called without creating Counter object
        count++;
    }
}
```

The static counter is created only once when the class is first loaded into memory, not each time you create a new object:
```java
public class Counter {
    private static int count = 0;  // Created ONCE when class loads
    
    public Counter() {
        // Constructor doesn't affect static count
    }
    
    public static void increment() {
        count++;
    }
    
    public static int getCount() {
        return count;
    }
}
```

```java
System.out.println(Counter.getCount());  // Prints: 0

Counter c1 = new Counter();
Counter.increment();
System.out.println(Counter.getCount());  // Prints: 1

Counter c2 = new Counter();
Counter.increment();
System.out.println(Counter.getCount());  // Prints: 2

// Both c1 and c2 see the same count
System.out.println(Counter.getCount());  // Still 2
```

6. `final`
- On class: Cannot be inherited
- On method: Cannot be overridden
- On variable: Cannot be changed after initialization
```java
public final class Math { // Cannot be inherited
    public final double PI = 3.14159; // Cannot be changed
    
    public final void calculate() { // Cannot be overridden
        // calculation
    }
}
```

7. `abstract`

- Can be applied to:
    - Classes: Cannot be instantiated, may have abstract methods
    - Methods: No implementation, must be implemented by non-abstract subclasses
```java
public abstract class Shape { // Cannot create Shape object directly
    abstract double getArea(); // No implementation here
    
    public void display() { // Regular method with implementation
        System.out.println("Area: " + getArea());
    }
}

public class Circle extends Shape {
    private double radius;
    
    @Override
    double getArea() { // Must implement abstract method
        return Math.PI * radius * radius;
    }
}
```
1. `Shape` is an abstract template that says:
    - You can't create just a "Shape" (what shape would it even be?)
    - Every shape MUST have a way to calculate its area (that's why getArea() is abstract)
    - Every shape can display its area (using the normal display() method)
2. `Circle` uses this Shape template:
    - It MUST provide the getArea() calculation (which it does using π * r * r)
    - It can use the display() method that Shape already defined

8. `new`

- Creates new instances of classes
- Allocates memory and initializes object
```java
Dog myDog = new Dog("Rex"); // Creates new Dog object
```

## Java Memory Management

### Garbage Collection

- Automatically frees memory from unused objects
- No manual memory management needed (no `free()` or `delete`)
- Runs automatically when Java decides to run it
- Cleans up objects that are no longer referenced

### When Objects Become Eligible for Garbage Collection

1. When references go out of scope:
```java
{
    Dog dog = new Dog("Rex");
} // dog can be garbage collected here
```

2. When references are set to null:
```java
Dog dog = new Dog("Rex");
dog = null; // original Dog object can be garbage collected
```

3. When references are reassigned:
```java
Dog dog = new Dog("Rex");
dog = new Dog("Max"); // "Rex" Dog can be garbage collected
```

### Primitive Variables

- Don't need garbage collection
- Stored on the stack (not heap)
- Automatically cleaned up when they go out of scope
```java
void example() {
    int x = 5;
    {
        int y = 10;
    } // y is cleaned up here
} // x is cleaned up here
```

### Best Practices

- Set objects to null if you're done with them
- Don't rely on specific garbage collection timing
- Close resources properly (files, database connections)
- Let Java handle the memory management automatically

# 3. Variables & Data Types

## Variable Declaration Syntax

Basic format: `type variableName = value;`
```java
int age = 25;        // Declare and initialize
double price;        // Declare only
price = 19.99;      // Initialize later
```

## Primitive Data Types

### Integer Types
```java
byte smallNumber = 127;          // 8-bit, range -128 to 127
short mediumNumber = 32767;      // 16-bit, range -32,768 to 32,767
int standardNumber = 2147483647; // 32-bit, most common
long largeNumber = 9223372036854775807L; // 64-bit, note the 'L' suffix
```

### Floating Point Types
```java
float decimalNumber = 3.14f;     // 32-bit, note the 'f' suffix
double preciseNumber = 3.14159;  // 64-bit, default for decimals
```

### Character Type
```java
char singleCharacter = 'A';      // 16-bit Unicode character
```

### Boolean Types
```java
boolean isTrue = true;           // Can only be true or false
```

## Reference Types (Objectives)

### String
```java
String text = "Hello World";     // String of characters
String emptyText = "";          // Empty string
String nullString = null;       // No string object
// because strings are technically objects, one can declare them this way:
String str = new String("Hello");
```

### Java Strings vs StringBuilder

String (Immutable)
```java
String text = "Hello World";     // String of characters
String emptyText = "";          // Empty string
String nullString = null;       // No string object
// because strings are technically objects, one can declare them this way:
String str = new String("Hello");

### Arrays
```java
int[] numbers = new int[5];     // Array of 5 integers
String[] names = {"John", "Jane", "Bob"}; // Array initialization
```

StringBuilder (Mutable)
```java
// Creation
StringBuilder str = new StringBuilder("Hello");

// Modifications (same object)
str.append(" World");                    // Modifies in place
str.insert(0, "Say: ");                  // Inserts at position
str.replace(5, 10, "Hi");               // Replaces range
str.deleteCharAt(0);                     // Deletes character
str.reverse();                           // Reverses string

// Convert to String when done
String finalString = str.toString();
```

Performance Impact
```java
String str = "Hello";
str = str + " World";     // Creates new String object
str = str + " Again";     // Creates another new String object
```

Each modification created a new object! If you're doing this in a loop 1000 times, you're creating 1000 new objects.

With StringBuilder, you modify the same object:
```java
StringBuilder str = new StringBuilder("Hello");
str.append(" World");     // Modifies same object
str.append(" Again");     // Still same object
```

When to Use What
- **String**: For text that won't change
- **StringBuilder**: For frequent modifications, especially in loops
- **StringBuffer**: Same as StringBuilder but thread-safe (slower)

Memory Management
- Java handles memory automatically through garbage collection
- Old String objects are automatically cleaned up when no longer referenced
- No manual memory management needed

### Objects
```java
Scanner scanner = new Scanner(System.in); // Object creation
```
## Type Casting

### Implicit Casting (Widening)

Automatic conversion to larger type:
```java
int smallNumber = 100;
long bigNumber = smallNumber;    // int to long
```

### Explicit Casting (Narrowing)

Manual conversion to smaller type:
```java
double decimal = 9.99;
int whole = (int) decimal;       // double to int, loses decimal part
```
### Constants

Using the `final` keyword:
```java
final double PI = 3.14159;       // Cannot be changed
final String COMPANY_NAME = "TechCorp";
```

## Variable Scope

### Class Level (Fields)
```java
public class ScopeExample {
    private int classVariable;    // Available to whole class
    
    public void method() {
        classVariable = 10;       // Can use here
    }
}
```

Method Level (Local)
```java
public void method() {
    int localVariable = 5;        // Only available in this method
}
```

Block Level
```java
if (true) {
    int blockVariable = 3;        // Only available in this block
}
// blockVariable not accessible here
```

# 4. Operators

## Assignment Operators
```java
// Basic Assignment
int x = 10;             // Assigns 10 to x

// Compound Assignment
x += 5;                 // Same as: x = x + 5
x -= 3;                 // Same as: x = x - 3
x *= 2;                 // Same as: x = x * 2
x /= 4;                 // Same as: x = x / 4
x %= 3;                 // Same as: x = x % 3
```

## Arithmetic Operators
```java
int a = 10, b = 3;

int sum = a + b;        // Addition: 13
int diff = a - b;       // Subtraction: 7
int product = a * b;    // Multiplication: 30
int quotient = a / b;   // Division: 3 (integer division)
int remainder = a % b;  // Modulus: 1 (remainder of division)
```

## Increment/Decrement Operators
```java
int count = 5;
count++;                // Post-increment: use then add 1
++count;                // Pre-increment: add 1 then use
count--;                // Post-decrement: use then subtract 1
--count;                // Pre-decrement: subtract 1 then use

// Example of difference:
int a = 5;
int b = a++;            // b = 5, then a becomes 6
int c = ++a;            // a becomes 7, then c = 7
```

## Comparison Operators
```java
int x = 5, y = 10;

boolean equal = x == y;          // Equal to: false
boolean notEqual = x != y;       // Not equal to: true
boolean greater = x > y;         // Greater than: false
boolean less = x < y;            // Less than: true
boolean greaterEqual = x >= y;   // Greater than or equal to: false
boolean lessEqual = x <= y;      // Less than or equal to: true
```

## Logical Operators
```java
boolean a = true, b = false;

boolean and = a && b;            // Logical AND: false
boolean or = a || b;             // Logical OR: true
boolean not = !a;                // Logical NOT: false

// Short-circuit evaluation
boolean result = (x > 0) && (y/x > 1);  // Second part only evaluated if x > 0
```

## Operator Precedence

Order of operations (from highest to lowest):

1. Increment/Decrement (++, --)
2. Arithmetic (*, /, %)
3. Arithmetic (+, -)
4. Relational (<, >, <=, >=)
5. Equality (`==, !=)
6. Logical AND (&&)
7. Logical OR (||)
8. Assignment (=, +=, -=, etc.)

Example:
```java
// Complex expression
int result = 5 + 3 * 2;          // Result is 11, not 16
                                 // Multiplication happens before addition

// Using parentheses to change precedence
int result2 = (5 + 3) * 2;       // Result is 16
                                 // Parentheses force addition first
```

# 5. Control Flow

## IF Statements

### Basic if Statement
```java
if (condition) {
    // Code executed if condition is true
}
```
### if-else Statement
```java
if (grade >= 90) {
    System.out.println("A");
} else if (grade >= 80) {
    System.out.println("B");
} else if (grade >= 70) {
    System.out.println("C");
} else {
    System.out.println("F");
}
```

### Nested if Statements
```java
if (age >= 18) {
    if (hasLicense) {
        System.out.println("Can drive");
    } else {
        System.out.println("Need license");
    }
} else {
    System.out.println("Too young");
}
```

### Ternary Operator

Shorthand for simple if-else:
```java
// syntax: condition ? valueIfTrue : valueIfFalse
int age = 20;
String status = age >= 18 ? "Adult" : "Minor";
```

## Loops

### For Loop

Basic structure:
```java
// for (initialization; condition; update)
for (int i = 0; i < 5; i++) {
    System.out.println(i);
}
```

### Enhanced For Loop (For-Each)

Used for arrays and collections:
```java
int[] numbers = {1, 2, 3, 4, 5};
for (int num : numbers) {
    System.out.println(num);
}
```

While Loop
```java
int count = 0;
while (count < 5) {
    System.out.println(count);
    count++;
}
```

### Do-While Loop

Executes at least once:
```java
int x = 0;
do {
    System.out.println(x);
    x++;
} while (x < 5);
```

Loop Control
```java
// Break statement - exits loop
for (int i = 0; i < 10; i++) {
    if (i == 5) {
        break;      // Exit loop when i equals 5
    }
}

// Continue statement - skips rest of current iteration
for (int i = 0; i < 5; i++) {
    if (i == 2) {
        continue;   // Skip printing 2
    }
    System.out.println(i);
}

// Nested loops
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        System.out.println("i=" + i + ", j=" + j);
    }
}
```

Infinite Loops (and how to avoid them)
```java
// Infinite loop - needs break condition
while (true) {
    if (someCondition) {
        break;
    }
}

// Common mistake - forgot to increment
for (int i = 0; i < 5; ) {  // Missing i++
    System.out.println("Infinite!");
}
```

# 6. Random Numbers, Casting, and Field Variables

## Random Number Generation

### Using Math.random()
```java
// Returns double between 0.0 (inclusive) and 1.0 (exclusive)
double randomDecimal = Math.random();

// Generate random int between 0 and n-1
int n = 10;
int randomInt = (int)(Math.random() * n);

// Generate random int between min and max
int min = 5;
int max = 10;
int randomRange = (int)(Math.random() * (max - min + 1)) + min;
```

### Using Random Class
```java
import java.util.Random;

Random rand = new Random();

// Generate random integers
int number = rand.nextInt(100);    // 0 to 99
int rangeNumber = rand.nextInt(50, 100);  // 50 to 99

// Generate random doubles
double decimal = rand.nextDouble();  // 0.0 to 1.0
double rangeDecimal = rand.nextDouble(10.0);  // 0.0 to 10.0

// Generate random booleans
boolean randomBool = rand.nextBoolean();
```

## Type Casting

### Primitive Type Casting

### Widening (Implicit Casting)
```java
// Automatic casting - no data loss
byte smallNum = 10;
int bigNum = smallNum;      // byte to int
long biggerNum = bigNum;    // int to long
float decimal = biggerNum;  // long to float
double bigDecimal = decimal;// float to double
```

### Narrowing (Explicit Casting)
```java
// Manual casting - possible data loss
double bigDecimal = 100.99;
float decimal = (float)bigDecimal;  // double to float
long bigNum = (long)decimal;        // float to long
int num = (int)bigNum;             // long to int
short smallNum = (short)num;        // int to short
byte tinyNum = (byte)smallNum;      // short to byte
```

## Object Type Casting

## Upcasting (Widening Reference Conversion)
```java
class Animal { }
class Dog extends Animal { }

// Implicit upcast
Dog dog = new Dog();
Animal animal = dog;  // Dog to Animal
```

## Downcasting (Narrowing Reference Conversion)
```java
// Explicit downcast - requires check
if (animal instanceof Dog) {
    Dog dog = (Dog)animal;  // Animal to Dog
}
```

## Field Variables (Class Variables)

### Instance Variables
```java
public class Student {
    // Instance variables - unique for each object
    private String name;
    private int age;
    private double gpa;
    
    // Constructor
    public Student(String name, int age, double gpa) {
        this.name = name;  // 'this' refers to instance variable
        this.age = age;
        this.gpa = gpa;
    }
}
```

### Static Fields (Class Variables)
```java
public class School {
    // Static variable - shared by all instances
    private static int totalStudents = 0;
    
    // Instance variable
    private String name;
    
    public School(String name) {
        this.name = name;
        totalStudents++;  // Increment shared counter
    }
    
    // Static method to access static variable
    public static int getTotalStudents() {
        return totalStudents;
    }
}
```

### Final Fields (Constants)
```java
public class MathConstants {
    // Constants - static final fields
    public static final double PI = 3.14159;
    public static final double E = 2.71828;
    
    // Instance final field - must be initialized
    private final String id;
    
    public MathConstants(String id) {
        this.id = id;  // Can only be set once
    }
}
```

# 7. Methods

## Method Declaration Syntax
```java
// Basic method structure
accessModifier returnType methodName(parameterType parameterName) {
    // Method body
    return value;  // if return type isn't void
}
```

## Access Modifiers
```java
public class MethodExample {
    // Public - accessible from anywhere
    public void publicMethod() { }
    
    // Private - only accessible within this class
    private void privateMethod() { }
    
    // Protected - accessible in same package and subclasses
    protected void protectedMethod() { }
    
    // Default (no modifier) - only accessible in same package
    void defaultMethod() { }
}
```

## Return Types
```java
// Method returning nothing (void)
public void printMessage() {
    System.out.println("Hello");
}

// Method returning int
public int add(int a, int b) {
    return a + b;
}

// Method returning String
public String getName() {
    return "John";
}

// Method returning boolean
public boolean isAdult(int age) {
    return age >= 18;
}
```

## Parameters
```java
// No parameters
public void sayHello() {
    System.out.println("Hello!");
}

// Single parameter
public void greet(String name) {
    System.out.println("Hello, " + name);
}

// Multiple parameters
public double calculateArea(double length, double width) {
    return length * width;
}

// Variable number of parameters (varargs)
public int sum(int... numbers) {
    int total = 0;
    for (int num : numbers) {
        total += num;
    }
    return total;
}
```

## Method Overloading
```java
public class Calculator {
    // Method overloading - same name, different parameters
    public int add(int a, int b) {
        return a + b;
    }
    
    public double add(double a, double b) {
        return a + b;
    }
    
    public int add(int a, int b, int c) {
        return a + b + c;
    }
}
```

## Static Methods
```java
public class MathHelper {
    // Static method - can be called without class instance
    public static double square(double number) {
        return number * number;
    }
    
    // Usage:
    // double result = MathHelper.square(5);
}
```

## Method Documentation (JavaDoc)
```java
/**
 * Calculates the average of an array of numbers.
 * 
 * @param numbers The array of numbers to average
 * @return The average value, or 0 if array is empty
 * @throws IllegalArgumentException if numbers is null
 */
public double calculateAverage(double[] numbers) {
    if (numbers == null) {
        throw new IllegalArgumentException("Array cannot be null");
    }
    if (numbers.length == 0) {
        return 0;
    }
    double sum = 0;
    for (double num : numbers) {
        sum += num;
    }
    return sum / numbers.length;
}
```

## Best Practices
```java
public class MethodBestPractices {
    // Keep methods short and focused
    // Use meaningful names
    public void sendEmail(String recipient, String subject, String body) {
        validateEmailAddress(recipient);
        createEmailContent(subject, body);
        deliver();
    }
    
    // Break complex methods into smaller ones
    private void validateEmailAddress(String email) {
        // Validation logic
    }
    
    // Handle exceptions appropriately
    public void processData(String data) {
        try {
            // Process data
        } catch (Exception e) {
            // Handle error
            logError(e);
            throw new RuntimeException("Data processing failed", e);
        }
    }
}
```

# 8. Object-Oriented Programming

## Classes
```java
// Basic class structure
public class Student {
    // Instance variables (fields)
    private String name;
    private int age;
    
    // Constructor
    public Student(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // Methods
    public void study() {
        System.out.println(name + " is studying");
    }
}
```

## Constructors
```java
public class Car {
    private String brand;
    private String model;
    
    // Default constructor - must be same name as class!
    public Car() {
        brand = "Unknown";
        model = "Unknown";
    }
    
    // Parameterized constructor
    public Car(String brand, String model) {
        this.brand = brand;
        this.model = model;
    }
    
    // Constructor overloading
    public Car(String brand) {
        this(brand, "Unknown");  // Call another constructor
    }
}
```

## this Keyword
```java
public class Person {
    private String name;
    
    public Person(String name) {
        this.name = name;    // this refers to instance variable
    }
    
    public void printInfo() {
        System.out.println(this.name);  // Explicit use of this
    }
}
```

## Object Creation and Usage
```java
// Creating objects
Student student1 = new Student("John", 20);
Student student2 = new Student("Jane", 21);

// Using objects
student1.study();
student2.study();
```

## Inheritance
```java
// Base class (superclass)
public class Animal {
    protected String name;
    
    public Animal(String name) {
        this.name = name;
    }
    
    public void makeSound() {
        System.out.println("Some sound");
    }
}

// Derived class (subclass)
public class Dog extends Animal {
    private String breed;
    
    public Dog(String name, String breed) {
        super(name);  // Call superclass constructor
        this.breed = breed;
    }
    
    @Override
    public void makeSound() {
        System.out.println("Woof!");
    }
}
```

## Method Overriding with @Override
`@Override` is an annotation in Java that tells the compiler you intend to override (rewrite) a method from the parent class. It's like saying "I'm deliberately changing how this inherited method works."
```java
public class Animal {
    public void makeSound() {
        System.out.println("Some generic sound");
    }
}

public class Dog extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Woof!");
    }
}
```

## Abstract Classes
```java
public abstract class Shape {
    // Abstract method - no implementation
    public abstract double calculateArea();
    
    // Concrete method - has implementation
    public void display() {
        System.out.println("Area is: " + calculateArea());
    }
}

// Concrete class implementing abstract class
public class Circle extends Shape {
    private double radius;
    
    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}
```

## Interfaces
```java
public interface Flyable {
    void fly();  // Abstract method
    
    // Default method (Java 8+)
    default void glide() {
        System.out.println("Gliding");
    }
}

public class Bird implements Flyable {
    @Override
    public void fly() {
        System.out.println("Bird is flying");
    }
}
```

## Encapsulation
```java
public class BankAccount {
    private double balance;  // Private field
    
    // Public getters and setters
    public double getBalance() {
        return balance;
    }
    
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }
}
```

# 9. Collections & Data Structures

## Arrays
```java
// Array declaration and initialization
int[] numbers = new int[5];         // Fixed size array
String[] names = {"John", "Jane"};   // Array with values

// Accessing elements
numbers[0] = 10;                     // Set first element
int firstNumber = numbers[0];        // Get first element

// Array operations
for (int i = 0; i < numbers.length; i++) {
    System.out.println(numbers[i]);
}

// Multi-dimensional arrays
int[][] matrix = new int[3][3];      // 3x3 matrix
matrix[0][0] = 1;                    // Set element
```

## Linked Lists
```java
public class Node<T> {
    T data;              // Generic data type
    Node<T> next;        // Reference to next node
    
    public Node(T data) {
        this.data = data;
        this.next = null;
    }
}

public class LinkedList<T> {
    private Node<T> head;    // First node
    private int size;        // List size
    
    // Add element to end
    public void add(T data) {
        Node<T> newNode = new Node<>(data);
        
        if (head == null) {
            head = newNode;
        } else {
            Node<T> current = head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = newNode;
        }
        size++;
    }
    
    // Remove element
    public boolean remove(T data) {
        if (head == null) return false;
        
        if (head.data.equals(data)) {
            head = head.next;
            size--;
            return true;
        }
        
        Node<T> current = head;
        while (current.next != null) {
            if (current.next.data.equals(data)) {
                current.next = current.next.next;
                size--;
                return true;
            }
            current = current.next;
        }
        return false;
    }
    
    // Get element at index
    public T get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        
        Node<T> current = head;
        for (int i = 0; i < index; i++) {
            current = current.next;
        }
        return current.data;
    }
}
```

## Vector Implementation
```java
public class Vector<T> {
    private Object[] elements;
    private int size;
    private static final int DEFAULT_CAPACITY = 10;
    
    public Vector() {
        elements = new Object[DEFAULT_CAPACITY];
    }
    
    // Add element
    public void add(T element) {
        ensureCapacity();
        elements[size++] = element;
    }
    
    // Get element
    @SuppressWarnings("unchecked")
    public T get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        return (T) elements[index];
    }
    
    // Increase array size if needed
    private void ensureCapacity() {
        if (size == elements.length) {
            Object[] newElements = new Object[elements.length * 2];
            System.arraycopy(elements, 0, newElements, 0, size);
            elements = newElements;
        }
    }
}
```

# 10. File Operations & Input/Output

## Console Input with Scanner
```java
import java.util.Scanner;

// Create Scanner object
Scanner scanner = new Scanner(System.in);

// Reading different types of input
System.out.print("Enter your name: ");
String name = scanner.nextLine();     // Read whole line

System.out.print("Enter your age: ");
int age = scanner.nextInt();          // Read integer

System.out.print("Enter your height: ");
double height = scanner.nextDouble();  // Read double

// Remember to close Scanner
scanner.close();
```

## File Reading
```java
// Reading text file with BufferedReader
import java.io.BufferedReader;
import java.io.FileReader;

try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    System.out.println("Error reading file: " + e.getMessage());
}

// Reading with Scanner
try (Scanner fileScanner = new Scanner(new File("file.txt"))) {
    while (fileScanner.hasNextLine()) {
        String line = fileScanner.nextLine();
        System.out.println(line);
    }
} catch (FileNotFoundException e) {
    System.out.println("File not found: " + e.getMessage());
}
```

## File Writing
```java
// Writing with BufferedWriter
import java.io.BufferedWriter;
import java.io.FileWriter;

try (BufferedWriter writer = new BufferedWriter(new FileWriter("output.txt"))) {
    writer.write("Hello World!");
    writer.newLine();  // Add new line
    writer.write("Another line");
} catch (IOException e) {
    System.out.println("Error writing to file: " + e.getMessage());
}

// Writing with PrintWriter
import java.io.PrintWriter;

try (PrintWriter writer = new PrintWriter("output.txt")) {
    writer.println("Hello World!");  // Writes line with newline
    writer.print("No newline");      // Writes without newline
} catch (FileNotFoundException e) {
    System.out.println("Error creating file: " + e.getMessage());
}
```

## Exception Handling
```java
// Basic try-catch
try {
    // Code that might throw exception
    int result = 10 / 0;
} catch (ArithmeticException e) {
    // Handle specific exception
    System.out.println("Cannot divide by zero!");
} catch (Exception e) {
    // Handle any other exception
    System.out.println("An error occurred: " + e.getMessage());
} finally {
    // Always executed
    System.out.println("This always runs");
}

// Try-with-resources (automatically closes resources)
try (FileReader fr = new FileReader("file.txt");
     BufferedReader br = new BufferedReader(fr)) {
    // Use the resources
    String line = br.readLine();
} catch (IOException e) {
    // Handle exceptions
    e.printStackTrace();
}
```


# 11. Basic GUI with Netbeans

## Basic Components Setup
```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class SimpleGUI extends JFrame {
    // Declare components
    private JPanel panel;
    private JButton button;
    private JLabel label;
    private JSlider slider;

    public SimpleGUI() {
        // Initialize frame
        setTitle("Simple GUI");
        setSize(300, 200);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        // Create and setup components
        initComponents();
    }

    private void initComponents() {
        // Create panel
        panel = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                // Custom painting code here
            }
        };
    }
}
```

## Graphics Drawing
```java
// Custom painting in panel
public class DrawingPanel extends JPanel {
    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        
        // Set drawing color
        g.setColor(Color.RED);
        
        // Draw shapes
        g.fillRect(10, 10, 100, 50);    // Filled rectangle
        g.drawOval(120, 10, 50, 50);    // Circle outline
        
        // Draw text
        g.setColor(Color.BLUE);
        g.drawString("Hello GUI!", 50, 100);
    }
}
```


## Event Handling
```java
// Button click event
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        // Handle button click
        label.setText("Button clicked!");
    }
});

// Slider change event
slider.addChangeListener(new ChangeListener() {
    @Override
    public void stateChanged(ChangeEvent e) {
        int value = slider.getValue();
        label.setText("Value: " + value);
        panel.repaint();  // Request repaint
    }
});
```

## Complete GUI Example
```java
public class CompleteGUI extends JFrame {
    private JPanel drawingPanel;
    private JSlider heightSlider;
    private JLabel valueLabel;

    public CompleteGUI() {
        setTitle("Drawing Application");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        // Create components
        drawingPanel = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                // Draw rectangle based on slider value
                int height = heightSlider.getValue();
                g.setColor(Color.RED);
                g.fillRect(50, getHeight() - height, 
                          100, height);
            }
        };
        
        heightSlider = new JSlider(0, 100, 50);
        valueLabel = new JLabel("Height: 50");
        
        // Layout
        setLayout(new BorderLayout());
        add(drawingPanel, BorderLayout.CENTER);
        add(heightSlider, BorderLayout.SOUTH);
        add(valueLabel, BorderLayout.NORTH);
        
        // Add event listeners
        heightSlider.addChangeListener(e -> {
            int value = heightSlider.getValue();
            valueLabel.setText("Height: " + value);
            drawingPanel.repaint();
        });
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new CompleteGUI().setVisible(true);
        });
    }
}
```
