
use std::fs::create_dir;

#[cfg_attr(mobile, tauri::mobile_entry_point)]

use tauri::async_runtime;
use tauri::Manager;
use tauri_plugin_shell::process::CommandEvent;
use tauri_plugin_shell::ShellExt;

pub fn run() {
 tauri::Builder::default()
    .setup(|app| {
        
        let sidecar = app
            .shell()
            .sidecar("FlaskAPI")
            .expect("Failed to create side car");
    
        let app_data_dir = app.path().app_data_dir().ok().take();
        let mut app_data_path = app_data_dir.unwrap();
        let error = create_dir(app_data_path.clone());

        let path_str = app_data_path.as_mut_os_str().to_os_string().into_string().unwrap();

        let (mut rx, _child) = sidecar
            .args([path_str + "\\config.cfg"])
            .spawn()
            .expect("Failed to initialize sidecar");

        async_runtime::spawn(async move {
            while let Some(event) = rx.recv().await {
                match event {
                    CommandEvent::Stdout(line) => {
                        println!("[FlaskAPI] {}", String::from_utf8_lossy(&line));
                    }
                    CommandEvent::Stderr(line) => {
                        println!("{}", String::from_utf8_lossy(&line))
                    }
                    _ => {}
                }
            }
        });

        Ok(())
    })
    .plugin(tauri_plugin_shell::init())
    .plugin(tauri_plugin_opener::init())
    .invoke_handler(tauri::generate_handler![])
    .build(tauri::generate_context!())
    .expect("Failed to build app")
    .run(|_app_handle, event| {
        if let tauri::RunEvent::ExitRequested { .. } = event {
            println!("Finished app process");
        }
    });
}
