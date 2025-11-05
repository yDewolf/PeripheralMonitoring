use yioe::helpers::events::controller::EventHandler;
use yioe::helpers::events::event::{EventLike, EventTypes};
use yioe::helpers::keyboard::events::KeyboardEvent;
use yioe::helpers::mouse::events::MouseEvent;

use crate::controllers::internals::display_chunk::DisplayChunk;

pub struct KeyboardEventHandler {
    previous_key: Option<i32>
}

impl EventHandler<KeyboardEvent> for KeyboardEventHandler {
    fn handle(&self, event: &Box<KeyboardEvent>) {
        let EventTypes::KeyboardEvent(event_type) = event.event_type() else { return; };
        match event_type {
            yioe::helpers::keyboard::events::KeyboardEventTypes::JustPressed => self.handle_key_press(event),
            yioe::helpers::keyboard::events::KeyboardEventTypes::Released => self.handle_key_release(event),
            _ => ()
        }
    }
}

impl KeyboardEventHandler {
    pub fn new() -> Self {
        return Self {
            previous_key: None
        }
    }

    pub fn handle_key_press(&self, event: &KeyboardEvent) {
        println!("{:?}", event.data())
    }

    pub fn handle_key_release(&self, event: &KeyboardEvent) {
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

impl EventHandler<MouseEvent> for MouseEventHandler {
    fn handle(&self, event: &Box<MouseEvent>) {
        let EventTypes::MouseEvent(event_type) = event.event_type() else { return; };
        match event_type {
            yioe::helpers::mouse::events::MouseEventTypes::JustPressed => self.handle_key_press(event),
            yioe::helpers::mouse::events::MouseEventTypes::Released => self.handle_key_release(event),
            yioe::helpers::mouse::events::MouseEventTypes::Move => self.handle_move(event),
            _ => ()
        }
    }
}

impl MouseEventHandler {
    pub fn new() -> Self {
        return Self {
            last_hovered_chunk: None
        }
    }

    pub fn handle_key_press(&self, event: &MouseEvent) {
        println!("{:?}", event.data())
    }

    pub fn handle_key_release(&self, event: &MouseEvent) {
        println!("{:?}", event.data())
    }

    pub fn handle_move(&self, event: &MouseEvent) {
        println!("{:?}", event.data())
    }

    pub fn update_data_on_pressed() {

    }

    pub fn update_data_on_released() {
        
    }
}