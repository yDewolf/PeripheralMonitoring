use std::ops::Add;

use crate::controllers::internals::base::chunks::{Chunk, ChunkData, ChunkDataType, ChunkLike};
use crate::utils::custom_types::{Position, Vector2i};

pub trait ChunkGridLike<ChunkType, CDataType> where ChunkType: ChunkLike<CDataType>, CDataType: ChunkDataType {
    type DataType: Add<Output = Self::DataType>;

    fn new(width: Self::DataType, height: Self::DataType) -> Self;

    fn get_chunk_at_pos(&mut self, pos: &Vector2i) -> Option<&mut ChunkType>;
    fn get_chunk_at(&mut self, x: Self::DataType, y: Self::DataType) -> Option<&mut ChunkType>;

    fn grid_size(&self) -> &Vector2i;
    
    fn pos_to_index(&self, x: Self::DataType, y: Self::DataType) -> Self::DataType;
    // fn get_chunks(&self) -> &Vec<Self::ChunkType>;
}

pub struct ChunkGrid<ChunkType> {
    pub(crate) data: Vec<ChunkType>,
    pub(crate) grid_size: Vector2i
}

impl<T, D> ChunkGridLike<T, D> for ChunkGrid<T> where T: ChunkLike<D>, D: ChunkDataType {
    type DataType = u16;

    fn new(width: Self::DataType, height: Self::DataType) -> Self {
        let mut data: Vec<T>  = Vec::new();
        for x in 0..width {
            for y in 0..height {
                data.push(T::new(Vector2i::new(x, y)));
            }
        }

        return Self {
            grid_size: Vector2i::new(width as u16, height as u16),
            data: data
        }
    }

    fn get_chunk_at_pos(&mut self, pos: &Vector2i) -> Option<&mut T> {
        return self.get_chunk_at(pos.x(), pos.y());
    }

    fn get_chunk_at(&mut self, x: Self::DataType, y: Self::DataType) -> Option<&mut T> {
        if x > self.grid_size.x() { return None; }
        if y > self.grid_size.y() { return None; }

        let idx = self.pos_to_index(x, y) as usize;
        return Some(&mut self.data[idx]);
    }

    fn grid_size(&self) -> &Vector2i { return &self.grid_size; }
    
    fn pos_to_index(&self, x: Self::DataType, y: Self::DataType) -> Self::DataType { return x + (y * self.grid_size.y())}
}

// Idk if this is recommended but it is incredibly sophisticated implementation of inheritance
// this was my first experience doing that. I loved it
pub trait StoresChunkGrid<ChunkType, CDataType> where ChunkType: ChunkLike<CDataType>, CDataType: ChunkDataType {
    type Grid: ChunkGridLike<ChunkType, CDataType>;
    type DataType: Add<Output = Self::DataType>;

    fn new(width: Self::DataType, height: Self::DataType) -> Self;

    fn get_grid(&self) -> &Self::Grid;
    fn get_chunk(&mut self, pos: &Vector2i) -> Option<&mut ChunkType>;
}

pub struct ChunkHolder {
    chunk_grid: ChunkGrid<Chunk>
}

impl StoresChunkGrid<Chunk, ChunkData> for ChunkHolder {
    type Grid = ChunkGrid<Chunk>;
    type DataType = u16;

    fn new(width: Self::DataType, height: Self::DataType) -> Self {
        return Self {
            chunk_grid: ChunkGrid::new(width, height)
        };
    }

    fn get_grid(&self) -> &Self::Grid { return &self.chunk_grid; }
    fn get_chunk(&mut self, pos: &Vector2i) -> Option<&mut Chunk> { return self.chunk_grid.get_chunk_at_pos(pos) }
}

