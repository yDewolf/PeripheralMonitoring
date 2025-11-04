pub trait Position {
    fn x(&self) -> u16;
    fn y(&self) -> u16;
}

#[derive(Debug)]
pub struct Vector2i {
    x: u16,
    y: u16
}

impl Vector2i {
    pub fn new(x: u16, y: u16) -> Self {
        Self {
            x: x,
            y: y
        }
    }
}

impl Position for Vector2i {
    fn x(&self) -> u16 { return self.x }
    fn y(&self) -> u16 { return self.y }
}
