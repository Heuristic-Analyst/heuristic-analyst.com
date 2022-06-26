from NewtonsMethod import newtons_method as newtons_method


if __name__ == "__main__":
    sqrtTwo = newtons_method(iterations=5)
    print("Approximate sqrt(2):", sqrtTwo)
