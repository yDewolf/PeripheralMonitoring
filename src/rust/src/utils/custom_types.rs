pub trait Position {
    fn x(&self) -> u16;
    fn y(&self) -> u16;
}

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

// pub struct SizedMatrix<T: Sized> {
//     data: Vec<T>,
//     n_rows: usize,
//     n_cols: usize
// }

// pub trait Matrix<T> {
//     fn new(n_rows: usize, n_cols: usize) -> Self;

//     fn get_value(x: usize, y: usize) -> T;
//     fn get_value_at(pos: Vector2i) -> T;
// }
