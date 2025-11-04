use crate::controllers::internals::base::chunk_holder::{ChunkGrid, ChunkGridLike, StoresChunkGrid};
use crate::controllers::internals::base::chunks::{ChunkDataType, ChunkLike, ChunkProperty};
use crate::utils::custom_types::{Vector2i};

pub struct DisplayChunkData {
    times_hovered: ChunkProperty,
    hover_time: ChunkProperty,
    idle_time: ChunkProperty,
    data_changed: bool
}

impl DisplayChunkData {
    pub fn times_hovered(&mut self) -> &mut ChunkProperty { return &mut self.times_hovered; }
    pub fn hover_time(&mut self) -> &mut ChunkProperty { return &mut self.hover_time; }
    pub fn idle_time(&mut self) -> &mut ChunkProperty { return &mut self.idle_time; }
}

impl ChunkDataType for DisplayChunkData {
    fn new_empty() -> Self {
        return Self {
            times_hovered: ChunkProperty::new(0),
            hover_time: ChunkProperty::new(0),
            idle_time: ChunkProperty::new(0),
            data_changed: false,
        };
    }
    
    fn data_changed(&self) -> bool { return self.data_changed; }
    
    fn set_changed(&mut self, value: bool) { self.data_changed = value; }
}

pub struct DisplayChunk {
    position: Vector2i,
    data: DisplayChunkData,
}

impl ChunkLike<DisplayChunkData> for DisplayChunk {
    fn new(pos: Vector2i) -> Self {
        return Self {position: pos, data: DisplayChunkData::new_empty()};
    }

    fn new_with_data(pos: Vector2i, data: DisplayChunkData) -> Self {
        return Self {position: pos, data: data};
    }

    fn pos(&self) -> &Vector2i { return &self.position; }

    fn data(&mut self) -> &mut DisplayChunkData { return &mut self.data; }
}


pub struct DisplayChunkController {
    chunk_grid: ChunkGrid<DisplayChunk>
}

impl StoresChunkGrid<DisplayChunk, DisplayChunkData> for DisplayChunkController {
    type Grid = ChunkGrid<DisplayChunk>;
    type DataType = u16;

    fn new(width: Self::DataType, height: Self::DataType) -> Self {
        return Self { chunk_grid: ChunkGrid::new(width, height) };
    }

    fn get_grid(&self) -> &Self::Grid { return &self.chunk_grid }

    fn get_chunk(&mut self, pos: Vector2i) -> Option<&mut DisplayChunk> {
        return self.chunk_grid.get_chunk_at_pos(pos);
    }
}

impl DisplayChunkController {
    pub fn new_from_display() -> Self {
        let mut width = 0;
        let mut height = 0;
        // TODO set width and height using display sizes

        return Self {
            chunk_grid: ChunkGrid::new(width, height)
        }
    }
}