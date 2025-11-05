use std::time::Duration;

use yioe::helpers::events::listener::SendBehavior;
use crate::controllers::peripheral_statistics::{HandlerConfig, PeripheralStatisticsHandler, SaveMetadata};

mod controllers;
mod utils;

fn main() {
    let behavior = SendBehavior::new(false, false, Duration::from_millis(16));
    let mut statistics_thing = PeripheralStatisticsHandler::new(
        HandlerConfig::new(false, vec![0], 8, Duration::from_millis(16), behavior.clone(), behavior.clone()), 
        SaveMetadata::new(vec![])
    );

    statistics_thing.listen_to_events();
}
