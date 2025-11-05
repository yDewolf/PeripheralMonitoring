use core::panic;
use std::sync::{Arc};
use std::sync::atomic::AtomicBool;
use std::thread;
use std::time::Duration;

use yioe::helpers::events::listener::{Listener, SendBehavior};
use yioe::helpers::keyboard::controller::KeyboardListenerController;
use yioe::helpers::keyboard::events::KeyboardEventTypes;
use yioe::helpers::keyboard::keyboard_listener::KeyboardEventListener;
use yioe::helpers::events::controller::{ListenerController};
use yioe::helpers::mouse::controller::MouseListenerController;
use yioe::helpers::mouse::events::MouseEventTypes;
use yioe::helpers::mouse::mouse_listener::MouseEventListener;

use crate::controllers::event::handlers::{KeyboardEventHandler, KeyboardHandlerContext, MouseEventHandler, MouseHandlerContext};

pub struct PeripheralEventController {
    keyboard_controller: KeyboardListenerController<KeyboardHandlerContext, KeyboardEventHandler>,
    mouse_controller: MouseListenerController<MouseHandlerContext, MouseEventHandler>,

    keyboard_handler: Arc<KeyboardEventHandler>,
    mouse_handler: Arc<MouseEventHandler>,
    run_controller: Arc<AtomicBool>,
}

impl PeripheralEventController {
    pub fn new(kb_behavior: SendBehavior, ms_behavior: SendBehavior) -> Self {
        let mut kb_controller = KeyboardListenerController::new(KeyboardEventListener::new(), kb_behavior);
        let mut ms_controller = MouseListenerController::new(MouseEventListener::new(), ms_behavior);

        let keyboard_handler: Arc<KeyboardEventHandler> = Arc::new(KeyboardEventHandler::new(0));
        let mouse_handler: Arc<MouseEventHandler> = Arc::new(MouseEventHandler::new(0));

        kb_controller.add_event_handler(keyboard_handler.clone(), KeyboardEventTypes::None);
        ms_controller.add_event_handler(mouse_handler.clone(), MouseEventTypes::None);
        // kb_controller.add_event_handler(keyboard_handler.clone(), KeyboardEventTypes::JustPressed);
        // kb_controller.add_event_handler(keyboard_handler.clone(), KeyboardEventTypes::Released);

        // ms_controller.add_event_handler(mouse_handler.clone(), MouseEventTypes::JustPressed);
        // ms_controller.add_event_handler(mouse_handler.clone(), MouseEventTypes::Released);
        // ms_controller.add_event_handler(mouse_handler.clone(), MouseEventTypes::Move);

        return Self {
            keyboard_controller: kb_controller,
            mouse_controller: ms_controller,
            keyboard_handler,
            mouse_handler,
            run_controller: Arc::new(AtomicBool::new(false))
            // running: Arc::new(AtomicBool::new(false)),
        }
    }

    pub fn start_listening(&mut self) {
        if self.run_controller.load(std::sync::atomic::Ordering::Relaxed) {
            panic!("ERROR: Can't start listeners that already started")
        }
        
        self.keyboard_controller.start_listening();
        self.mouse_controller.start_listening();
        self.run_controller.store(true, std::sync::atomic::Ordering::Relaxed);
    }

    pub fn handle_events(&mut self, mouse_context: Box<MouseHandlerContext>, keyboard_context: Box<KeyboardHandlerContext>, poll_rate: Duration) {
        if !self.run_controller.load(std::sync::atomic::Ordering::Relaxed) {
            panic!("ERROR: Can't handle events without starting listeners.")
        }

        let Some(ms_receiver) = self.mouse_controller.receiver().take() else { panic!("ERROR: Couldn't take receiver from mouse controller") };
        let Some(kb_receiver) = self.keyboard_controller.receiver().take() else { panic!("ERROR: Couldn't take receiver from keyboard controller") };
        let mut ms_contexts = vec![mouse_context];
        let mut kb_contexts = vec![keyboard_context];

        while self.run_controller.load(std::sync::atomic::Ordering::Relaxed) {
            self.mouse_controller._handle_events(&ms_receiver, &mut ms_contexts, &MouseEventTypes::None);
            self.keyboard_controller._handle_events(&kb_receiver, &mut kb_contexts, &KeyboardEventTypes::None);
         
            thread::sleep(poll_rate);
        }

        *self.mouse_controller.receiver() = Some(ms_receiver);
        *self.keyboard_controller.receiver() = Some(kb_receiver);
    }

    pub fn stop_listening(&mut self) {
        if !self.run_controller.load(std::sync::atomic::Ordering::Relaxed) {
            panic!("ERROR: Trying to stop peripheral controller that is already stopped.");
        }

        self.run_controller.store(false, std::sync::atomic::Ordering::Relaxed);
        // self.mouse_controller.stop_listening();
        self.keyboard_controller.stop_listening();
    }

    pub fn run_controller_clone(&self) -> Arc<AtomicBool> { return self.run_controller.clone() }
}