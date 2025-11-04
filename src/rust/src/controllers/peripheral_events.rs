use std::sync::Arc;
use std::sync::atomic::AtomicBool;

use yioe::helpers::events::event::EventTypes;
use yioe::helpers::events::listener::{Listener, SendBehavior};
use yioe::helpers::keyboard::controller::KeyboardListenerController;
use yioe::helpers::keyboard::events::KeyboardEventTypes;
use yioe::helpers::keyboard::keyboard_listener::KeyboardEventListener;
use yioe::helpers::mouse::controller::MouseListenerController;
use yioe::helpers::events::controller::{ListenerController};
use yioe::helpers::mouse::events::MouseEventTypes;
use yioe::helpers::mouse::mouse_listener::MouseEventListener;

use crate::controllers::event::handlers::{KeyboardEventHandler, MouseEventHandler};

pub struct PeripheralEventController {
    keyboard_controller: KeyboardListenerController,
    mouse_controller: MouseListenerController,

    keyboard_handler: KeyboardEventHandler,
    mouse_handler: MouseEventHandler
}

impl PeripheralEventController {
    pub fn new(kb_behavior: SendBehavior, ms_behavior: SendBehavior) -> Self {
        let mut kb_controller = KeyboardListenerController::new(KeyboardEventListener::new(), kb_behavior);
        let mut ms_controller = MouseListenerController::new(MouseEventListener::new(), ms_behavior);


        let mut keyboard_handler: KeyboardEventHandler = KeyboardEventHandler::new();
        let mut mouse_handler: MouseEventHandler = MouseEventHandler::new();

        kb_controller.add_event_handler(Box::new(|event| {}), KeyboardEventTypes::JustPressed);
        kb_controller.add_event_handler(Box::new(|event| {}), KeyboardEventTypes::Released);

        ms_controller.add_event_handler(Box::new(|event| {}), MouseEventTypes::JustPressed);
        ms_controller.add_event_handler(Box::new(|event| {}), MouseEventTypes::Released);
        ms_controller.add_event_handler(Box::new(|event| {}), MouseEventTypes::Move);

        return Self {
            keyboard_controller: kb_controller,
            mouse_controller: ms_controller,
            keyboard_handler,
            mouse_handler,
            // running: Arc::new(AtomicBool::new(false)),
        }
    }

    pub fn start_listening(&mut self) {
        self.keyboard_controller.start_listening();
        self.mouse_controller.start_listening();

    }
}