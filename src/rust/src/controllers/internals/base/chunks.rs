use crate::utils::custom_types::Vector2i;

#[derive(Debug)]
pub struct ChunkProperty {
    max_value: u16,
    value: u16,
    min_value: u16
}

impl ChunkProperty {
    pub fn new(current_value: u16) -> Self {
        return Self {
            value: current_value,
            min_value: current_value,
            max_value: current_value
        }
    }

    pub fn set(&mut self, value: u16) {
        self.value = value;
        self.min_value = if self.min_value < value {self.min_value} else {value};
        self.max_value = if self.max_value < value {value} else {self.max_value};
    }

    pub fn add(&mut self) {
        self.value += 1;
        self.min_value = if self.min_value < self.value {self.min_value} else {self.value};
        self.max_value = if self.max_value < self.value {self.value} else {self.max_value};
    }
    pub fn get(&mut self) -> u16 { self.value }
    pub fn get_max(&mut self) -> u16 { self.max_value }
    pub fn get_min(&mut self) -> u16 { self.min_value }
}


pub trait ChunkDataType {
    fn new_empty() -> Self;
    fn data_changed(&self) -> bool;
    fn set_changed(&mut self, value: bool);
}

pub struct ChunkData {
    data_changed: bool
}

impl ChunkDataType for ChunkData {
    fn new_empty() -> Self {
        return Self {
            data_changed: false,
        };
    }
    
    fn data_changed(&self) -> bool { return self.data_changed; }
    
    fn set_changed(&mut self, value: bool) { self.data_changed = value; }
}


pub trait ChunkLike<ChunkDataType> {
    fn new(pos: Vector2i) -> Self;
    fn new_with_data(pos: Vector2i, data: ChunkDataType) -> Self;

    fn pos(&self) -> &Vector2i;
    fn data(&mut self) -> &mut ChunkDataType;
}

pub struct Chunk {
    position: Vector2i,
    data: ChunkData
}

impl ChunkLike<ChunkData> for Chunk {
    fn new(pos: Vector2i) -> Self {
        return Self {position: pos, data: ChunkData::new_empty()};
    }
    fn new_with_data(pos: Vector2i, data: ChunkData) -> Self {
        return Self {position: pos, data: data}
    }

    fn pos(&self) -> &Vector2i { return &self.position }
    
    fn data(&mut self) -> &mut ChunkData { return &mut self.data; }
}
