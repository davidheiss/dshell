class Color:
    def __init__(self, red: float, green: float, blue: float):
        assert 0 <= red <= 1
        assert 0 <= green <= 1
        assert 0 <= blue <= 1
        self.red = red
        self.green = green
        self.blue = blue

    def __add__(self, rhs: "Color"):
        assert isinstance(rhs, Color)
        return Color(
            min(1, self.red + rhs.red),
            min(1, self.green + rhs.green),
            min(1, self.blue + rhs.blue),
        )

    def __mul__(self, rhs: float):
        assert isinstance(rhs, float) or isinstance(rhs,int)

        return Color(
            max(0, min(1, self.red * rhs)),
            max(0, min(1, self.green * rhs)),
            max(0, min(1, self.blue * rhs)),
        )

    def __repr__(self):
        return f"rgb({self.red},{self.green},{self.blue})"

    def __iter__(self):
        yield from (self.red, self.green, self.blue)
