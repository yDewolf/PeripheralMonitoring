
use std::fs::create_dir;
use std::sync::{Arc, Mutex};

#[cfg_attr(mobile, tauri::mobile_entry_point)]

use tauri::async_runtime;
use tauri::Manager;
use tauri_plugin_shell::process::{CommandEvent};
use tauri_plugin_shell::ShellExt;

struct AppState {
    api_pid: Arc<Mutex<Option<u32>>>,
}

pub fn kill_process(pid: u32) -> std::io::Result<()> {
    #[cfg(target_os = "windows")]
    {
        // Usa o comando nativo taskkill
        std::process::Command::new("taskkill")
            .args(["/PID", &pid.to_string(), "/F"])
            .status()?;
    }

    Ok(())
}

pub fn run() {
    tauri::Builder::default()
        .manage(AppState {
            api_pid: Arc::new(Mutex::new(None)),
        })
        .setup(move |app| {
            let state = app.state::<AppState>();

            let sidecar = app
                .shell()
                .sidecar("FlaskAPI")
                .expect("Failed to create side car");
        
            let app_data_dir = app.path().app_data_dir().ok().take();
            let mut app_data_path = app_data_dir.unwrap();
            let _error = create_dir(app_data_path.clone());

            let path_str = app_data_path.as_mut_os_str().to_os_string().into_string().unwrap();

            let (mut rx, child) = sidecar
                .args([
                    "--config ", &format!("{}\\config.cfg", &path_str),
                    "--save ", &format!("{}\\saves", &path_str)
                ])
                .spawn()
                .expect("Failed to initialize sidecar");
            
            let pid_arc = Arc::clone(&state.api_pid);
            {
                let mut lock = pid_arc.lock().unwrap();
                *lock = Some(child.pid());
            }

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
    .run(move |app_handle, event| match event {
        tauri::RunEvent::Ready => {
        }
        tauri::RunEvent::ExitRequested { .. } => {
            let state = app_handle.state::<AppState>();
            let pid_arc = Arc::clone(&state.api_pid);

            if let Ok(lock) = pid_arc.lock() {
                if let Some(pid) = *lock {
                    println!("Killing api process (PID {})...", pid);
                    // thread::sleep(time::Duration::from_millis(2000));

                    let _ = kill_process(pid);
                }
            }

            println!("Finished app process");
        }
        _ => {}
    });
}
