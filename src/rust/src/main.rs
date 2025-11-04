use crate::controllers::internals::base::chunk_holder::StoresChunkGrid;
use crate::controllers::internals::display_chunk::DisplayChunkHolder;

mod controllers;
mod utils;

fn main() {
    let controller = DisplayChunkHolder::new_from_display(vec![], 8);
    println!("{:?}", controller.get_grid().grid_size)
}
