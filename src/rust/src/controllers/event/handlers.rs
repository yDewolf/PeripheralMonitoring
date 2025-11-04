use yioe::helpers::events::event::{EventLike, EventTypes};
use yioe::helpers::keyboard::events::KeyboardEvent;
use yioe::helpers::mouse::events::MouseEvent;

use crate::controllers::internals::display_chunk::DisplayChunk;

pub struct KeyboardEventHandler {
    previous_key: Option<i32>
}

impl KeyboardEventHandler {
    pub fn new() -> Self {
        return Self {
            previous_key: None
        }
    }

    pub fn handle_event(&mut self, event: &Box<KeyboardEvent>) {
        let EventTypes::KeyboardEvent(event_type) = event.event_type() else { return; };

    }

    pub fn handle_key_press(&mut self, event: &KeyboardEvent) {
        println!("{:?}", event.data())
    }

    pub fn handle_key_release(&mut self, event: &KeyboardEvent) {
        println!("{:?}", event.data())
    }

    pub fn update_data_on_pressed() {

    }

    pub fn update_data_on_released() {
        
    }
}

pub struct MouseEventHandler {
    last_hovered_chunk: Option<Box<DisplayChunk>>
}

impl MouseEventHandler {
    pub fn new() -> Self {
        return Self {
            last_hovered_chunk: None
        }
    }

    pub fn handle_key_press(&mut self, event: &MouseEvent) {
        println!("{:?}", event.data())
    }

    pub fn handle_key_release(&mut self, event: &MouseEvent) {
        println!("{:?}", event.data())
    }

    pub fn handle_move(&mut self, event: &MouseEvent) {
        println!("{:?}", event.data())
    }

    pub fn update_data_on_pressed() {

    }

    pub fn update_data_on_released() {
        
    }
}