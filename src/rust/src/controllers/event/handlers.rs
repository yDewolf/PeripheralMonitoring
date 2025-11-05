use yioe::helpers::events::controller::{EventContext, EventHandler};
use yioe::helpers::events::event::{EventLike};
use yioe::helpers::keyboard::events::KeyboardEvent;
use yioe::helpers::mouse::events::MouseEvent;

use crate::controllers::internals::base::chunk_holder::StoresChunkGrid;
use crate::controllers::internals::base::chunks::ChunkLike;
use crate::controllers::internals::display_chunk::{DisplayChunk, DisplayChunkHolder};
use crate::utils::custom_types::Vector2i;

pub struct KeyboardHandlerContext {
    pub(crate) previous_key: Option<i32>,
}

impl KeyboardHandlerContext {
    pub fn new() -> Self {
        return Self {previous_key: None}
    }
}

impl EventContext for KeyboardHandlerContext {}

pub struct KeyboardEventHandler {
    context_id: usize
}

impl EventHandler<KeyboardEvent, KeyboardHandlerContext> for KeyboardEventHandler {
    fn handle(&self, event: &Box<KeyboardEvent>, context: &mut Box<KeyboardHandlerContext>) {
        // let EventTypes::KeyboardEvent(event_type) = event.event_type() else { return; };
        match event.event_type() {
            yioe::helpers::keyboard::events::KeyboardEventTypes::JustPressed => self.handle_key_press(event, context),
            yioe::helpers::keyboard::events::KeyboardEventTypes::Released => self.handle_key_release(event),
            _ => ()
        }
    }
    
    fn context_id(&self) -> usize { return self.context_id }
    
    fn set_context(&mut self, value: usize) { self.context_id = value }
}

impl KeyboardEventHandler {
    pub fn new(context_id: usize) -> Self {
        return Self {
            context_id: context_id
        }
    }

    pub fn handle_key_press(&self, event: &KeyboardEvent, context: &mut Box<KeyboardHandlerContext>) {
        // self.previous_key = event.data().target_key().clone();
        
        // self.mutable_data.previous_key = event.data().target_key().clone();
        println!("Previous key {:?} | {:?}", context.previous_key, event.data());
        context.previous_key = event.data().target_key().clone();
    }

    pub fn handle_key_release(&self, event: &KeyboardEvent) {
        println!("{:?}", event.data())
    }

    pub fn update_data_on_pressed() {

    }

    pub fn update_data_on_released() {
        
    }
}


pub struct MouseHandlerContext {
    pub(crate) last_hovered_chunk: Option<Box<DisplayChunk>>,
    pub(crate) chunk_size: u16,
    pub(crate) chunk_holder: Option<DisplayChunkHolder>,
}
impl MouseHandlerContext {
    pub fn new(chunk_size: u16, chunk_holder: Option<DisplayChunkHolder>) -> Self {
        return Self { last_hovered_chunk: None, chunk_size: chunk_size, chunk_holder: chunk_holder }
    }
}

impl EventContext for MouseHandlerContext {}

pub struct MouseEventHandler {
    context_id: usize
}

impl EventHandler<MouseEvent, MouseHandlerContext> for MouseEventHandler {
    fn handle(&self, event: &Box<MouseEvent>, context: &mut Box<MouseHandlerContext>) {
        // let EventTypes::MouseEvent(event_type) = event.event_type() else { return; };
        match event.event_type() {
            yioe::helpers::mouse::events::MouseEventTypes::JustPressed => self.handle_key_press(event, context),
            yioe::helpers::mouse::events::MouseEventTypes::Released => self.handle_key_release(event, context),
            yioe::helpers::mouse::events::MouseEventTypes::Move => self.handle_move(event, context),
            _ => ()
        }
    }
    
    fn context_id(&self) -> usize { return self.context_id; }
    
    fn set_context(&mut self, value: usize) { self.context_id = value }
}

impl MouseEventHandler {
   pub fn new(context_id: usize) -> Self {
        return Self {
            context_id: context_id
        }
    }

    pub fn handle_key_press(&self, event: &MouseEvent, context: &mut Box<MouseHandlerContext>) {
        println!("{:?}", event.data())
    }

    pub fn handle_key_release(&self, event: &MouseEvent, context: &mut Box<MouseHandlerContext>) {
        println!("{:?}", event.data())
    }

    pub fn handle_move(&self, event: &MouseEvent, context: &mut Box<MouseHandlerContext>) {
        let mouse_pos = Vector2i::new(event.data().pos()[0] as u16, event.data().pos()[1] as u16);
        let chunk_pos =  mouse_pos / Vector2i::new(context.chunk_size, context.chunk_size);

        let chunk_holder = context.chunk_holder.as_mut().unwrap();
        let chunk = chunk_holder.get_chunk(&chunk_pos).unwrap();
        chunk.data().times_hovered().add();

        println!("{:?} | {:?}", chunk_pos, chunk.data());
        // println!("{:?}", event.data())
    }

    pub fn update_data_on_pressed() {

    }

    pub fn update_data_on_released() {
        
    }
}