use std::time::Duration;

use yioe::helpers::events::listener::SendBehavior;

use crate::controllers::event::handlers::{KeyboardHandlerContext, MouseHandlerContext};
use crate::controllers::internals::base::chunk_holder::StoresChunkGrid;
use crate::controllers::internals::display_chunk::DisplayChunkHolder;
use crate::controllers::peripheral_events::PeripheralEventController;

#[derive(Clone)]
pub struct HandlerConfig {
    pub debug: bool,
    pub display_list: Vec<usize>,
    pub chunk_size: u16,
    pub poll_rate: Duration,

    pub kb_behavior: SendBehavior,
    pub ms_behavior: SendBehavior
}

impl HandlerConfig {
    pub fn new(debug: bool, display_list: Vec<usize>, chunk_size: u16, poll_rate: Duration, kb_behavior: SendBehavior, ms_behavior: SendBehavior) -> Self {
        Self { debug, display_list, chunk_size, poll_rate, kb_behavior, ms_behavior }
    }
}

pub struct SaveMetadata {
    pub tags: Vec<String>
}

impl SaveMetadata {
    pub fn new(tags: Vec<String>) -> Self {
        Self { tags }
    }
}

pub struct PeripheralStatisticsHandler {
    metadata: SaveMetadata,
    config: HandlerConfig,
    // chunk_holder: DisplayChunkHolder,
    event_controller: PeripheralEventController,

    mouse_context: Option<Box<MouseHandlerContext>>,
    keyboard_context: Option<Box<KeyboardHandlerContext>>,
}

impl PeripheralStatisticsHandler {
    pub fn new(config: HandlerConfig, metadata: SaveMetadata) -> Self {
        let cfg = config.clone();

        return Self {
            metadata: metadata,
            config: cfg,
            // chunk_holder: DisplayChunkHolder::new_from_display(config.display_list, config.chunk_size),
            event_controller: PeripheralEventController::new(config.kb_behavior, config.ms_behavior),
            mouse_context: Some(Box::new(MouseHandlerContext::new(config.chunk_size, Some(DisplayChunkHolder::new_from_display(config.display_list, config.chunk_size))))),
            keyboard_context: Some(Box::new(KeyboardHandlerContext::new()))
        }
    }

    pub fn listen_to_events(&mut self) {
        self.event_controller.start_listening();

        // self.mouse_context.unwrap().set_chunk_holder(Some(&self.chunk_holder.get_chunk(pos)));
        let mouse_context = self.mouse_context.take().unwrap();
        let keyboard_context = self.keyboard_context.take().unwrap();
        self.event_controller.handle_events(mouse_context, keyboard_context, self.config.poll_rate);

        self.event_controller.stop_listening();
    }
}