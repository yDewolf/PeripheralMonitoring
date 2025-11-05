use std::sync::Arc;
use std::sync::atomic::AtomicBool;
use std::thread;
use std::time::Duration;

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

    keyboard_handler: Arc<KeyboardEventHandler>,
    mouse_handler: Arc<MouseEventHandler>
}

impl PeripheralEventController {
    pub fn new(kb_behavior: SendBehavior, ms_behavior: SendBehavior) -> Self {
        let mut kb_controller = KeyboardListenerController::new(KeyboardEventListener::new(), kb_behavior);
        let mut ms_controller = MouseListenerController::new(MouseEventListener::new(), ms_behavior);


        let keyboard_handler: Arc<KeyboardEventHandler> = Arc::new(KeyboardEventHandler::new());
        let mouse_handler: Arc<MouseEventHandler> = Arc::new(MouseEventHandler::new());

        kb_controller.add_event_handler(keyboard_handler.clone(), KeyboardEventTypes::JustPressed);
        kb_controller.add_event_handler(keyboard_handler.clone(), KeyboardEventTypes::Released);

        ms_controller.add_event_handler(mouse_handler.clone(), MouseEventTypes::JustPressed);
        ms_controller.add_event_handler(mouse_handler.clone(), MouseEventTypes::Released);
        ms_controller.add_event_handler(mouse_handler.clone(), MouseEventTypes::Move);

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

    pub fn handle_events(&mut self) {
        let run_controller: Arc<AtomicBool> = Arc::new(AtomicBool::new(true));

        self.mouse_controller.handle_events(run_controller.clone(), Duration::from_millis(16));
        self.keyboard_controller.handle_events(run_controller.clone(), Duration::from_millis(16));
    }
}