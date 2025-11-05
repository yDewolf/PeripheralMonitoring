use std::time::Duration;

use rust::controllers::peripheral_events::PeripheralEventController;
use yioe::helpers::events::listener::SendBehavior;

use crate::controllers::internals::base::chunk_holder::StoresChunkGrid;
use crate::controllers::internals::display_chunk::DisplayChunkHolder;

mod controllers;
mod utils;

fn main() {
    let controller = DisplayChunkHolder::new_from_display(vec![], 8);
    // controller.handle_events
    println!("{:?}", controller.get_grid().grid_size);

    let behavior = SendBehavior::new(false, false, Duration::from_millis(16));
    let mut event_controller: PeripheralEventController = PeripheralEventController::new(behavior.clone(), behavior);
    event_controller.start_listening();
    event_controller.handle_events();
}
