use core::panic;
use std::cmp::{max, min};

use display_info::DisplayInfo;

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


pub struct DisplayChunkHolder {
    chunk_grid: ChunkGrid<DisplayChunk>,
    bounds: [Vector2i; 2]
}

impl DisplayChunkHolder {
    pub fn new_from_display(display_list: Vec<usize>, chunk_size: u16) -> Self {
        let mut bounds: [Option<i32>; 4] = [None, Some(0), None, Some(0)];
        let info = DisplayInfo::all().unwrap_or_else(|err| {panic!("Couldn't get display infos | {err}");});
        for (idx, display) in info.iter().enumerate() {
            if !display_list.is_empty() {
                if !display_list.contains(&idx) {
                    continue;
                }
            }
            
            bounds[0] = Some(min(bounds[0].unwrap_or(display.x), display.x));
            bounds[1] = Some(bounds[1].unwrap_or_default() + display.width as i32);

            bounds[2] = Some(min(bounds[2].unwrap_or(display.y), display.y));
            bounds[3] = Some(max(bounds[3].unwrap_or_default(), display.height as i32));
        }

        if display_list.is_empty() {
            bounds[0] = Some(0);
            bounds[2] = Some(0);
        }

        println!("{:?}", bounds);
        return Self {
            chunk_grid: ChunkGrid::new(bounds[1].unwrap() as u16 / chunk_size, bounds[3].unwrap() as u16 / chunk_size),
            bounds: [
                Vector2i::new(bounds[0].unwrap_or_default() as u16, bounds[1].unwrap() as u16), 
                Vector2i::new(bounds[2].unwrap_or_default() as u16, bounds[3].unwrap() as u16)
            ]
        }
    }
}

impl StoresChunkGrid<DisplayChunk, DisplayChunkData> for DisplayChunkHolder {
    type Grid = ChunkGrid<DisplayChunk>;
    type DataType = u16;

    fn new(width: Self::DataType, height: Self::DataType) -> Self {
        return Self { chunk_grid: ChunkGrid::new(width, height), bounds: [Vector2i::new(0, width), Vector2i::new(0, height)] };
    }

    fn get_grid(&self) -> &Self::Grid { return &self.chunk_grid }

    fn get_chunk(&mut self, pos: Vector2i) -> Option<&mut DisplayChunk> {
        return self.chunk_grid.get_chunk_at_pos(pos);
    }
}
