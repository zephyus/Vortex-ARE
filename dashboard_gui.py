import customtkinter as ctk
import tkinter as tk
from system_engine import SystemEngine
import time
import os
import random
import json

class EvolutionDashboard(ctk.CTk):
    def __init__(self, engine: SystemEngine):
        super().__init__()
        self.engine = engine
        
        # UI Setup
        self.title("AI Autonomous Evolution Dashboard v2.0")
        self.geometry(self.engine.config.get("window_size", "900x600"))
        ctk.set_appearance_mode(self.engine.config.get("appearance_mode", "dark"))
        
        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.setup_sidebar()
        
        # Main Area
        self.setup_main_area()
        
        # Start Loops
        self.last_csv_log = time.time()
        self.last_dep_check: float = 0.0
        self.last_ui_snapshot: float = 0.0
        self.anomaly_count = 0
        self.current_metabolic_state = "STEADY"
        self.update_personality_theme(self.engine.config.get("personality", "Default"))
        self.update_telemetry()
        
        # Subscribe to Neural Hub signals
        self.engine.subscribe_to_signals("pulse", self.on_pulse_signal)
        self.engine.subscribe_to_signals("event", self.on_event_signal)
        self.engine.subscribe_to_signals("synapse_feedback", self.on_synapse_feedback)
        self.engine.subscribe_to_signals("cluster_active", self.on_cluster_signal)
        self.engine.subscribe_to_signals("sandbox_complete", self.on_sandbox_signal)
        self.engine.subscribe_to_signals("entropy_pruned", self.on_entropy_signal)
        self.engine.subscribe_to_signals("metabolic_feedback", self.engine.analyze_visual_metabolism)

    def on_entropy_signal(self, payload):
        removed = payload.get("removed", 0)
        self.after(0, lambda: self.add_log(f"ENTROPY REDUCED: Pruned {removed} redundant logic markers."))

    def on_cluster_signal(self, payload):
        nodes = payload.get("nodes", 0)
        self.after(0, lambda: self.cluster_label.configure(text=f"🧵 CLUSTER: {nodes} NODES"))

    def on_sandbox_signal(self, payload):
        sid = payload.get("id")
        res = payload.get("res", 0.0)
        self.after(0, lambda: self.add_log(f"SANDBOX [{sid}] COMPLETE: {res*100:.1f}% RESONANCE"))

    def on_synapse_feedback(self, payload):
        """Callback for synaptic rule weight updates."""
        weights = payload.get("weights", {})
        msg = "SYNAPSE ADJUSTED: " + ", ".join([f"{k}:{v:.2f}" for k,v in weights.items()])
        self.after(0, lambda: self.add_log(msg))

    def on_pulse_signal(self, value):
        """Callback for Neural Hub 'pulse' signal."""
        # This handles high-frequency visual updates decoupled from main telemetry
        self.after(0, lambda: self.update_pulse_viz(value, self.engine.config.get("personality", "Default")))
        self.after(0, lambda: self.conduction_pulse())

    def on_event_signal(self, payload):
        """Callback for Neural Hub 'event' signals."""
        self.after(0, lambda: self.add_log(f"SIGNAL: {payload}"))

    def conduction_pulse(self):
        """Flickers the conduction indicator to show active data stream."""
        self.conduction_label.configure(text="📡 ACTIVE", text_color="#00FF00")
        self.after(200, lambda: self.conduction_label.configure(text="📡 IDLE", text_color="#555555"))
        self.engine.append_log("GUI Initialized / System Engaged")

    def setup_sidebar(self):
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        
        self.nav_label = ctk.CTkLabel(self.navigation_frame, text="EVOLUTION OS", font=ctk.CTkFont(size=20, weight="bold"))
        self.nav_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.theme_btn = ctk.CTkButton(self.navigation_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_btn.grid(row=1, column=0, padx=10, pady=10)

        self.energy_history_bars = []
        bar_frame2 = ctk.CTkFrame(self.navigation_frame, fg_color="transparent")
        bar_frame2.grid(row=29, column=0, pady=5)
        # ... skipped loop for brevity ...
            
        self.personality_btn = ctk.CTkButton(self.navigation_frame, text="Cycle Persona", command=self.cycle_personality)
        self.personality_btn.grid(row=30, column=0, pady=20)
        
        self.personality_label = ctk.CTkLabel(self.navigation_frame, text=f"Persona: {self.engine.config.get('personality', 'Default')}", font=ctk.CTkFont(size=12))
        self.personality_label.grid(row=8, column=0, padx=20, pady=5)

        self.sync_label = ctk.CTkLabel(self.navigation_frame, text="📡 SYNC: OFFLINE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#666666")
        self.sync_label.grid(row=9, column=0, padx=20, pady=5)

        self.heartbeat_label = ctk.CTkLabel(self.navigation_frame, text="💓 PULSE: NOMINAL", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00FFAA")
        self.heartbeat_label.grid(row=10, column=0, padx=20, pady=(5, 20))
        
        self.regen_label = ctk.CTkLabel(self.navigation_frame, text="⚡ REGEN: OFF", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00FFFF")
        self.regen_label.grid(row=11, column=0, padx=20, pady=5)
        
        self.personality_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Default", "Performance", "Safety", "Aesthetic"], command=self.change_personality)
        self.personality_menu.set(self.engine.config.get("personality", "Default"))
        self.personality_menu.grid(row=3, column=0, padx=10, pady=(0, 10))
        
        # Theme tokens
        self.themes = {
            "Default": {"bg": "#1a1a1a", "accent": "#1f538d", "text": "#ffffff", "pill": "#00FFAA"},
            "Performance": {"bg": "#2a1010", "accent": "#ff4400", "text": "#ffeeee", "pill": "#ff0000"},
            "Safety": {"bg": "#101a2a", "accent": "#0088ff", "text": "#eef6ff", "pill": "#00ccff"},
            "Aesthetic": {"bg": "#1a102a", "accent": "#aa00ff", "text": "#f6eeff", "pill": "#ff00ff"}
        }

        self.apply_personality_theme()
        
        self.cleanup_btn = ctk.CTkButton(self.navigation_frame, text="System Cleanup", command=self.trigger_cleanup, fg_color="#A371F7", hover_color="#8A5BDE")
        self.cleanup_btn.grid(row=4, column=0, padx=10, pady=5)
        
        self.backup_btn = ctk.CTkButton(self.navigation_frame, text="Manual Backup", command=self.trigger_backup, fg_color="#2EA44F", hover_color="#22863A")
        self.backup_btn.grid(row=5, column=0, padx=10, pady=5)
        
        self.report_btn = ctk.CTkButton(self.navigation_frame, text="Gen Evolution Report", command=self.trigger_report, fg_color="#FF5F1F", hover_color="#E6551A")
        self.report_btn.grid(row=6, column=0, padx=10, pady=5)
        
        self.doc_btn = ctk.CTkButton(self.navigation_frame, text="Sync Documentation", command=self.trigger_docs, fg_color="#1FA56A", hover_color="#147048")
        self.doc_btn.grid(row=7, column=0, padx=10, pady=5)
        
        self.insights_btn = ctk.CTkButton(self.navigation_frame, text="Codebase Insights", command=self.open_insights, fg_color="#A56A1F", hover_color="#704814")
        self.insights_btn.grid(row=8, column=0, padx=10, pady=5)
        
        self.arch_btn = ctk.CTkButton(self.navigation_frame, text="Visualize Architecture", command=self.trigger_arch, fg_color="#1F6AA5", hover_color="#144870")
        self.arch_btn.grid(row=9, column=0, padx=10, pady=5)
        
        self.personality_label.grid(row=8, column=0, padx=20, pady=5)
        self.insights_btn.grid(row=9, column=0, padx=10, pady=5)
        
        self.arch_btn = ctk.CTkButton(self.navigation_frame, text="Visualize Architecture", command=self.trigger_arch, fg_color="#1F6AA5", hover_color="#144870")
        self.arch_btn.grid(row=10, column=0, padx=10, pady=5)
        
        self.history_btn = ctk.CTkButton(self.navigation_frame, text="Browse Code History", command=self.open_history_viewer, fg_color="#707070", hover_color="#505050")
        self.history_btn.grid(row=11, column=0, padx=10, pady=5)

        self.timetravel_btn = ctk.CTkButton(self.navigation_frame, text="🕒 UI Time Travel", command=self.open_time_travel, fg_color="#FFD700", text_color="#000000", hover_color="#DAA520")
        self.timetravel_btn.grid(row=12, column=0, padx=10, pady=5)
        
        self.tree_btn = ctk.CTkButton(self.navigation_frame, text="View Code Tree", command=self.open_project_tree, fg_color="#1F6AA5", border_width=1)
        self.tree_btn.grid(row=13, column=0, padx=10, pady=5)
        
        self.commit_btn = ctk.CTkButton(self.navigation_frame, text="Commit Evolution", command=self.trigger_commit, fg_color="#F1E05A", text_color="#000000", hover_color="#D1C04A")
        self.commit_btn.grid(row=14, column=0, padx=10, pady=5)
        
        self.tune_btn = ctk.CTkButton(self.navigation_frame, text="Tune Personas", command=self.open_personality_tuner, fg_color="#FF00AA", hover_color="#C00088")
        self.tune_btn.grid(row=15, column=0, padx=10, pady=5)
        
        self.hub_btn = ctk.CTkButton(self.navigation_frame, text="Connectivity Hub", command=self.open_connectivity_hub, fg_color="#00AAFF", hover_color="#0088CC")
        self.hub_btn.grid(row=16, column=0, padx=10, pady=5)
        
        self.heatmap_btn = ctk.CTkButton(self.navigation_frame, text="EVO Heatmap", command=self.open_evolution_heatmap, fg_color="#FF5F1F", hover_color="#E6551A")
        self.heatmap_btn.grid(row=17, column=0, padx=10, pady=5)

        self.snapshot_matrix_btn = ctk.CTkButton(self.navigation_frame, text="🧠 LOGIC MATRIX", command=self.open_cognitive_matrix, fg_color="#00FFAA", text_color="#000000", hover_color="#00CC88")
        self.snapshot_matrix_btn.grid(row=18, column=0, padx=10, pady=5)

        self.editor_btn = ctk.CTkButton(self.navigation_frame, text="🛠️ Arch Editor", command=self.open_arch_editor, fg_color="#00FFAA", text_color="#000000", hover_color="#00CC88")
        self.editor_btn.grid(row=19, column=0, padx=10, pady=5)
        
        self.metrics_btn = ctk.CTkButton(self.navigation_frame, text="🔬 Metrics Lab", command=self.open_metrics_lab, fg_color="#AA00FF", hover_color="#8800CC")
        self.metrics_btn.grid(row=20, column=0, padx=10, pady=5)
        
        self.refactor_btn = ctk.CTkButton(self.navigation_frame, text="☢️ REFACTOR LAB", command=self.open_refactor_lab, fg_color="#FF0000", text_color="#FFFFFF", hover_color="#CC0000")
        self.refactor_btn.grid(row=21, column=0, padx=10, pady=5)
        
        self.harden_btn = ctk.CTkButton(self.navigation_frame, text="🧬 Evolve Logic", command=self.trigger_logic_hardening, fg_color="#FFD700", text_color="#000000", hover_color="#CCAB00")
        self.harden_btn.grid(row=22, column=0, padx=10, pady=5)
        
        self.sync_label = ctk.CTkLabel(self.navigation_frame, text="📡 SYNC: OFFLINE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#666666")
        self.sync_label.grid(row=23, column=0, padx=20, pady=5)

        self.heartbeat_label = ctk.CTkLabel(self.navigation_frame, text="💓 PULSE: NOMINAL", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00FFAA")
        self.heartbeat_label.grid(row=24, column=0, padx=20, pady=(5, 20))
        
        self.regen_label = ctk.CTkLabel(self.navigation_frame, text="⚡ REGEN: OFF", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00FFFF")
        self.regen_label.grid(row=25, column=0, padx=20, pady=5)
        
        self.tree_btn = ctk.CTkButton(self.navigation_frame, text="View Code Tree", command=self.open_project_tree, fg_color="#1F6AA5", border_width=1)
        self.tree_btn.grid(row=12, column=0, padx=10, pady=5)
        
        self.commit_btn = ctk.CTkButton(self.navigation_frame, text="Commit Evolution", command=self.trigger_commit, fg_color="#F1E05A", text_color="#000000", hover_color="#D1C04A")
        self.commit_btn.grid(row=13, column=0, padx=10, pady=5)
        
        self.tune_btn = ctk.CTkButton(self.navigation_frame, text="Tune Personas", command=self.open_personality_tuner, fg_color="#FF00AA", hover_color="#C00088")
        self.tune_btn.grid(row=14, column=0, padx=10, pady=5)
        
        self.hub_btn = ctk.CTkButton(self.navigation_frame, text="Connectivity Hub", command=self.open_connectivity_hub, fg_color="#00AAFF", hover_color="#0088CC")
        self.hub_btn.grid(row=15, column=0, padx=10, pady=5)
        
        self.heatmap_btn = ctk.CTkButton(self.navigation_frame, text="EVO Heatmap", command=self.open_evolution_heatmap, fg_color="#FF5F1F", hover_color="#E6551A")
        self.heatmap_btn.grid(row=16, column=0, padx=10, pady=5)

        self.snapshot_matrix_btn = ctk.CTkButton(self.navigation_frame, text="🧠 LOGIC MATRIX", command=self.open_cognitive_matrix, fg_color="#00FFAA", text_color="#000000", hover_color="#00CC88")
        self.snapshot_matrix_btn.grid(row=17, column=0, padx=10, pady=5)

        self.editor_btn = ctk.CTkButton(self.navigation_frame, text="🛠️ Arch Editor", command=self.open_arch_editor, fg_color="#00FFAA", text_color="#000000", hover_color="#00CC88")
        self.editor_btn.grid(row=18, column=0, padx=10, pady=5)
        
        self.metrics_btn = ctk.CTkButton(self.navigation_frame, text="🔬 Metrics Lab", command=self.open_metrics_lab, fg_color="#AA00FF", hover_color="#8800CC")
        self.metrics_btn.grid(row=19, column=0, padx=10, pady=5)
        
        self.refactor_btn = ctk.CTkButton(self.navigation_frame, text="☢️ REFACTOR LAB", command=self.open_refactor_lab, fg_color="#FF0000", text_color="#FFFFFF", hover_color="#CC0000")
        self.refactor_btn.grid(row=20, column=0, padx=10, pady=5)
        
        self.harden_btn = ctk.CTkButton(self.navigation_frame, text="🧬 Evolve Logic", command=self.trigger_logic_hardening, fg_color="#FFD700", text_color="#000000", hover_color="#CCAB00")
        self.harden_btn.grid(row=21, column=0, padx=10, pady=5)
        
        self.stats_label = ctk.CTkLabel(self.navigation_frame, text="Project Stats", font=ctk.CTkFont(size=14, weight="bold"))
        self.stats_label.grid(row=26, column=0, pady=(20, 0))
        
        self.file_stat = ctk.CTkLabel(self.navigation_frame, text="Files: 0", font=ctk.CTkFont(size=12))
        self.dir_stat = ctk.CTkLabel(self.navigation_frame, text="Dirs: 0", font=ctk.CTkFont(size=12))
        self.sloc_stat = ctk.CTkLabel(self.navigation_frame, text="SLOC: 0", font=ctk.CTkFont(size=12))

        self.file_stat.grid(row=27, column=0)
        self.dir_stat.grid(row=28, column=0)
        self.sloc_stat.grid(row=29, column=0, pady=(10, 0))
        
        # Self-Test Status HUD
        self.test_label = ctk.CTkLabel(self.navigation_frame, text="Integrity: UNKNOWN", font=ctk.CTkFont(size=12, weight="bold"), cursor="hand2")
        self.test_label.grid(row=30, column=0, pady=(10, 0))
        self.test_label.bind("<Button-1>", lambda e: self.open_test_details())
        
        self.test_btn = ctk.CTkButton(self.navigation_frame, text="RE-VERIFY", command=self.run_manual_tests, height=24)
        self.test_btn.grid(row=31, column=0, pady=5)
        
        self.anomaly_label = ctk.CTkLabel(self.navigation_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FF00FF")
        self.anomaly_label.grid(row=32, column=0, pady=5)
        
        self.divergence_label = ctk.CTkLabel(self.navigation_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00FFFF")
        self.divergence_label.grid(row=33, column=0, pady=5)
        
        self.healing_label = ctk.CTkLabel(self.navigation_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FF3333")
        self.healing_label.grid(row=34, column=0, pady=5)
        
        self.conduction_label = ctk.CTkLabel(self.navigation_frame, text="📡 IDLE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#555555")
        self.conduction_label.grid(row=35, column=0, pady=5)
        
        self.synapse_label = ctk.CTkLabel(self.navigation_frame, text="🧠 SYNAPSE: 0/0", font=ctk.CTkFont(size=12, weight="bold"), text_color="#99FF99")
        self.synapse_label.grid(row=36, column=0, pady=5)
        
        self.resonance_label = ctk.CTkLabel(self.navigation_frame, text="📈 RESONANCE: 100%", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FF99FF")
        self.resonance_label.grid(row=37, column=0, pady=5)
        
        self.cluster_label = ctk.CTkLabel(self.navigation_frame, text="🧵 CLUSTER: IDLE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#CCCCFF")
        self.cluster_label.grid(row=38, column=0, pady=5)
        
        self.entropy_label = ctk.CTkLabel(self.navigation_frame, text="📉 ENTROPY: 0.10", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCC99")
        self.entropy_label.grid(row=39, column=0, pady=5)
        
        self.synesthesia_label = ctk.CTkLabel(self.navigation_frame, text="🔗 SYNESTHESIA: OFF", font=ctk.CTkFont(size=12, weight="bold"), text_color="#99FFFF")
        self.synesthesia_label.grid(row=40, column=0, pady=5)
        
        self.consciousness_label = ctk.CTkLabel(self.navigation_frame, text="🧠 CONSCIOUSNESS: 0%", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFFFFF")
        self.consciousness_label.grid(row=41, column=0, pady=5)
        
        self.consensus_label = ctk.CTkLabel(self.navigation_frame, text="🛰️ CONSENSUS: STABLE (100%)", font=ctk.CTkFont(size=12, weight="bold"), text_color="#55FF55")
        self.consensus_label.grid(row=42, column=0, pady=5)
        
        self.harvest_label = ctk.CTkLabel(self.navigation_frame, text="🔋 HARVEST: 100%", font=ctk.CTkFont(size=12, weight="bold"), text_color="#AAFFAA")
        self.harvest_label.grid(row=43, column=0, pady=5)
        
        self.governor_label = ctk.CTkLabel(self.navigation_frame, text="🛡️ GOVERNOR: ACTIVE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#55FF55")
        self.governor_label.grid(row=44, column=0, pady=5)
        
        self.thermal_label = ctk.CTkLabel(self.navigation_frame, text="🔥 THERMAL: 0%", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00FFFF")
        self.thermal_label.grid(row=45, column=0, pady=5)
        
        self.memory_label = ctk.CTkLabel(self.navigation_frame, text="💾 MEMORY: SAFE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#AAAAFF")
        self.memory_label.grid(row=46, column=0, pady=5)
        
        self.healer_label = ctk.CTkLabel(self.navigation_frame, text="🩺 HEALER: IDLE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#AAAAAA")
        self.healer_label.grid(row=47, column=0, pady=5)
        
        self.refiner_label = ctk.CTkLabel(self.navigation_frame, text="🧬 REFINER: SLEEPING", font=ctk.CTkFont(size=12, weight="bold"), text_color="#AAAAAA")
        self.refiner_label.grid(row=48, column=0, pady=5)
        
        self.revenue_title = ctk.CTkLabel(self.navigation_frame, text="💰 10,000 NTD GOAL", font=ctk.CTkFont(size=14, weight="bold"), text_color="#00FFAA")
        self.revenue_title.grid(row=49, column=0, pady=(20, 5))
        
        self.revenue_bar = ctk.CTkProgressBar(self.navigation_frame, progress_color="#FFD700")
        self.revenue_bar.grid(row=50, column=0, padx=20, pady=5)
        self.revenue_bar.set(0)
        
        self.revenue_status = ctk.CTkLabel(self.navigation_frame, text="0 / 10000 NTD", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFFFFF")
        self.revenue_status.grid(row=51, column=0, pady=5)
        
        self.breakdown_label = ctk.CTkLabel(self.navigation_frame, text="Code Breakdown", font=ctk.CTkFont(size=12, weight="bold"))
        self.breakdown_label.grid(row=52, column=0, pady=(20, 5))
        
        self.breakdown_text = ctk.CTkLabel(self.navigation_frame, text="", font=ctk.CTkFont(size=10), justify="left")
        self.breakdown_text.grid(row=53, column=0, padx=10)

    def setup_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.status_label = ctk.CTkLabel(self.main_frame, text="AI Engine: AUTONOMOUS", font=ctk.CTkFont(size=24, weight="bold"), text_color="#00FFAA")
        self.status_label.pack(pady=20)
        
        self.cpu_label, self.cpu_bar = self.create_resource_row("CPU")
        self.ram_label, self.ram_bar = self.create_resource_row("RAM")
        self.disk_label, self.disk_bar = self.create_resource_row("Disk")
        self.energy_label, self.energy_bar = self.create_resource_row("AI Energy", color="#FFD700")
        
        # Network Display
        self.net_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.net_frame.pack(fill="x", padx=20, pady=5)
        self.up_label = ctk.CTkLabel(self.net_frame, text="Upload: 0 KB/s", text_color="#FFAA00")
        self.up_label.pack(side="left", padx=10)
        self.down_label = ctk.CTkLabel(self.net_frame, text="Download: 0 KB/s", text_color="#00AAFF")
        self.down_label.pack(side="left", padx=10)
        
        # Goals Area
        self.goals_frame = ctk.CTkFrame(self.main_frame, fg_color="#1A1A1A")
        self.goals_frame.pack(fill="x", padx=20, pady=10)
        self.goals_title = ctk.CTkLabel(self.goals_frame, text="EVOLUTION GOALS", font=ctk.CTkFont(size=12, weight="bold"))
        self.goals_title.pack(pady=5)
        self.goal_widgets = [] # List of (label, progress)
        
        self.vision_label = ctk.CTkLabel(self.main_frame, text="VISION: ARCHITECTING...", font=ctk.CTkFont(size=14, weight="bold", slant="italic"), text_color="#FF00FF")
        self.vision_label.pack(pady=5)
        
        # Pulse Canvas (EKG)
        self.pulse_frame = ctk.CTkFrame(self.main_frame, height=40, fg_color="#111111")
        self.pulse_frame.pack(fill="x", padx=20, pady=5)
        self.pulse_canvas = tk.Canvas(self.pulse_frame, height=40, bg="#111111", highlightthickness=0)
        self.pulse_canvas.pack(fill="both", expand=True)
        self.pulse_points = [20] * 50 # History of pulse values
        
        # Health Indicator
        self.health_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.health_frame.pack(fill="x", padx=20)
        self.health_label = ctk.CTkLabel(self.health_frame, text="Code Health: EXCELLENT", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00FFAA")
        self.health_label.pack(side="left")
        
        self.forecast_label = ctk.CTkLabel(self.health_frame, text="Trend: -", font=ctk.CTkFont(size=10))
        self.forecast_label.pack(side="left", padx=10)
        
        self.smells_label = ctk.CTkLabel(self.health_frame, text="", font=ctk.CTkFont(size=10, slant="italic"))
        self.smells_label.pack(side="left", padx=20)
        
        self.preview_btn = ctk.CTkButton(self.health_frame, text="Preview Fix", width=80, height=20, font=ctk.CTkFont(size=9), command=self.open_refactor_preview)
        self.preview_btn.pack(side="left", padx=5)
        
        self.test_health_label = ctk.CTkLabel(self.health_frame, text="Tests: N/A", font=ctk.CTkFont(size=10, weight="bold"), text_color="#AAAAAA")
        self.test_health_label.pack(side="right", padx=10)
        
        self.deps_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.deps_frame.pack(fill="x", padx=20)
        self.deps_label = ctk.CTkLabel(self.deps_frame, text="Package Health: CHECKING...", font=ctk.CTkFont(size=10))
        self.deps_label.pack(side="left")
        self.heal_btn = ctk.CTkButton(self.deps_frame, text="Heal Deps", width=80, height=20, font=ctk.CTkFont(size=9), fg_color="#FF3333", command=self.trigger_heal)
        self.heal_btn.pack(side="left", padx=10)
        self.heal_btn.pack_forget() # Hide by default
        
        # Timeline Area
        self.timeline_title = ctk.CTkLabel(self.main_frame, text="EVOLUTION TIMELINE", font=ctk.CTkFont(size=12, weight="bold"))
        self.timeline_title.pack(pady=(10,0))
        self.timeline_box = ctk.CTkTextbox(self.main_frame, height=100, font=ctk.CTkFont(size=11))
        self.timeline_box.pack(padx=20, pady=5, fill="x")
        
        # Log Box
        self.log_box = ctk.CTkTextbox(self.main_frame, height=150, font=ctk.CTkFont(size=11))
        self.log_box.pack(padx=20, pady=5, fill="both", expand=True)
        self.log_box.insert("0.0", self.engine.load_logs())
        
        self.analytics_btn = ctk.CTkButton(self.main_frame, text="View High-Res Analytics", command=self.open_analytics)
        self.analytics_btn.pack(pady=5)
        
        self.test_btn = ctk.CTkButton(self.main_frame, text="Run Self-Tests", command=self.trigger_tests, fg_color="#D1B000", hover_color="#B39700")
        self.test_btn.pack(pady=5)
        
        # History Canvas/Bar Frame
        self.history_frame = ctk.CTkFrame(self.main_frame, height=60, fg_color="transparent")
        self.history_frame.pack(fill="x", padx=20, pady=5)
        self.history_label = ctk.CTkLabel(self.history_frame, text="Trend (Last 15s):", font=ctk.CTkFont(size=12))
        self.history_label.pack(side="left")
        
        self.cpu_history_bars = []
        for _ in range(15):
            b = ctk.CTkProgressBar(self.history_frame, width=30, height=2, orientation="vertical")
            b.pack(side="left", padx=1)
            b.set(0)
            self.cpu_history_bars.append(b)

    def create_resource_row(self, label_text, color=None):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=5)
        lbl = ctk.CTkLabel(frame, text=f"{label_text}: -", font=ctk.CTkFont(size=12))
        lbl.pack(side="left")
        bar = ctk.CTkProgressBar(frame)
        if color:
            bar.configure(progress_color=color)
        bar.pack(side="right", fill="x", expand=True, padx=(10, 0))
        bar.set(0)
        return (lbl, bar)

    def toggle_theme(self):
        new_mode = "light" if self.engine.config["appearance_mode"] == "dark" else "dark"
        self.engine.config["appearance_mode"] = new_mode
        ctk.set_appearance_mode(new_mode)
        self.engine.save_config(self.engine.config)
        self.add_log_to_ui(f"Theme toggled: {new_mode}")

    def open_personality_tuner(self):
        tuner = ctk.CTkToplevel(self)
        tuner.title("Personality Tuner")
        tuner.geometry("300x500")
        tuner.attributes("-topmost", True)

        ctk.CTkLabel(tuner, text="Select Evolution Strategy", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        personas = self.personality_menu.cget("values")

        def apply_persona(p):
            self.engine.config["personality"] = p
            self.engine.save_config(self.engine.config)
            self.add_log_to_ui(f"PERSONALITY: Strategy shifted to '{p}'.")
            self.engine.speak(f"Operational strategy set to {p}.")
            tuner.destroy()

        def open_strategy_lab():
            lab = ctk.CTkToplevel(tuner) # Parent to tuner window
            lab.title("Evolutionary Strategy Lab")
            lab.geometry("450x380")
            lab.attributes("-topmost", True)
            
            ctk.CTkLabel(lab, text="Recursive Strategy Optimization", font=("Inter", 16, "bold"), text_color="#00FFAA").pack(pady=10)
            
            # Fetch results
            res = self.engine.optimize_strategy_thresholds()
            if not res or not res["efficiencies"]:
                ctk.CTkLabel(lab, text="Insufficient telemetry for optimization.", text_color="#AAAAAA").pack(pady=20)
                ctk.CTkLabel(lab, text="(Need more diverse persona cycles in CSV)", font=("Inter", 10), text_color="#666666").pack()
                return

            best = res["best"]
            effs = res["efficiencies"]
            
            ctk.CTkLabel(lab, text=f"Top Efficiency Strategy: {best}", font=("Inter", 14, "bold"), text_color="#FF00FF").pack(pady=5)
            
            # Chart-like list
            for p, val in effs.items():
                row = ctk.CTkFrame(lab, fg_color="transparent")
                row.pack(fill="x", padx=20, pady=4)
                ctk.CTkLabel(row, text=f"{p}:", width=100, anchor="w").pack(side="left")
                # Visual Bar
                bar_bg = ctk.CTkFrame(row, fg_color="#333333", height=12, width=200)
                bar_bg.pack(side="left", padx=10)
                bar_width = min(200, int(val * 100)) # Scaled
                ctk.CTkFrame(bar_bg, fg_color="#00FFFF" if p == best else "#FF00FF", height=12, width=bar_width).place(x=0, y=0)
                ctk.CTkLabel(row, text=f"{val:.2f}").pack(side="left")

            ctk.CTkButton(lab, text="🧬 Persist Meta-Optimization", fg_color="#00FFAA", text_color="#000000",
                        command=lambda: [self.add_log_to_ui(f"META: Evolved thresholds for {best}."), lab.destroy()]).pack(pady=20)

        def open_metrics_lab():
            lab = ctk.CTkToplevel(self)
            lab.title("Evolutionary Metrics Lab | Efficiency Scorecard")
            lab.geometry("700x550")
            lab.attributes("-topmost", True)
            
            tab_view = ctk.CTkTabview(lab)
            tab_view.pack(fill="both", expand=True, padx=10, pady=10)
            
            t1 = tab_view.add("Historical Trends")
            t2 = tab_view.add("Efficiency Scorecard")
            
            # --- Tab 1: Trends (Legacy) ---
            canvas = ctk.CTkCanvas(t1, bg="#1A1A1A", highlightthickness=0)
            canvas.pack(fill="both", expand=True, padx=20, pady=20)
            data = self.engine.get_performance_history_data()
            self._render_metrics_chart(canvas, data)

            # --- Tab 2: Efficiency Scorecard ---
            score_scroll = ctk.CTkScrollableFrame(t2, fg_color="transparent")
            score_scroll.pack(fill="both", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(score_scroll, text="Module Metabolic Heat Index", font=("Inter", 16, "bold"), text_color="#00FFAA").pack(pady=10)
            
            # Get current health issues (which now contains metabolic scores)
            hotspots = self.engine.check_code_health()
            for fname, func, length, m_score in hotspots:
                row = ctk.CTkFrame(score_scroll, fg_color="#222222", height=50)
                row.pack(fill="x", pady=5, padx=10)
                
                ctk.CTkLabel(row, text=f"🔥 {fname}\n{func}", width=180, anchor="w", font=("Inter", 11)).pack(side="left", padx=10)
                
                # Efficiency Meter
                meter_bg = ctk.CTkFrame(row, fg_color="#333333", height=12, width=250)
                meter_bg.pack(side="left", padx=20)
                heat_width = min(250, int(m_score * 2))
                heat_color = "#FF4400" if m_score > 80 else ("#FFAA00" if m_score > 50 else "#00FFAA")
                ctk.CTkFrame(meter_bg, fg_color=heat_color, height=12, width=heat_width).place(x=0, y=0)
                
                ctk.CTkLabel(row, text=f"Heat: {m_score}", font=("Inter", 12, "bold")).pack(side="left")

            def trigger_metabolic_fix():
                if hotspots:
                    best_target = hotspots[0]
                    self.add_log_to_ui(f"METABOLIC: Initiating efficiency patch for {best_target[1]}...")
                    lab.destroy()
                else:
                    self.add_log_to_ui("METABOLIC: System is already at peak efficiency.")

            ctk.CTkButton(t2, text="🧬 Apply Efficiency Patches", fg_color="#00FFAA", text_color="#000000",
                         command=trigger_metabolic_fix).pack(pady=20)

        def open_deep_test_hud():
            hud = ctk.CTkToplevel(self)
            hud.title("Deep Test HUD | Immune Response Visualization")
            hud.geometry("500x400")
            hud.attributes("-topmost", True)
            
            ctk.CTkLabel(hud, text="Logic Hardening Heatmap", font=("Inter", 18, "bold"), text_color="#00FFAA").pack(pady=10)
            
            # Build stats from generated tests
            test_results = self.engine.get_last_test_results()
            if not test_results:
                ctk.CTkLabel(hud, text="Run tests to generate coverage data.", text_color="#AAAAAA").pack(pady=40)
                return

            tests = test_results.get("tests", [])
            hardening_counts = {} # Module -> count
            for t in tests:
                name = t["name"]
                if "test_gen_" in name:
                    # Identify module: test_gen_system_engine_...
                    parts = name.split("_")
                    if len(parts) >= 4:
                        mod = parts[2] + "_" + parts[3] if parts[3] == "engine" else parts[2]
                        hardening_counts[mod] = hardening_counts.get(mod, 0) + 1

            # Render heatmap
            scroll = ctk.CTkScrollableFrame(hud, fg_color="transparent")
            scroll.pack(fill="both", expand=True, padx=20, pady=10)
            
            for mod, count in hardening_counts.items():
                row = ctk.CTkFrame(scroll, fg_color="#1A1A1A", height=40)
                row.pack(fill="x", pady=4, padx=5)
                
                ctk.CTkLabel(row, text=f"🛡️ {mod}", width=150, anchor="w").pack(side="left", padx=10)
                
                # Visual Bar for Hardening Depth
                bar_bg = ctk.CTkFrame(row, fg_color="#333333", height=10, width=200)
                bar_bg.pack(side="left", padx=10)
                depth_width = min(200, count * 40)
                ctk.CTkFrame(bar_bg, fg_color="#00FFFF", height=10, width=depth_width).place(x=0, y=0)
                
                ctk.CTkLabel(row, text=f"Depth: {count}").pack(side="left", padx=5)

            ctk.CTkButton(hud, text="Trigger Logic hardening", fg_color="#0088FF", 
                         command=lambda: [self.engine.evolve_test_suite(), hud.destroy(), self.add_log_to_ui("IMMUNE: Recursive logic hardening triggered.")]).pack(pady=20)

        # Persona Buttons
        for p in personas:
            btn = ctk.CTkButton(tuner, text=p, fg_color="#333333", hover_color="#444444",
                             command=lambda x=p: apply_persona(x))
            btn.pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(tuner, text="🧬 Strategy Lab", fg_color="#0088FF", 
                    command=open_strategy_lab).pack(pady=15, padx=20, fill="x")

        # Assuming 'metrics_area' is a frame within 'tuner' or 'self'
        # For now, let's add them directly to 'tuner' for simplicity,
        # or create a new frame if the user intended a specific layout.
        # Based on the diff, it seems 'metrics_area' was implied.
        # Let's create a placeholder frame for these buttons.
        metrics_area = ctk.CTkFrame(tuner, fg_color="transparent")
        metrics_area.pack(fill="x", padx=20, pady=10)

        # Buttons
        ctk.CTkButton(metrics_area, text="📊 Open Evolution Metrics Lab", fg_color="#333333", hover_color="#444444", 
                    command=open_metrics_lab).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(metrics_area, text="🛡️ Open Deep Test HUD", fg_color="#333333", hover_color="#444444", 
                    command=open_deep_test_hud).pack(pady=5, padx=20, fill="x")

    def change_personality(self, new_p):
        self.engine.config["personality"] = new_p
        self.engine.save_config(self.engine.config)
        self.personality_label.configure(text=f"Persona: {new_p}")
        self.add_log_to_ui(f"SYSTEM: EVOLUTIONARY SHIFT -> {new_p} logic active.")
        self.apply_personality_theme()

    def update_personality_theme(self, personality):
        themes = {
            "Default": {"color": "#00FFAA", "text": "Engine: AUTONOMOUS"},
            "Performance": {"color": "#00AAFF", "text": "Engine: HIGH PRIORITY"},
            "Safety": {"color": "#FFC107", "text": "Engine: DEEP SCANNING"},
            "Aesthetic": {"color": "#A371F7", "text": "Engine: DESIGN POLISH"}
        }
        theme = themes.get(personality, themes["Default"])
        self.status_label.configure(text=theme["text"], text_color=theme["color"])
        self.nav_label.configure(text_color=theme["color"])
        
    def update_dashboard_aesthetic(self, state):
        """[v4.15] Shifts UI palette based on metabolic state."""
        aesthetics = {
            "SPRINT": {"status_bg": "#FF0055", "text": "#00FFFF", "pulse": 50},
            "STEADY": {"status_bg": "#1A1A1A", "text": "#00FFAA", "pulse": 200},
            "RECHARGE": {"status_bg": "#332200", "text": "#FFCC00", "pulse": 1000}
        }
        if state not in aesthetics: return
        style = aesthetics[state]
        self.status_label.configure(fg_color=style["status_bg"], text_color=style["text"])
        self.navigation_frame.configure(fg_color=style["status_bg"])
        self.current_metabolic_state = state
        self.add_log(f"AESTHETIC SYNC: Shifted to {state} palette.")
        
        # [v4.15] Broadcast feedback for resonance calculation
        intensity = 0.8 if state == "SPRINT" else 0.2 if state == "RECHARGE" else 0.5
        self.engine.broadcast_signal("metabolic_feedback", {"state": state, "intensity": intensity})
        
    def add_log_to_ui(self, msg):
        log_line = self.engine.append_log(msg)
        self.log_box.insert("end", log_line)
        self.log_box.see("end")

    def trigger_backup(self):
        success, info = self.engine.perform_backup()
        if success:
            self.add_log_to_ui(f"Backup created: {info.split('/')[-1]}")
            self.engine.speak("Safety backup completed successfully.")
        else:
            self.add_log_to_ui(f"Backup failed: {info}")

    def trigger_cleanup(self):
        count = self.engine.cleanup_old_data(days=1)
        self.add_log_to_ui(f"Cleanup finished. Removed {count} old backups.")

    def trigger_report(self):
        report_file = self.engine.generate_evolution_report()
        self.add_log_to_ui(f"Report generated: {report_file}")
        self.engine.speak("Evolution report generated.")

    def trigger_docs(self):
        stats = self.engine.get_project_stats()
        sloc = self.engine.count_sloc()
        readme_content = f"""# Autonomous AI Evolution Environment
Enabled 24/7 autonomous project development.

## 📊 Live Metrics
- **Current SLOC:** {sloc}
- **File Count:** {stats['files']}
- **Last Sync:** {time.strftime('%Y-%m-%d %H:%M:%S')}

## 🛠️ Features
- Real-time Monitoring & Dashboard
- Autonomous Dependency Healing
- Self-Testing & Refactor Preview
- Historical Time-Machine
- Voice Notifications (TTS)

*Generated autonomously by the evolution engine.*
"""
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        self.add_log_to_ui("README.md synchronized with current state.")
        self.engine.speak("Documentation updated.")

    def trigger_arch(self):
        arch_file = self.engine.generate_dependency_graph()
        self.add_log_to_ui(f"Architecture mapped: {arch_file}")

    def trigger_commit(self):
        success, msg = self.engine.git_commit("Manual Evolution Snapshot")
        if success:
            self.add_log_to_ui("Snapshot committed to repository.")
            self.engine.speak("Evolution state saved to version control.")
        else:
            self.add_log_to_ui(f"Commit failed: {msg}")

    def trigger_tests(self):
        self.add_log_to_ui("Running autonomous test suite...")
        res = self.engine.run_self_tests()
        self.test_health_label.configure(text=f"Tests: {res['passed']}/{res['total']} PASSED", text_color="#00FFAA" if res['passed'] == res['total'] and res['total'] > 0 else "#FFAA00")
        self.add_log_to_ui(f"Test Results: {res['passed']}/{res['total']} successful.")

    def open_analytics(self):
        self.analytics_window = ctk.CTkToplevel(self)
        self.analytics_window.title("Evolution Performance Analytics")
        self.analytics_window.geometry("700x500")
        
        header = ctk.CTkLabel(self.analytics_window, text="High-Resolution Resource Trends", font=ctk.CTkFont(size=16, weight="bold"))
        header.pack(pady=10)
        
        self.analytics_canvas = ctk.CTkCanvas(self.analytics_window, height=350, bg="#1A1A1A", highlightthickness=0)
        self.analytics_canvas.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.refresh_analytics_chart()

    def refresh_analytics_chart(self):
        if not hasattr(self, "analytics_canvas") or not self.analytics_window.winfo_exists():
            return
            
        self.analytics_canvas.delete("all")
        w = self.analytics_canvas.winfo_width()
        h = self.analytics_canvas.winfo_height()
        if w < 10: w = 660 # fallback
        if h < 10: h = 330
        
        # Grid lines
        for i in range(0, 101, 20):
            y = h - (i * h / 100)
            self.analytics_canvas.create_line(0, y, w, y, fill="#333333", dash=(4, 4))
            self.analytics_canvas.create_text(10, y-10, text=f"{i}%", fill="#666666", font=("Arial", 8))

        # CPU Chart
        self.draw_plot(self.analytics_canvas, self.engine.history["cpu"], "#00AAFF", w, h, "CPU")
        # RAM Chart
        self.draw_plot(self.analytics_canvas, self.engine.history["ram"], "#00FFAA", w, h, "RAM")
        # Health Chart (scaled for visibility)
        health_data = [min(100, x * 10) for x in self.engine.history["health"]]
        self.draw_plot(self.analytics_canvas, health_data, "#FFAA00", w, h, "HEALTH")

    def draw_plot(self, canvas, data, color, w, h, label):
        if not data: return
        points = []
        step = w / (len(data) - 1 if len(data) > 1 else 1)
        for i, val in enumerate(data):
            x = i * step
            y = h - (val * h / 100)
            points.append((x, y))
            
        if len(points) > 1:
            for i in range(len(points)-1):
                canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill=color, width=2)
        
        # Legend
        if label == "CPU": offset = 20
        elif label == "RAM": offset = 50
        else: offset = 80 # HEALTH
        
        canvas.create_rectangle(w-95, offset, w-85, offset+10, fill=color)
        canvas.create_text(w-80, offset+5, text=label, fill="white", anchor="w", font=("Arial", 10))

    def open_refactor_preview(self):
        issues = self.engine.check_code_health()
        if not issues: return
        
        orig, suggested = self.engine.get_refactor_preview(issues[0])
        
        preview_win = ctk.CTkToplevel(self)
        preview_win.title("AI Refactor Preview")
        preview_win.geometry("800x500")
        
        f1 = ctk.CTkFrame(preview_win)
        f1.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(f1, text="Original Code").pack()
        t1 = ctk.CTkTextbox(f1, width=350)
        t1.pack(fill="both", expand=True)
        t1.insert("0.0", orig)
        
        f2 = ctk.CTkFrame(preview_win)
        f2.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(f2, text="Suggested Refactoring").pack()
        t2 = ctk.CTkTextbox(f2, width=350)
        t2.pack(fill="both", expand=True)
        t2.insert("0.0", suggested)
        
        def execute_refactor():
            success, msg = self.engine.apply_refactor(issues[0].split(":")[0].strip(), orig, suggested)
            if success:
                self.add_log_to_ui("Code successfully evolved.")
                self.engine.speak("Refactor applied. Evolution goal nearing.")
                preview_win.destroy()
            else:
                self.add_log_to_ui(f"Refactor failed: {msg}")
        
        btn = ctk.CTkButton(preview_win, text="APPLY REFACTOR", command=execute_refactor, fg_color="#00FFAA", text_color="#000000")
        btn.pack(pady=10)

    def open_insights(self):
        insights_win = ctk.CTkToplevel(self)
        insights_win.title("Project Insights & Heatmap")
        insights_win.geometry("600x500")
        
        ctk.CTkLabel(insights_win, text="Top Files by SLOC", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        canvas = ctk.CTkCanvas(insights_win, height=350, bg="#1A1A1A", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=20, pady=10)
        
        data = self.engine.get_heatmap_stats()
        if not data: return
        
        max_val = max(d[1] for d in data)
        w = 560
        h = 350
        bar_w = w / len(data) - 10
        
        for i, (name, val) in enumerate(data):
            bar_h = (val / max_val) * (h - 50)
            x0 = 20 + i * (bar_w + 10)
            y0 = h - bar_h - 20
            x1 = x0 + bar_w
            y1 = h - 20
            
            canvas.create_rectangle(x0, y0, x1, y1, fill="#AA66FF", outline="#FFFFFF")
            canvas.create_text(x0 + bar_w/2, y1 + 10, text=name[:6], fill="white", font=("Arial", 8))
            canvas.create_text(x0 + bar_w/2, y0 - 10, text=str(val), fill="#AA66FF", font=("Arial", 8))

    def open_history_viewer(self):
        """Metabolic-aware 'Time-Capsule' for auditing and restoring system DNA."""
        backups = self.engine.get_backup_list()
        if not backups:
            self.add_log_to_ui("No DNA snapshots found to browse.")
            return
            
        history_win = ctk.CTkToplevel(self)
        history_win.title("🕒 Evolutionary Time-Capsule (DNA Snapshots)")
        history_win.geometry("1000x700")
        
        # Left Panel: Backup List + Metadata
        left_panel = ctk.CTkFrame(history_win, width=300)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)
        
        # Right Panel: Code Comparison
        right_panel = ctk.CTkFrame(history_win)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(left_panel, text="SNAPSHOT DNA", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        meta_box = ctk.CTkTextbox(left_panel, height=200, font=("Consolas", 10), fg_color="#1A1A1A")
        meta_box.pack(fill="x", padx=10, pady=5)
        meta_box.insert("0.0", "Select a snapshot to view DNA metadata...")
        meta_box.configure(state="disabled")

        file_entry = ctk.CTkEntry(left_panel, placeholder_text="File (e.g. system_engine.py)")
        file_entry.insert(0, "system_engine.py")
        file_entry.pack(fill="x", padx=10, pady=10)

        def load_comparison(zip_file):
            target_file = file_entry.get()
            # Update Metadata
            metadata = self.engine.get_backup_metadata(zip_file)
            meta_box.configure(state="normal")
            meta_box.delete("0.0", "end")
            if metadata:
                m_str = f"Time: {metadata['timestamp']}\nReason: {metadata['reason']}\nPersona: {metadata['personality']}\nEnergy: {metadata['energy']:.1f}%\nSLOC: {metadata['sloc']}\nSmells: {metadata['smells']}"
                meta_box.insert("0.0", m_str)
            else:
                meta_box.insert("0.0", "No metadata found (Legacy Backup)")
            meta_box.configure(state="disabled")

            # Update Diff
            old_content = self.engine.get_file_from_backup(zip_file, target_file)
            new_content = ""
            if os.path.exists(target_file):
                with open(target_file, "r", encoding="utf-8", errors='replace') as f:
                    new_content = f.read()
            
            t_old.delete("0.0", "end")
            t_old.insert("0.0", old_content)
            t_new.delete("0.0", "end")
            t_new.insert("0.0", new_content)
            
            restore_btn.configure(state="normal", command=lambda z=zip_file: trigger_rollback(z))

        scroll = ctk.CTkScrollableFrame(left_panel)
        scroll.pack(fill="both", expand=True)

        for b in backups[:15]:
            btn = ctk.CTkButton(scroll, text=b, command=lambda z=b: load_comparison(z), fg_color="#333333", height=40)
            btn.pack(fill="x", pady=2)

        def trigger_rollback(zip_file):
            if ctk.CTkInputDialog(text=f"Type 'RESTORE' to confirm DNA rollback to {zip_file}:", title="Safety Confirmation").get_input() == "RESTORE":
                success, msg = self.engine.rollback_to_snapshot(zip_file)
                if success:
                    self.add_log_to_ui(f"SYSTEM: Rollback successful. State restored to {zip_file}.")
                    self.engine.speak("System DNA stabilized. Rollback complete.")
                    history_win.destroy()
                else:
                    self.add_log_to_ui(f"ERROR: Rollback failed: {msg}")

        restore_btn = ctk.CTkButton(left_panel, text="⚡ RESTORE DNA", state="disabled", fg_color="#FFD700", text_color="#000000", hover_color="#CCAB00")
        restore_btn.pack(pady=20, fill="x", padx=10)

        diff_frame = ctk.CTkFrame(right_panel)
        diff_frame.pack(fill="both", expand=True)
        
        f_old = ctk.CTkFrame(diff_frame)
        f_old.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        ctk.CTkLabel(f_old, text="PAST DNA").pack()
        t_old = ctk.CTkTextbox(f_old, font=("Consolas", 10))
        t_old.pack(fill="both", expand=True)
        
        f_new = ctk.CTkFrame(diff_frame)
        f_new.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        ctk.CTkLabel(f_new, text="CURRENT DNA").pack()
        t_new = ctk.CTkTextbox(f_new, font=("Consolas", 10))
        t_new.pack(fill="both", expand=True)

    def open_project_tree(self):
        tree_win = ctk.CTkToplevel(self)
        tree_win.title("Visual Codebase Explorer")
        tree_win.geometry("500x600")
        
        header = ctk.CTkLabel(tree_win, text="Project Structure", font=ctk.CTkFont(size=14, weight="bold"))
        header.pack(pady=10)
        
        tree_box = ctk.CTkTextbox(tree_win, font=("Consolas", 10))
        tree_box.pack(fill="both", expand=True, padx=20, pady=20)
        
        tree_data = self.engine.get_project_tree()
        tree_box.insert("0.0", tree_data)
        tree_box.configure(state="disabled")

    def open_personality_tuner(self):
        tuner_win = ctk.CTkToplevel(self)
        tuner_win.title("AI Personality Tuner")
        tuner_win.geometry("600x600")
        
        header = ctk.CTkLabel(tuner_win, text="Advanced Persona Configuration (JSON)", font=ctk.CTkFont(size=14, weight="bold"))
        header.pack(pady=10)
        
        edit_box = ctk.CTkTextbox(tuner_win, font=("Consolas", 10))
        edit_box.pack(fill="both", expand=True, padx=20, pady=10)
        
        current_data = json.dumps(self.engine.personality_quotes, indent=2)
        edit_box.insert("0.0", current_data)
        
        def save_tuning():
            try:
                new_data = json.loads(edit_box.get("0.0", "end"))
                self.engine.update_personality_quotes(new_data)
                self.add_log_to_ui("Personality configurations updated.")
                self.engine.speak("Behavioral matrices retuned.")
                tuner_win.destroy()
            except Exception as e:
                self.add_log_to_ui(f"Invalid JSON: {e}")
        
        # Auto-Regulate Toggle
        self.reg_var = ctk.BooleanVar(value=self.engine.config.get("auto_regulate", False))
        self.reg_check = ctk.CTkCheckBox(tuner_win, text="Enable AI Self-Regulation", variable=self.reg_var, command=self.toggle_auto_regulate, font=ctk.CTkFont(size=14, weight="bold"), text_color="#00FFAA")
        self.reg_check.pack(pady=10)
        
        save_btn = ctk.CTkButton(tuner_win, text="SAVE CONFIGURATION", command=save_tuning, fg_color="#00FFAA", text_color="#000000")
        save_btn.pack(pady=20)

    def open_connectivity_hub(self):
        hub_win = ctk.CTkToplevel(self)
        hub_win.title("Structural Connectivity Hub")
        hub_win.geometry("500x500")
        
        header = ctk.CTkLabel(hub_win, text="Top Central Node Modules (Imports)", font=ctk.CTkFont(size=14, weight="bold"))
        header.pack(pady=10)
        
        stats = self.engine.get_connectivity_stats()
        
        for mod, count in stats:
            frame = ctk.CTkFrame(hub_win, fg_color="transparent")
            frame.pack(fill="x", padx=40, pady=5)
            
            ctk.CTkLabel(frame, text=f"• {mod}", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
            ctk.CTkLabel(frame, text=f"{count} references", font=ctk.CTkFont(size=11, slant="italic"), text_color="#AAAAAA").pack(side="right")
            
            # Simple bar for visualization
            pb = ctk.CTkProgressBar(hub_win, width=300, height=8)
            pb.pack(padx=40, pady=(0, 10))
            pb.set(min(1.0, count / 10)) # Normalized for visibility

    def open_cognitive_matrix(self):
        """[v4.17] Opens a fine-grained view of logic node snapshots."""
        top = ctk.CTkToplevel(self)
        top.title("Cognitive Logic Matrix")
        top.geometry("600x400")
        
        frame = ctk.CTkFrame(top)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        label = ctk.CTkLabel(frame, text="Cognitive Snapshot Vault", font=ctk.CTkFont(size=16, weight="bold"))
        label.pack(pady=10)
        
        scroll = ctk.CTkScrollableFrame(frame, width=500, height=300)
        scroll.pack(padx=10, pady=10, fill="both", expand=True)
        
        snapshots = os.listdir(self.engine.node_snapshot_dir)
        if not snapshots:
            ctk.CTkLabel(scroll, text="No snapshots captured yet.").pack(pady=20)
        else:
            for snap in sorted(snapshots, reverse=True):
                btn_frame = ctk.CTkFrame(scroll)
                btn_frame.pack(fill="x", pady=2, padx=5)
                
                name = snap.replace(".log", "")
                ctk.CTkLabel(btn_frame, text=name, font=ctk.CTkFont(size=10)).pack(side="left", padx=10)
                
                rollback_btn = ctk.CTkButton(btn_frame, text="ROLLBACK", width=80, height=22, 
                                             command=lambda n=name: self.trigger_node_rollback(n))
                rollback_btn.pack(side="right", padx=10)

    def trigger_node_rollback(self, snapshot_id: str):
        node_name = snapshot_id.split("_")[0]
        if self.engine.rollback_node(node_name, snapshot_id):
            self.add_log(f"SUCCESS: Rolled back {node_name} to {snapshot_id}")
        else:
            self.add_log(f"ERROR: Rollback failed for {snapshot_id}")
        hm_win = ctk.CTkToplevel(self)
        hm_win.title("Structural Evolution Heatmap")
        hm_win.geometry("800x600")
        
        header = ctk.CTkLabel(hm_win, text="Topographical Code Density (Color: SLOC | Size: Connections)", font=ctk.CTkFont(size=14, weight="bold"))
        header.pack(pady=10)
        
        canvas = ctk.CTkCanvas(hm_win, bg="#1a1a1a", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=20, pady=20)
        
        data = self.engine.get_heatmap_data()
        
        # Simple grid layout for blocks
        x_off: float = 20.0
        y_off: float = 20.0
        for item in data:
            # Color based on SLOC (Scale: 0-1000)
            sloc_val = min(255, int(item['sloc'] / 4))
            color = f"#{sloc_val:02x}{255-sloc_val:02x}aa" # Redder = Heavier
            
            # Size based on Connectivity
            size = float(40 + (item['connectivity'] * 10))
            
            canvas.create_rectangle(float(x_off), float(y_off), float(x_off+size), float(y_off+size), fill=color, outline="#ffffff")
            canvas.create_text(float(x_off + size/2), float(y_off + size/2), text=item['file'], fill="#ffffff", font=("Consolas", 8))
            
            x_off += size + 20
            if x_off > 700:
                x_off = 20.0
                y_off += 100.0

    def open_metrics_lab(self):
        """Opens a detailed window for long-term evolutionary telemetry analysis."""
        lab_win = ctk.CTkToplevel(self)
        lab_win.title("Evolutionary Metrics Lab")
        lab_win.geometry("900x650")
        
        header = ctk.CTkLabel(lab_win, text="Long-term Evolutionary Telemetry (performance.csv)", font=ctk.CTkFont(size=16, weight="bold"))
        header.pack(pady=15)
        
        canvas = ctk.CTkCanvas(lab_win, bg="#111111", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=30, pady=10)
        
        hist = self.engine.get_performance_history_data()
        if not hist or not hist["labels"]:
            canvas.create_text(450, 300, text="NOT ENOUGH TELEMETRY DATA YET", fill="#AAAAAA", font=("Arial", 14))
            return
            
        w, h = 840, 500
        # Plot CPU (Red)
        self.plot_lab_series(canvas, hist["cpu"], "#FF5555", w, h, "Avg CPU %")
        # Plot RAM (Cyan)
        self.plot_lab_series(canvas, hist["ram"], "#00FFAA", w, h, "Avg RAM %", offset=30)
        # Plot Smells (Orange, scaled)
        smells_scaled = [s * 10 for s in hist["smells"]]
        self.plot_lab_series(canvas, smells_scaled, "#FFAA00", w, h, "Health Smells (x10)", offset=60)
        
    def plot_lab_series(self, canvas, data, color, w, h, label, offset=0):
        if not data: return
        points = []
        step = w / (len(data) - 1 if len(data) > 1 else 1)
        for i, val in enumerate(data):
            x = i * step + 30
            y = h - (val * h / 110) - 20 # Leave room for bottom axes
            points.append((x, y))
            
        if len(points) > 1:
            canvas.create_line([p for pt in points for p in pt], fill=color, width=3, smooth=True)
            
        # Markers and Legend
        lx = 50 + offset * 3
        canvas.create_rectangle(lx, 10, lx+15, 25, fill=color)
        canvas.create_text(lx+20, 18, text=label, fill="white", anchor="w", font=("Arial", 9))

    def trigger_heal(self):
        missing = self.engine.check_dependencies()
        if not missing: return
        self.add_log_to_ui(f"Healing {len(missing)} dependencies: {missing}")
        for pkg in missing:
            success, msg = self.engine.install_dependency(pkg)
            if success:
                self.add_log_to_ui(f"Healed: {pkg}")
                self.engine.speak(f"Successfully installed package {pkg}")
            else:
                self.add_log_to_ui(f"Heal failed for {pkg}: {msg}")
        self.update_dependency_status()

    def update_dependency_status(self):
        missing = self.engine.check_dependencies()
        if missing:
            self.deps_label.configure(text=f"Package Health: {len(missing)} MISSING ({', '.join(missing)})", text_color="#FF3333")
            self.heal_btn.pack(side="left", padx=10)
        else:
            self.deps_label.configure(text="Package Health: PERFECT", text_color="#00FFAA")
            self.heal_btn.pack_forget()

    def update_sync_status(self):
        endpoint = self.engine.config.get("telemetry_endpoint")
        if not endpoint:
            self.sync_label.configure(text="📡 SYNC: DISABLED", text_color="#666666")
        else:
            self.sync_label.configure(text="📡 SYNC: READY", text_color="#00FFAA")

    def trigger_pulse_pull(self):
        if not self.engine.config.get("command_endpoint"): return
        
        self.sync_label.configure(text="📡 SYNC: PULSE", text_color="#FFD700")
        success, msg = self.engine.poll_remote_commands()
        if success and ("Shifted" in msg or "Backup" in msg):
            self.add_log_to_ui(f"REMOTE: {msg}")
            # Visual confirmation pulse
            self.after(500, lambda: self.sync_label.configure(text_color="#FFFFFF"))
            self.after(1000, self.update_sync_status)
        else:
            self.after(500, self.update_sync_status)

    def open_arch_editor(self):
        win = ctk.CTkToplevel(self)
        win.title("Architectural Node Editor (BETA)")
        win.geometry("900x700")
        
        data = self.engine.get_node_link_data()
        nodes = data["nodes"]
        links = data["links"]
        
        canvas = ctk.CTkCanvas(win, bg="#111111", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # --- Auto-Layout Control ---
        def trigger_auto_layout():
            self.engine.optimize_visual_layout()
            self.add_log_to_ui("ARCH: Visual layout self-optimized via gravity engine.")
            win.destroy() # Re-open for simplicity or I could redraw
            self.open_arch_editor()

        layout_btn = ctk.CTkButton(win, text="✨ AUTO-LAYOUT", command=trigger_auto_layout, 
                                  fg_color="#00FFAA", text_color="#000000", width=120)
        layout_btn.place(x=20, y=20)

        # --- Stress Lab Overlay ---
        stress_frame = ctk.CTkFrame(win, fg_color="#1A1A1A", height=150)
        stress_frame.pack(fill="x", side="bottom")
        
        ctk.CTkLabel(stress_frame, text="☢️ PREDICTIVE STRESS LAB (What-If)", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FF5555").pack(pady=5)
        
        ctrl_frame = ctk.CTkFrame(stress_frame, fg_color="transparent")
        ctrl_frame.pack(fill="x", padx=20)
        
        ctk.CTkLabel(ctrl_frame, text="Extra Coupling:").grid(row=0, column=0, padx=5)
        coupling_slider = ctk.CTkSlider(ctrl_frame, from_=0, to=5, number_of_steps=50, width=200)
        coupling_slider.grid(row=0, column=1, padx=5)
        coupling_slider.set(0)
        
        ctk.CTkLabel(ctrl_frame, text="SLOC Injection:").grid(row=0, column=2, padx=5)
        sloc_slider = ctk.CTkSlider(ctrl_frame, from_=0, to=2000, number_of_steps=20, width=200)
        sloc_slider.grid(row=0, column=3, padx=5)
        sloc_slider.set(0)
        
        sim_canvas = ctk.CTkCanvas(stress_frame, height=80, bg="#000000", highlightthickness=0)
        sim_canvas.pack(fill="x", padx=20, pady=10)
        
        def run_sim(event=None):
            sim_canvas.delete("all")
            hist = self.engine.simulate_architectural_stress(coupling_slider.get(), sloc_slider.get())
            w = sim_canvas.winfo_width()
            h = sim_canvas.winfo_height()
            if w < 10: w = 840
            
            # Draw Health (Orange) and Energy (Gold) predictions
            points_h = []
            points_e = []
            step = w / 59
            for i in range(60):
                points_h.append((i*step, h - (hist["health"][i] * h / 100)))
                points_e.append((i*step, h - (hist["energy"][i] * h / 100)))
            
            sim_canvas.create_line([p for pt in points_h for p in pt], fill="#FFAA00", width=2)
            sim_canvas.create_line([p for pt in points_e for p in pt], fill="#FFD700", width=2, dash=(2, 2))
            sim_canvas.create_text(10, 10, text="Health Decay Prediction (60 Cycles)", fill="#FFAA00", anchor="w", font=("Arial", 8))
            
        coupling_slider.configure(command=run_sim)
        sloc_slider.configure(command=run_sim)
        # --------------------------
        
        node_radius = 35
        node_objs = {} # id -> canvas_id

        # Draggable and Neural-Path logic
        drag_data = {"x": 0, "y": 0, "item": None}
        propagation_mode = {"active": False, "source": None}

        def on_press(event):
            closest = canvas.find_closest(event.x, event.y)[0]
            if closest in node_id_map:
                nid = node_id_map[closest]
                # Toggle Neural-Path Mode
                if propagation_mode["source"] == nid:
                    reset_propagation()
                else:
                    trigger_propagation(nid)
                    
            drag_data["item"] = closest
            drag_data["x"] = event.x
            drag_data["y"] = event.y

        def trigger_propagation(nid):
            propagation_mode["active"] = True
            propagation_mode["source"] = nid
            path = self.engine.get_impact_propagation_path(nid)
            
            # Visual Feedback: Dim all, highlight path
            for node_id, c_id in node_objs.items():
                if node_id in path:
                    # Highlight impacted node
                    dist = path[node_id]
                    color = "#FF00FF" if dist > 0 else "#00FFFF" # Cyan source, Magenta downstream
                    canvas.itemconfig(c_id, outline=color, width=4)
                    # Add Contagion Ring
                    coords = canvas.coords(c_id)
                    canvas.create_oval(coords[0]-10, coords[1]-10, coords[2]+10, coords[3]+10, 
                                     outline=color, width=1, tags=("ring", f"ring_{node_id}"))
                else:
                    # Dim unaffected node
                    canvas.itemconfig(c_id, outline="#333333", width=1)
            self.add_log_to_ui(f"NEURAL-PATH: Visualizing contagion from '{nid}' ({len(path)-1} affected).")

        def reset_propagation():
            propagation_mode["active"] = False
            propagation_mode["source"] = None
            canvas.delete("ring")
            for nid, c_id in node_objs.items():
                canvas.itemconfig(c_id, outline="#00FFAA", width=2)
            self.add_log_to_ui("NEURAL-PATH: Visualization reset.")

        def on_release(event):
            if drag_data["item"] in node_id_map:
                nid = node_id_map[drag_data["item"]]
                coords = canvas.coords(drag_data["item"])
                cx = (coords[0] + coords[2]) / 2
                cy = (coords[1] + coords[3]) / 2
                self.engine.update_node_position(nid, cx, cy)
            drag_data["item"] = None

        def on_motion(event):
            if drag_data["item"]:
                dx = event.x - drag_data["x"]
                dy = event.y - drag_data["y"]
                canvas.move(drag_data["item"], dx, dy)
                # Move associated text
                tags = canvas.gettags(drag_data["item"])
                if tags:
                    canvas.move(f"text_{tags[0]}", dx, dy)
                # Move associated rings
                if tags:
                    canvas.move(f"ring_{tags[0]}", dx, dy)
                drag_data["x"] = event.x
                drag_data["y"] = event.y
                redraw_links()

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<ButtonRelease-1>", on_release)
        canvas.bind("<B1-Motion>", on_motion)

        # Neural-Flow Animation State
        self.neural_packets = [] # List of {id, x, y, target_id, speed, color}
        
        def animate_neural_flow():
            if not win.winfo_exists(): return
            
            canvas.delete("packet")
            activity = self.engine.get_module_activity()
            
            # 1. Spawn new packets
            for link in links:
                src = link["source"]
                tgt = link["target"]
                if src in node_objs and tgt in node_objs:
                    act_level = activity.get(src, 0.1)
                    # Chance to spawn based on activity
                    if random.random() < (act_level * 0.2):
                        s_coords = canvas.coords(node_objs[src])
                        sx = (s_coords[0] + s_coords[2]) / 2
                        sy = (s_coords[1] + s_coords[3]) / 2
                        
                        t_coords = canvas.coords(node_objs[tgt])
                        tx = (t_coords[0] + t_coords[2]) / 2
                        ty = (t_coords[1] + t_coords[3]) / 2
                        
                        # Packets move faster if heat is high
                        speed = 0.05 + (act_level * 0.15)
                        p_color = "#FF00FF" if act_level > 0.7 else "#00FFFF"
                        
                        self.neural_packets.append({
                            "tx": sx, "ty": sy, # Current pos
                            "dest_x": tx, "dest_y": ty,
                            "progress": 0.0,
                            "speed": speed,
                            "color": p_color
                        })
            
            # 2. Update and Draw packets
            remaining = []
            for p in self.neural_packets:
                p["progress"] += p["speed"]
                if p["progress"] < 1.0:
                    prog = p["progress"]
                    # Interpolate
                    curr_x = p["tx"] + (p["dest_x"] - p["tx"]) * prog
                    curr_y = p["ty"] + (p["dest_y"] - p["ty"]) * prog
                    
                    canvas.create_oval(curr_x-3, curr_y-3, curr_x+3, curr_y+3, 
                                     fill=p["color"], outline="", tags="packet")
                    remaining.append(p)
            self.neural_packets = remaining
            
            canvas.after(50, animate_neural_flow)

        # Start animation
        animate_neural_flow()

        def redraw_links():
            canvas.delete("link")
            for link in links:
                if link["source"] in node_objs and link["target"] in node_objs:
                    s_coords = canvas.coords(node_objs[link["source"]])
                    t_coords = canvas.coords(node_objs[link["target"]])
                    sx = (s_coords[0] + s_coords[2]) / 2
                    sy = (s_coords[1] + s_coords[3]) / 2
                    tx = (t_coords[0] + t_coords[2]) / 2
                    ty = (t_coords[1] + t_coords[3]) / 2
                    # Enhanced Directionality: Deep highlight for core foundational dependencies
                    link_color = "#00FFAA" if link["target"] in ["system_engine", "main_app"] else "#555555"
                    canvas.create_line(sx, sy, tx, ty, fill=link_color, width=2, tags="link", arrow="last", arrowshape=(10, 12, 5))

        # Tooltip Logic
        tooltip_label = ctk.CTkLabel(win, text="", fg_color="#333333", text_color="#00FFAA", corner_radius=5)
        
        def show_tooltip(event, node_id, sloc):
            # Calculate connectivity for this node
            conn = 0
            for l in links:
                if l["source"] == node_id or l["target"] == node_id:
                    conn += 1
            e_score = self.engine.get_entanglement_score(node_id)
            tooltip_label.configure(text=f"Module: {node_id}\nSLOC: {sloc}\nConnect: {conn}\nEntangle: {e_score:.2f}")
            tooltip_label.place(x=event.x_root - win.winfo_rootx() + 10, y=event.y_root - win.winfo_roottx() + 10)

        def hide_tooltip(event):
            tooltip_label.place_forget()

        # Initial Layout
        node_id_map = {} # canvas_id -> node_id
        import math
        center_x, center_y = 450, 350
        radius = 200
        for i, node in enumerate(nodes):
            nid = node["id"]
            if nid in self.engine.node_positions:
                nx, ny = self.engine.node_positions[nid]
            else:
                angle = (2 * math.pi * i) / len(nodes)
                nx = center_x + radius * math.cos(angle)
                ny = center_y + radius * math.sin(angle)
            
            # Dynamic scaling and coloring based on SLOC & Entanglement (Semantic Heatmap)
            nr = int(20 + math.sqrt(node["sloc"]) * 1.5)
            e_score = self.engine.get_entanglement_score(nid)
            
            # Color blending: Cyan (0.0) to Red (1.0)
            red = int(255 * e_score)
            green = int(255 * (1.0 - e_score))
            quality_color = f"#{red:02x}{green:02x}aa" # Semi-transparent-like cyan/red mix
            
            if nid in self.engine.current_anomalies:
                quality_color = "#FF00FF" # Magenta (ANOMALY) priority
            elif node["sloc"] > 500: 
                quality_color = "#FF5555" # Critical Complexity
            elif node["sloc"] > 200: 
                quality_color = "#FFAA00" # Warning Threshold
            
            c_id = canvas.create_oval(nx-nr, ny-nr, nx+nr, ny+nr, 
                                     fill="#1A1A1A", outline=quality_color, width=3 if nid in self.engine.current_anomalies else 2, tags=nid)
            canvas.create_text(nx, ny, text=nid, fill="white", font=("Arial", 10, "bold"), tags=f"text_{nid}")
            
            node_objs[nid] = c_id
            node_id_map[c_id] = nid
            
            # Interactive Tooltips
            canvas.tag_bind(c_id, "<Enter>", lambda e, nid=node["id"], ns=node["sloc"]: show_tooltip(e, nid, ns))
            canvas.tag_bind(c_id, "<Leave>", hide_tooltip)
            
        def animate_pulse():
            import math
            t = time.time()
            for nid, c_id in node_objs.items():
                # Check if this node was recently healed (within 1 hour)
                heal_time = self.engine.healed_registry.get(f"{nid}.py", 0)
                if t - heal_time < 3600:
                    # Pulse effect: cycle width from 2 to 6
                    pulse = 2 + 4 * (0.5 + 0.5 * math.sin(t * 5))
                    canvas.itemconfig(c_id, width=pulse, outline="#00FFBC")
                else:
                    canvas.itemconfig(c_id, width=2, outline="#00FFAA")
            
            if win.winfo_exists():
                win.after(100, animate_pulse)

        redraw_links()
        animate_pulse()

    def open_time_travel(self):
        snaps = self.engine.get_history_snapshots()
        if not snaps:
            self.add_log_to_ui("No snapshots available for time travel yet.")
            return

        window = ctk.CTkToplevel(self)
        window.title("Evolutionary Time Travel")
        window.geometry("1000x700")
        
        title_lbl = ctk.CTkLabel(window, text="VISUAL EVOLUTION HISTORY", font=ctk.CTkFont(size=20, weight="bold"))
        title_lbl.pack(pady=10)

        info_lbl = ctk.CTkLabel(window, text=f"Snapshot: {snaps[-1]['time']}", font=ctk.CTkFont(size=12))
        info_lbl.pack()

        # Image Display
        img_frame = ctk.CTkFrame(window, fg_color="#000000")
        img_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        img_lbl = ctk.CTkLabel(img_frame, text="")
        img_lbl.pack(fill="both", expand=True)

        def update_snapshot(val):
            idx = int(float(val))
            if 0 <= idx < len(snaps):
                snap = snaps[idx]
                info_lbl.configure(text=f"Snapshot: {snap['time']} ({idx+1}/{len(snaps)})")
                try:
                    from PIL import Image
                    pil_img = Image.open(snap['path'])
                    # Scale to fit frame reasonably
                    w, h = pil_img.size
                    scale = min(960/w, 540/h)
                    new_size = (int(w*scale), int(h*scale))
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=new_size)
                    img_lbl.configure(image=ctk_img)
                    img_lbl.image = ctk_img # Keep reference
                except Exception as e:
                    img_lbl.configure(text=f"Error loading snapshot: {e}")

        # Slider
        slider = ctk.CTkSlider(window, from_=0, to=len(snaps)-1, number_of_steps=len(snaps)-1, command=update_snapshot)
        slider.pack(fill="x", padx=40, pady=20)
        slider.set(len(snaps)-1)
        update_snapshot(len(snaps)-1)

    def update_telemetry(self):
        # Calculate Adaptive Heartbeat
        new_interval = self.engine.calculate_adaptive_heartbeat()
        self.update_heartbeat_visual(new_interval)
        
        stats = self.engine.get_system_stats()
        # Add smells to stats for history tracking
        issues = self.engine.check_code_health()
        stats["smells"] = len(issues)
        
        self.engine.update_history(stats)
        
        # Neural Pulse-Pull (every ~20 seconds if endpoint exists)
        if int(time.time()) % 20 == 0:
            self.trigger_pulse_pull()
        else:
            self.update_sync_status()
        
        # Update Dashboard UI components
        
        # Forecast Update
        trend, color = self.engine.get_health_forecast()
        self.forecast_label.configure(text=f"Trend: {trend}", text_color=color)
        
        self.cpu_label.configure(text=f"CPU: {stats.get('cpu', stats.get('cpu_percent', '?'))}%")
        self.cpu_bar.set(stats.get('cpu', stats.get('cpu_percent', 0))/100)
        
        self.ram_label.configure(text=f"RAM: {stats.get('ram_percent', '?')}% ({stats.get('ram_used_mb', stats.get('ram_used_gb', '?'))}MB)")
        self.ram_bar.set(stats.get('ram_percent', 0)/100)
        
        self.disk_label.configure(text=f"Disk: {stats.get('disk_percent', '?')}% ({stats.get('disk_free_gb', '?')}GB Free)")
        self.disk_bar.set(stats.get('disk_percent', 0)/100)
        # Energy HUD (v4.9 Predictive-Regeneration)
        state = stats.get("metabolic_state", "STEADY")
        h_eff = stats.get("harvest_efficiency", 1.0)
        
        if state != self.current_metabolic_state:
            self.update_dashboard_aesthetic(state)
            
        self.harvest_label.configure(text=f"🔋 HARVEST: {int(h_eff*100)}%", text_color="#AAFFAA" if h_eff >= 1.0 else "#FFAAAA")
            
        predicted_dip = stats.get("energy_predict", 100.0) < 30.0
        is_buffering = self.engine.buffering_target_energy > 0
        
        if state == "RECHARGE":
            bar_color = "#00FFFF" # Azure / Cyan
            status_text = f"⚡ REGEN: {int(stats.get('energy', 0))}% {'(PREDICTIVE)' if predicted_dip else '(CRITICAL)'}"
            self.regen_label.configure(text="⚡ REGEN: ACTIVE", text_color="#00FFFF")
        elif state == "SPRINT":
            bar_color = "#FF3333" # Crimson
            status_text = f"Energy: {int(stats.get('energy', 0))}% [SPRINT]"
            self.regen_label.configure(text="⚡ REGEN: OFF", text_color="#555555")
        elif is_buffering:
            bar_color = "#00FFFF" # Cyan
            status_text = f"Energy: {int(stats.get('energy', 0))}% (BUFFERING)"
            self.regen_label.configure(text="⚡ REGEN: OFF", text_color="#555555")
        else:
            energy = stats.get("energy", 50)
            if energy > 70: bar_color = "#00FFAA"
            elif energy > 30: bar_color = "#FFAA00"
            else: bar_color = "#FF4444"
            status_text = f"Energy: {int(energy)}% [{state}]"
            self.regen_label.configure(text="⚡ REGEN: OFF", text_color="#555555")

        self.energy_bar.configure(progress_color=bar_color)
        self.energy_label.configure(text=status_text)
        self.energy_bar.set(stats.get('energy', 0)/100)
        
        self.up_label.configure(text=f"Upload: {stats.get('net_up_kb', 0.0):.1f} KB/s")
        self.down_label.configure(text=f"Download: {stats.get('net_down_kb', 0.0):.1f} KB/s")
        
        # Project stats (every 5s roughly via modulo or separate counter, here just simplified)
        p_stats = self.engine.get_project_stats()
        sloc = self.engine.count_sloc()
        self.file_stat.configure(text=f"Files: {p_stats['files']}")
        self.dir_stat.configure(text=f"Dirs: {p_stats['dirs']}")
        self.sloc_stat.configure(text=f"Lines of Code: {sloc}")
        
        # Breakdown update
        bd = self.engine.get_code_breakdown()
        bd_str = "\n".join([f"{k}: {v}" for k, v in bd.items() if v > 0])
        self.breakdown_text.configure(text=bd_str)
        
        # Evolution Goals update
        goal_status = self.engine.get_goal_status()
        if not self.goal_widgets:
            for g in goal_status:
                g_lbl = ctk.CTkLabel(self.goals_frame, text=f"{g['name']}: {g['current']}/{g['target']}", font=ctk.CTkFont(size=10))
                g_lbl.pack()
                g_bar = ctk.CTkProgressBar(self.goals_frame, height=8)
                g_bar.pack(fill="x", padx=20, pady=(0, 10))
                self.goal_widgets.append((g_lbl, g_bar))
        
        for i, g in enumerate(goal_status):
            self.goal_widgets[i][0].configure(text=f"{g['name']}: {g['current']}/{g['target']}")
            self.goal_widgets[i][1].set(g['percent'])
            if g['percent'] >= 1.0: self.goal_widgets[i][1].configure(progress_color="#00FF00")

        # Divergence Update
        sims = stats.get("simulations", 0)
        bias = stats.get("personality_bias", "Default")
        vision = stats.get("next_vision", "Evolution")
        
        if sims > 0:
            self.divergence_label.configure(text=f"🧬 DIVERGENCE: {sims} PATHS [{bias.upper()} BIAS]")
        else:
            self.divergence_label.configure(text="")
            
        self.vision_label.configure(text=f"🔭 VISION: {vision.upper()}")

        # Synapse Update
        syn = stats.get("synapse", {"accepted": 0, "suppressed": 0})
        self.synapse_label.configure(text=f"🧠 SYNAPSE: {syn['accepted']}/{syn['accepted']+syn['suppressed']}")
        
        # Resonance Update
        res = stats.get("resonance", 1.0)
        self.resonance_label.configure(text=f"📈 RESONANCE: {res*100:.1f}%")
        
        # Swarm Update (v4.10)
        nodes = stats.get("active_nodes", 0)
        self.cluster_label.configure(
            text=f"🧵 SWARM: {nodes if nodes > 0 else 'IDLE'}", 
            text_color="#00FFAA" if nodes > 0 else "#555555"
        )
            
        # Entropy Update
        ent = stats.get("entropy", 0.1)
        self.entropy_label.configure(text=f"📉 ENTROPY: {ent:.2f}")
        
        # Synesthesia Update
        bias = stats.get("synesthesia", 0.5)
        self.synesthesia_label.configure(text=f"🔗 SYNESTHESIA: {bias*100:.0f}%")
        # pulse_val = stats.get("pulse", 0.5)
        # self.update_pulse_viz(pulse_val, bias)

        if stats.get("is_healing", False):
            self.healing_label.configure(text="💉 HEALING ACTIVE")
        else:
            self.healing_label.configure(text="")

        if stats.get("tuning_event", False):
            self.vision_label.configure(text="🔭 VISION: 🧬 TUNING", text_color="#FFAA00")
        else:
            self.vision_label.configure(text=f"🔭 VISION: {vision.upper()}", text_color="#FFFFFF")

        # Consciousness Monitor (v4.11)
        audit = stats.get("structural_audit", 0.0)
        self.consciousness_label.configure(text=f"🧠 CONSCIOUSNESS: {audit*100:.1f}%")
        
        # Consensus HUD (v4.19)
        c_active = stats.get("consensus_active", False)
        self.consensus_label.configure(
            text=f"🛰️ CONSENSUS: {'ACTIVE' if c_active else 'IDLE'}",
            text_color="#00FFAA" if c_active else "#AAAAAA"
        )

        # [v4.20] Governor Telemetry
        gov_active = stats.get("governor_status", True)
        gov_text = "🛡️ GOVERNOR: ACTIVE" if gov_active else "🛡️ GOVERNOR: THROTTLED"
        gov_color = "#55FF55" if gov_active else "#FF5555"
        self.governor_label.configure(text=gov_text, text_color=gov_color)

        # [v4.21] Thermal Telemetry
        thermal = stats.get("thermal_score", 0.0)
        t_color = "#00FFFF" # Cyan (Cold)
        if thermal > 80: t_color = "#FF3333" # Red (Critical)
        elif thermal > 60: t_color = "#FF9933" # Orange (High)
        elif thermal > 30: t_color = "#00FFAA" # Green (Nominal)
        
        t_status = "STRETCHED" if thermal > 80 else "NOMINAL" if thermal > 30 else "COLD"
        self.thermal_label.configure(text= f"🔥 THERMAL: {thermal}% ({t_status})", text_color=t_color)

        # [v4.22] Memory Telemetry
        mem_pressure = stats.get("memory_pressure", 0.0)
        m_color = "#AAAAFF" # Default light blue
        if mem_pressure > 80: m_color = "#FF3333" # Red
        elif mem_pressure > 50: m_color = "#FFFF33" # Yellow
        
        m_status = "CRITICAL" if mem_pressure > 80 else "TRIMMING" if mem_pressure > 50 else "SAFE"
        self.memory_label.configure(text=f"💾 MEMORY: {m_status}", text_color=m_color)

        # [v4.23] Healer Telemetry
        h_status = stats.get("healing_status", "IDLE")
        h_color = "#AAAAAA" # IDLE/STABLE = Gray
        if h_status == "SCANNING": h_color = "#FFFF33" # Yellow
        elif h_status == "REPAIRING": h_color = "#FF3333" # Red
        elif h_status == "STABLE": h_color = "#55FF55" # Green
        
        self.healer_label.configure(text=f"🩺 HEALER: {h_status}", text_color=h_color)

        # [v4.24] Refiner Telemetry
        r_status = stats.get("refiner_status", "SLEEPING")
        r_color = "#AAAAAA" # Default SLEEPING
        if r_status == "THINKING": r_color = "#FFFF33" # Yellow
        elif r_status == "REFINING": r_color = "#FF9933" # Orange
        elif r_status == "POLISHED": r_color = "#55FF55" # Green
        
        self.refiner_label.configure(text=f"🧬 REFINER: {r_status}", text_color=r_color)

        # [v4.25] Consensus Telemetry
        c_strength = stats.get("consensus_strength", 100.0)
        c_active = stats.get("consensus_active", False)
        
        c_color = "#55FF55" # STABLE (Green)
        c_status = "STABLE"
        if c_strength < 50: 
            c_color = "#FF3333" # DIVERGING (Red)
            c_status = "DIVERGING"
        elif c_strength < 80: 
            c_color = "#FFFF33" # CONVERGING (Yellow)
            c_status = "CONVERGING"
        
        if not c_active and c_strength == 100.0:
            c_status = "IDLE"
            c_color = "#AAAAAA"

        self.consensus_label.configure(text=f"🛰️ CONSENSUS: {c_status} ({c_strength}%)", text_color=c_color)

        # [v4.26] Governor Telemetry
        g_status = stats.get("governor_status", "ACTIVE")
        g_color = "#55FF55" # ACTIVE (Green)
        if g_status == "ALERT": g_color = "#FFFF33" # Yellow
        elif g_status == "REVERTING": g_color = "#FF3333" # Red
        elif g_status == "STANDBY": g_color = "#AAAAAA" # Gray
        
        self.governor_label.configure(text=f"🛡️ GOVERNOR: {g_status}", text_color=g_color)

        if hasattr(self.engine, "revenue"):
            rev_prog = self.engine.revenue.get_progress()
            self.revenue_bar.set(rev_prog["percentage"])
            self.revenue_status.configure(text=f"{rev_prog['current_ntd']} / {rev_prog['target_ntd']} NTD")

        # Health Update
        issues = self.engine.check_code_health()
        if not issues:
            self.health_label.configure(text="Code Health: EXCELLENT", text_color="#00FFAA")
            self.smells_label.configure(text="")
        else:
            self.health_label.configure(text=f"Code Health: {len(issues)} SMELLS", text_color="#FFAA00")
            # get_refactor_advice is not implemented — show issue names directly
            advice = [f"{i[1]}({i[2]}L)" for i in issues[:3]]
            self.smells_label.configure(text=" | ".join(advice))
            
        # Timeline Update
        current_timeline = "\n".join([f"[{e['time']}] {e['type']}: {e['msg']}" for e in self.engine.event_history])
        self.timeline_box.configure(state="normal")
        self.timeline_box.delete("0.0", "end")
        self.timeline_box.insert("0.0", current_timeline)
        self.timeline_box.configure(state="disabled")

        
        # Update History & Visualization
        self.engine.update_history(stats)
        
        # Periodic Personality Quote (1% chance / sec)
        if random.random() < 0.01:
            quote = self.engine.get_personality_quote()
            self.add_log_to_ui(f"AI: {quote}")
            self.engine.speak(quote)
            
        for i, val in enumerate(self.engine.history["cpu"]):
            if i < len(self.cpu_history_bars):
                self.cpu_history_bars[i].set(val/100)
        
        if "energy" in self.engine.history:
            for i, val in enumerate(self.engine.history["energy"]):
                if i < len(self.energy_history_bars):
                    self.energy_history_bars[i].set(val/100)
        
        # Automated Backup Check (every hour = 3600s)
        if time.time() - self.engine.last_auto_backup > 3600:
            self.engine.last_auto_backup = time.time()
            self.engine.trigger_throttled_task(self.trigger_backup, energy_cost=15)
            self.add_log_to_ui("🕒 Automated hourly backup check.")
        
        if time.time() - self.last_csv_log > 60:
            self.last_csv_log = time.time()
            self.engine.log_performance_csv(stats)
        
        # Behavioral Anomaly Detection
        self.engine.check_behavioral_anomalies(stats)
        
        # Autonomous Personality Adaptation (every 10s)
        if int(time.time()) % 10 == 0:
            if self.engine.auto_regulate_personality():
                self.personality_label.configure(text=f"Persona: {self.engine.config['personality']} (AUTO)")
            
        if time.time() - self.last_dep_check > 30:
            self.last_dep_check = time.time()
            self.engine.trigger_throttled_task(self.update_dependency_status, energy_cost=5)
            self.refresh_analytics_chart()
        
        # Periodic UI Snapshot (every 10 minutes = 600s) for time-lapse
        if time.time() - self.last_ui_snapshot > 600:
            self.last_ui_snapshot = time.time()
            x = self.winfo_rootx()
            y = self.winfo_rooty()
            w = self.winfo_width()
            h = self.winfo_height()
            self.engine.save_ui_snapshot(x, y, w, h)
            self.add_log_to_ui("📸 Evolution snapshot captured for time-lapse.")
        
        # Architectural Anomaly Check (every 30s)
        if int(time.time()) % 30 == 0:
            anomalies = self.engine.check_architectural_anomalies()
            if anomalies:
                self.anomaly_label.configure(text="⚠️ ANOMALY DETECTED")
                if random.random() < 0.1: # 10% chance to speak warning
                    self.engine.speak(f"Architectural anomaly detected in {len(anomalies)} modules.")
                # Autonomous Logic Hardening: 20% chance to evolve if anomaly exists
                if random.random() < 0.2:
                    self.engine.trigger_throttled_task(self.engine.evolve_test_suite, energy_cost=20)
            else:
                self.anomaly_label.configure(text="")

        # Proactive Logic Hardening (every 60s)
        if int(time.time()) % 60 == 0:
            if hasattr(self.engine, "revenue"):
                if random.random() < 0.3:
                    ai_worker = getattr(self.engine, 'ai_worker', None)
                    title, val = self.engine.revenue.generate_micro_saas_product(ai_worker=ai_worker)
                    self.add_log_to_ui(f"💰 FORGED: '{title}' (Est. Value: {val} NTD)")
            
            if self.engine.energy > 30:
                self.test_label.configure(text="🛡️ HARDENING", text_color="#FFFF00")
                success, msg = self.engine.proactive_logic_hardening()
                if success:
                    self.add_log_to_ui(f"SYSTEM: {msg}")
                    self.test_label.configure(text="Integrity: OPTIMAL", text_color="#00FFAA")
                else:
                    self.test_label.configure(text="Integrity: STRETCHED", text_color="#FFAA00")

        self.after(1000, self.update_loop)

    def update_loop(self):
        """Alias / bridge for the recurring 1s telemetry update cycle."""
        try:
            self.update_telemetry()
        except Exception as e:
            print(f"[update_loop] Error: {e}")
            self.after(1000, self.update_loop)

    def update_pulse_viz(self, value, persona):
        """Updates the EKG pulse wave visualization and pushes feedback."""
        # Push visual feedback to engine (v4.8 Synesthesia)
        self.engine.broadcast_signal("metabolic_feedback", {"pulse": value})
        
        # Shift points
        y = 40 - (value * 30 + 5)
        self.pulse_points.pop(0)
        self.pulse_points.append(y)
        
        self.pulse_canvas.delete("wave")
        
        # Color based on persona
        color = "#00FFFF" # Performance
        if persona == "Safety": color = "#FFCC00"
        elif persona == "Aesthetic": color = "#9933FF"
        
        coords = []
        for i, p in enumerate(self.pulse_points):
            coords.extend([i * (self.pulse_canvas.winfo_width() / 50), p])
            
        if len(coords) >= 4:
            self.pulse_canvas.create_line(coords, fill=color, width=2, tags="wave", smooth=True)

    def trigger_logic_hardening(self):
        """Manually trigger the test suite evolution loop."""
        if self.engine.trigger_throttled_task(self.engine.evolve_test_suite, energy_cost=20):
            self.add_log_to_ui("USER: Triggering evolution logic hardening...")
        else:
            self.add_log_to_ui("ERROR: Insufficient metabolic energy (20 req).")

    def toggle_auto_regulate(self):
        """Toggle autonomous behavioral adaptation."""
        self.engine.config["auto_regulate"] = self.reg_var.get()
        self.engine.save_config(self.engine.config)
        status = "ENABLED" if self.reg_var.get() else "DISABLED"
        self.add_log_to_ui(f"SYSTEM: AI Self-Regulation {status}")
        if self.reg_var.get():
            self.personality_label.configure(text=f"Persona: {self.engine.config['personality']} (AUTO)")
        else:
            self.personality_label.configure(text=f"Persona: {self.engine.config['personality']}")

    def run_manual_tests(self):
        """Manually trigger the autonomous verification suite."""
        if self.engine.run_autonomous_tests():
            self.add_log_to_ui("USER: Triggering logic verification suite...")
            self.test_label.configure(text="🛡️ HARDENING", text_color="#FFFF00")

    def open_test_details(self):
        """Opens a detailed view of the latest logic verification results."""
        results = self.engine.get_last_test_results()
        if not results:
            self.add_log_to_ui("No test results found. Please run RE-VERIFY first.")
            return

        win = ctk.CTkToplevel(self)
        win.title("Logic Integrity Details")
        win.geometry("500x400")
        
        header = ctk.CTkLabel(win, text=f"Last Verification: {results.get('timestamp', 'N/A')}", font=ctk.CTkFont(size=14, weight="bold"))
        header.pack(pady=10)
        
        scroll = ctk.CTkScrollableFrame(win, width=450, height=300)
        scroll.pack(padx=20, pady=10, fill="both", expand=True)
        
        for t in results.get("tests", []):
            color = "#00FFAA" if t["status"] == "PASS" else "#FF5555"
            frame = ctk.CTkFrame(scroll)
            frame.pack(fill="x", pady=2, padx=5)
            
            name = ctk.CTkLabel(frame, text=t["name"], font=ctk.CTkFont(size=12))
            name.pack(side="left", padx=10)
            
            res = ctk.CTkLabel(frame, text=t["status"], text_color=color, font=ctk.CTkFont(size=12, weight="bold"))
            res.pack(side="right", padx=10)
            
            if "value" in t or "msg" in t:
                val = t.get("value", t.get("msg", ""))
                val_lbl = ctk.CTkLabel(frame, text=f"({val})", font=ctk.CTkFont(size=10), text_color="#AAAAAA")
                val_lbl.pack(side="right", padx=5)

    def open_refactor_lab(self):
        """Interactive HUD for auditing and applying predictive refactors."""
        issues = self.engine.check_code_health()
        if not issues:
            self.add_log_to_ui("Logic integrity optimal. No refactor targets identified.")
            return

        win = ctk.CTkToplevel(self)
        win.title("☢️ AI-Driven Refactor Lab (Predictive)")
        win.geometry("900x700")
        
        left_frame = ctk.CTkFrame(win, width=250)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        right_frame = ctk.CTkFrame(win)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(left_frame, text="HOTSPOT TARGETS", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        # Preview Area
        prev_orig = ctk.CTkTextbox(right_frame, height=250, font=("Consolas", 10), corner_radius=5)
        prev_orig.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(right_frame, text="PREDICTIVE PROPOSAL", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00FFAA").pack(pady=2)
        prev_suggest = ctk.CTkTextbox(right_frame, height=250, font=("Consolas", 10), corner_radius=5, border_width=1, border_color="#00FFAA")
        prev_suggest.pack(fill="x", padx=10, pady=5)

        def select_issue(issue):
            orig, suggest = self.engine.get_refactor_preview(issue)
            prev_orig.delete("0.0", "end")
            prev_orig.insert("0.0", orig)
            prev_suggest.delete("0.0", "end")
            prev_suggest.insert("0.0", suggest)
            apply_btn.configure(state="normal")
            self.selected_refactor = issue

        scroll = ctk.CTkScrollableFrame(left_frame)
        scroll.pack(fill="both", expand=True)

        for issue in issues[:8]:
            fname, func, length, m_score = issue
            btn = ctk.CTkButton(scroll, text=f"{func}\n(Heat: {m_score:.1f})", 
                              command=lambda i=issue: select_issue(i),
                              fg_color="#333333", height=50)
            btn.pack(fill="x", pady=2)

        def trigger_auto_apply():
            if hasattr(self, 'selected_refactor'):
                self.add_log_to_ui(f"AUTONOMOUS: Initiating modular split for {self.selected_refactor[1]}...")
                # Stub for next iteration: actual file write + backup
                win.destroy()

        apply_btn = ctk.CTkButton(right_frame, text="⚡ AUTO-APPLY MODULAR SPLIT", state="disabled",
                                fg_color="#FF0000", hover_color="#CC0000", command=trigger_auto_apply)
    def cycle_personality(self):
        personas = ["Default", "Performance", "Safety", "Aesthetic"]
        current = self.engine.config.get("personality", "Default")
        try:
            nxt = personas[(personas.index(current) + 1) % len(personas)]
        except ValueError:
            nxt = "Default"
        self.change_personality(nxt)
        if hasattr(self, 'personality_menu'):
            self.personality_menu.set(nxt)

    def change_personality(self, new_persona):
        self.engine.config["personality"] = new_persona
        # Some engines might not have save_config exposed directly or handle it internally
        if hasattr(self.engine, 'save_config'):
            self.engine.save_config(self.engine.config)
        if hasattr(self, 'personality_label'):
            self.personality_label.configure(text=f"Persona: {new_persona}")
        self.apply_personality_theme()

    def trigger_report(self): self.add_log_to_ui("STUB: trigger_report not fully implemented yet.")
    def trigger_docs(self): self.add_log_to_ui("STUB: trigger_docs not fully implemented yet.")
    def open_insights(self): self.add_log_to_ui("STUB: open_insights not fully implemented yet.")
    def trigger_arch(self): self.add_log_to_ui("STUB: trigger_arch not fully implemented yet.")
    def open_history_viewer(self): self.add_log_to_ui("STUB: open_history_viewer not fully implemented yet.")
    def open_time_travel(self): self.add_log_to_ui("STUB: open_time_travel not fully implemented yet.")
    def open_project_tree(self): self.add_log_to_ui("STUB: open_project_tree not fully implemented yet.")
    def open_evolution_heatmap(self): self.add_log_to_ui("STUB: open_evolution_heatmap not fully implemented yet.")
    def run_manual_tests(self):
        pass # If we overwrite this we might break something real, let's keep it clean

    def apply_personality_theme(self):
        p = self.engine.config.get("personality", "Default")
        theme = self.themes.get(p, self.themes["Default"])
        
        # Update Main Frame Colors (Simplified recursive application for Phase 1)
        self.configure(fg_color=theme["bg"])
        self.navigation_frame.configure(fg_color=theme["bg"])
        
        # Update specific labels
        if hasattr(self, 'nav_label'):
            self.nav_label.configure(text_color=theme["accent"])
        self.sync_label.configure(text_color=theme["pill"])
        
        # Adjust Metabolism
        if p == "Performance":
            self.engine.energy_decay_rate = 0.05
            self.engine.config["metabolic_interval"] = 2.0
        elif p == "Safety":
            self.engine.energy_decay_rate = 0.01
            self.engine.config["metabolic_interval"] = 8.0
        else:
            self.engine.energy_decay_rate = 0.02
            self.engine.config["metabolic_interval"] = 4.0
        
        if hasattr(self, 'log_box'):
            self.add_log_to_ui(f"HUD: Neural-Morph applied for persona '{p}'.")

    def update_heartbeat_visual(self, interval):
        p = self.engine.config.get("personality", "Default")
        if p == "Performance": base = 2.0
        elif p == "Safety": base = 8.0
        else: base = 4.0
        
        if interval < base:
            self.heartbeat_label.configure(text="💓 PULSE: ACCELERATED", text_color="#FF00FF")
        elif interval > base:
            self.heartbeat_label.configure(text="💓 PULSE: THROTTLED", text_color="#FF4400")
        else:
            self.heartbeat_label.configure(text="💓 PULSE: NOMINAL", text_color="#00FFAA")
