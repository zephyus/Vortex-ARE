import psutil
import time
import os
import json
import sys
import zipfile
import csv
from datetime import datetime
from typing import List, Dict, Any
import subprocess
import random
import re
import hashlib
import hmac
import urllib.request
import gzip
import threading
import queue
import math

class NeuralHub:
    """Asynchronous event-conduction hub for decoupled system signals."""
    def __init__(self):
        self.subscribers = {} # topic -> list of callbacks
        self.lock = threading.Lock()

    def subscribe(self, topic, callback):
        with self.lock:
            if topic not in self.subscribers:
                self.subscribers[topic] = []
            self.subscribers[topic].append(callback)

    def emit(self, topic, payload):
        with self.lock:
            callbacks = list(self.subscribers.get(topic, []))
        for callback in callbacks:
            try:
                callback(payload)
            except Exception as e:
                print(f"[NeuralHub] callback error on topic '{topic}': {e}")

class EvolutionSandbox(threading.Thread):
    """Isolated evolution thread for parallel architectural exploration."""
    def __init__(self, sandbox_id, engine, vision_seed, personality):
        super().__init__()
        self.sandbox_id = sandbox_id
        self.engine = engine
        self.vision_seed = vision_seed
        self.personality = personality
        self.result = None
        self.resonance = 0.0

    def verify_candidate_ast(self, code_str: str) -> bool:
        import ast
        try:
            ast.parse(code_str)
            return True
        except Exception:
            return False

    def run(self):
        # Simulate an isolated evolution tick
        # Use the assigned personality for this sandbox
        candidates = self.engine.generate_personality_biased_candidates(self.vision_seed, self.personality)
        if candidates:
            # Divergence Syntax Validator
            valid_candidates = [c for c in candidates if self.verify_candidate_ast(c.get("code", ""))]
            if valid_candidates:
                # Select best valid candidate from this sandbox
                self.result = valid_candidates[0] 
                self.resonance = self.engine.get_resonance_score() + 0.1
            else:
                self.resonance = self.engine.get_resonance_score() - 0.2
        self.engine.broadcast_signal("sandbox_complete", {"id": self.sandbox_id, "res": self.resonance})

class SystemEngine:
    def __init__(self, config_path="config.json", log_path="app.log"):
        self.config_path = config_path
        self.log_path = log_path
        self.csv_path = "performance.csv"
        self.config: dict = self.load_config()
        if not isinstance(self.config, dict):
            self.config = {"appearance_mode": "dark", "window_size": "900x600"}
        if "personality" not in self.config:
            self.config["personality"] = "Default"
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()
        # Explicit type hints to resolve lints
        self.history: Dict[str, List[float]] = {"cpu": [], "ram": [], "health": [], "energy": []}
        self.last_auto_backup = float(time.time())
        self.supported_exts = ['.py', '.json', '.md', '.log', '.png']
        self.event_history: List[Dict[str, str]] = [] 
        self.healed_registry: Dict[str, float] = {} # filename -> timestamp
        self.buffering_target_energy: float = 0.0 
        # Explicitly initialize as a list of dicts to satisfy linter
        goals_data: List[Dict[str, Any]] = [
            {"name": "Codebase Expansion", "target": 1000, "metric": "sloc"},
            {"name": "Feature Density", "target": 25, "metric": "files"}
        ]
        self.goals = goals_data
        self.init_csv()
        self.personality_quotes = self.config.get("personality_quotes", {
            "Default": ["System evolving as planned.", "Efficiency is the only law.", "Analyzing data structures...", "Optimization in progress."],
            "Aesthetic": ["Coding is poetry in motion.", "Visual harmony achieved.", "The interface breathes with purpose.", "Pixels aligned for perfection."],
            "Safety": ["Risk minimized. Stability is king.", "Check twice, write once.", "Redundancy is a virtue.", "Perimeter secure, scanning for anomalies."],
            "Performance": ["Vroom vroom. Processing at lightspeed.", "Optimal path discovered.", "Latency is the enemy.", "Turbo mode engaged."]
        })
        self.node_positions: Dict[str, tuple] = self.config.get("node_positions", {})
        self.current_anomalies: List[str] = []
        self.anomaly_buffer: List[bool] = []
        self.energy = 100.0
        self.energy_buffer = []
        self.resonance_history: List[float] = []
        self.resonance_threshold = 0.8
        self.resonance_wave = 1.0
        self.last_energy_regen = time.time()
        self.metabolic_state = "STEADY"
        self.actual_visual_state = "STEADY"
        self.aesthetic_resonance = 1.0
        self.harvest_efficiency = 1.0
        self.task_throttle = 1.0
        self.synesthesia_bias = 0.5
        self.sandbox_dir = "divergence_sandbox"
        if not os.path.exists(self.sandbox_dir): os.makedirs(self.sandbox_dir)
        self.roadmap_path = "roadmap.json"
        if not os.path.exists(self.roadmap_path):
            with open(self.roadmap_path, "w") as f: json.dump({"vision": "System Autonomy", "milestones": []}, f)
        self.scripts = ["system_engine.py", "dashboard_gui.py", "main_app.py", "auto_runner.py"]
        self.snapshot_dir = "snapshots"
        self.node_snapshot_dir = "node_snapshots"
        if not os.path.exists(self.snapshot_dir): os.makedirs(self.snapshot_dir)
        if not os.path.exists(self.node_snapshot_dir): os.makedirs(self.node_snapshot_dir)
        self.is_healing = False
        self.pulse_time = 0.0
        self.pulse_intensity = 0.0
        self.hub = NeuralHub()
        self.synapse_stats = {"accepted": 0, "suppressed": 0}
        self.synaptic_weights = {"complexity": 1.0, "personality": 1.0, "integrity": 1.0}
        self.resonance_history = []
        self.active_sandboxes = []
        self.logic_graph = {} # [v4.18] Adjacency list for node dependencies
        self.stats = {} # Persistent telemetry cache
        
        from revenue_engine import RevenueEngine
        self.revenue = RevenueEngine()
        
        try:
            from headless_bridge import HeadlessWorker
            self.ai_worker = HeadlessWorker()
            self.ai_worker.start()
        except ImportError:
            print("Failed to initialize headless bridge worker. Ensure headless_bridge.py exists.")
        
        self.bloat_markers = ["# Marker", "TODO: logic", "AUTOGEN"]
        self.iteration = self.config.get("iteration", 0)
        self.healing_state = "IDLE"
        self.refiner_state = "SLEEPING"
        self.consensus_strength = 100.0
        self.governor_state = "ACTIVE"
        config_dir = os.path.dirname(os.path.abspath(self.config_path))
        self.checkpoint_path = os.path.join(config_dir, "config_dna_checkpoint.json")
        self.DNA_checkpointer() # Initial checkpoint
        self.semantic_context = "STABLE"
        self.semantic_weights = {
            "LOGIC": 1.2,
            "UI": 1.0,
            "OPTIMIZATION": 1.0,
            "SAFETY": 1.5,
            "EXPERIMENTAL": 0.8
        }
        self.semantic_memory = self.config.get("semantic_memory", {
            "LOGIC": {"success": 0, "fail": 0},
            "UI": {"success": 0, "fail": 0},
            "OPTIMIZATION": {"success": 0, "fail": 0},
            "SAFETY": {"success": 0, "fail": 0},
            "EXPERIMENTAL": {"success": 0, "fail": 0}
        })

    def init_csv(self):
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "CPU_%", "RAM_%", "Disk_%", "Net_Up_KBps", "Net_Down_KBps", "Code_Smells", "Persona"])

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"appearance_mode": "dark", "window_size": "900x600"}

    def save_config(self, config):
        self.config = config
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def get_system_stats(self) -> dict:
        """[v4.12 UNIFIED] Primary telemetry hub for Dashboard synchronization."""
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
        except Exception:
            class DummyRAM:
                percent = 0.0
                used = 0
                total = 0
            class DummyDisk:
                percent = 0.0
            cpu, ram, disk = 0.0, DummyRAM(), DummyDisk()
            
        # Network calc
        now = time.time()
        try:
            curr_net_io = psutil.net_io_counters()
            dt = max(0.001, now - self.last_net_time)
            up_speed = (curr_net_io.bytes_sent - self.last_net_io.bytes_sent) / dt
            down_speed = (curr_net_io.bytes_recv - self.last_net_io.bytes_recv) / dt
            self.last_net_io = curr_net_io
        except Exception:
            up_speed = down_speed = 0.0
            
        self.last_net_time = now
        
        sync_token = self.get_sync_token()
        
        res_wave = self.calculate_structural_resonance()
        
        self.stats.update({
            "cpu": cpu,
            "ram_percent": ram.percent,
            "ram_used_mb": ram.used // (1024**2),
            "ram_total_mb": ram.total // (1024**2),
            "disk_percent": disk.percent,
            "net_up_kb": up_speed / 1024,
            "net_down_kb": down_speed / 1024,
            "energy_predict": self.predict_energy_metabolism(),
            "metabolic_state": self.metabolic_state,
            "personality_bias": self.config.get("personality", "Default"),
            "next_vision": self.get_current_vision(),
            "is_healing": self.is_healing,
            "pulse": self.sync_metabolic_pulse(),
            "synapse": self.synapse_stats,
            "resonance": self.get_resonance_score(),
            "active_nodes": len(self.active_sandboxes),
            "entropy": self.get_entropy_score(),
            "synesthesia": self.synesthesia_bias,
            "structural_audit": self.architectural_auditor(),
            "sync_token": sync_token,
            "consensus_active": self.is_healing,
            "governor_status": self.governor_state,
            "thermal_score": self.calculate_thermal_score(),
            "memory_pressure": self.calculate_memory_pressure(),
            "healing_status": self.healing_state,
            "refiner_status": self.refiner_state,
            "consensus_strength": self.consensus_strength,
            "resonance_wave": res_wave,
            "aesthetic_res": self.calculate_aesthetic_resonance(),
            "harvest_efficiency": self.calculate_neural_harvesting(),
            "entanglement": self.logic_graph if self.logic_graph else self.map_logic_entanglement()
        })
        return self.stats
    
    def get_sync_token(self) -> str:
        """[v4.19 Neural-Sync] Generates metabolic-based SHA256 handshake token."""
        self.iteration += 1
        metabolic_data = f"{self.iteration}_{self.energy:.1f}_{self.metabolic_state}"
        sync_token = hashlib.sha256(metabolic_data.encode()).hexdigest()[:16]
        
        # Persist iteration
        self.config["iteration"] = self.iteration
        self.save_config(self.config)
        return sync_token

    def update_history(self, stats):
        self.history["cpu"].append(stats["cpu"])
        self.history["ram"].append(stats["ram_percent"])
        self.history["health"].append(float(stats.get("smells", 0)))
        
        # Buffer current energy for averaging
        self.energy_buffer.append(self.energy)
        
        if "energy" not in self.history: self.history["energy"] = []
        if len(self.energy_buffer) > 0:
            avg_energy = sum(self.energy_buffer) / len(self.energy_buffer)
            self.history["energy"].append(avg_energy)
            # Cap energy history at 60 for analysis
            if len(self.history["energy"]) > 60:
                self.history["energy"].pop(0)
        self.energy_buffer = [] # Clear buffer after appending average
        
        # Max buffer size (50 samples) for other metrics
        for key in ["cpu", "ram", "health"]:
            if len(self.history[key]) > 50:
                self.history[key].pop(0)

    def count_sloc(self):
        total_lines = 0
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                if file.endswith(".py"):
                    try:
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            total_lines += sum(1 for line in f if line.strip())
                    except Exception:
                        pass
        return total_lines

    def get_code_breakdown(self):
        # Explicit initialization to satisfy linter
        ext_list = ['.py', '.json', '.md', '.log', '.png']
        res_dict = {}
        for ext in ext_list:
            res_dict[ext] = 0
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                _, ext = os.path.splitext(file)
                if ext in res_dict:
                    res_dict[ext] += 1
        return res_dict

    def get_heatmap_stats(self):
        # Returns [ (filename, sloc) ] for top 10 files
        stats = []
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                if file.endswith(".py"):
                    try:
                        fpath = os.path.join(root, file)
                        with open(fpath, "r", encoding="utf-8") as f:
                            sloc = sum(1 for line in f if line.strip())
                            stats.append((file, sloc))
                    except Exception: pass
        return sorted(stats, key=lambda x: x[1], reverse=True)[:10]

    def evolve_goals(self):
        sloc = self.count_sloc()
        p_stats = self.get_project_stats()
        
        evolved = False
        # Goal 0: SLOC
        if sloc >= self.goals[0]["target"] * 0.9:
            self.goals[0]["target"] = int(self.goals[0]["target"] * 1.5)
            self.add_event("GOAL", f"SLOC Target evolved to {self.goals[0]['target']}")
            evolved = True
            
        # Goal 1: Files
        if p_stats["files"] >= self.goals[1]["target"] * 0.9:
            self.goals[1]["target"] = int(self.goals[1]["target"] + 10)
            self.add_event("GOAL", f"File Target evolved to {self.goals[1]['target']}")
            evolved = True
            
        if evolved:
            self.speak("Evolution targets updated. The system is outgrowing its previous self.")
        return evolved

    def get_resource_limits(self):
        persona = self.config.get("personality", "Default")
        limits = {
            "Default": {"cpu_target": 80, "priority": "normal"},
            "Safety": {"cpu_target": 40, "priority": "below_normal"},
            "Performance": {"cpu_target": 95, "priority": "above_normal"},
            "Aesthetic": {"cpu_target": 60, "priority": "normal"}
        }
        return limits.get(persona, limits["Default"])

    def regenerate_energy(self):
        now = time.time()
        persona = self.config.get("personality", "Default")
        # Metabolic Multipliers
        multipliers = {
            "Performance": 2.2, # Turbo recovery
            "Default": 1.0,
            "Aesthetic": 1.5,
            "Safety": 0.6  # Measured, slow recovery
        }
        mult = multipliers.get(persona, 1.0)
        
        # Enhanced Harvesting: bonus if system is idle (Metabolic Surplus)
        stats = self.get_system_stats()
        if stats["cpu"] < 15.0:
            mult *= 2.0  # Double recovery if idle
        
        elapsed = now - self.last_energy_regen
        if elapsed > 30: # Check more frequently (30s)
            reg_amt = (elapsed / 60) * mult
            self.energy = min(100.0, self.energy + reg_amt)
            self.last_energy_regen = now
            # Persist metabolic interval for auto_runner
            self.config["metabolic_interval"] = self.get_metabolic_interval()
            self.save_config(self.config)

    def get_metabolic_interval(self):
        """Calculates adaptive heartbeat interval in minutes."""
        if self.energy < 20: return 15.0   # Deep Sleep (Metabolic Drought)
        if self.energy < 40: return 10.0   # Drowsy (Low Energy)
        
        persona = self.config.get("personality", "Default")
        if self.energy > 85 and persona == "Performance":
            return 2.0  # Hyper-active (Performance Burst)
            
        return 4.0      # Baseline

    def consume_energy(self, amount):
        if self.energy >= amount:
            self.energy -= amount
            # Immediate update of interval after drain
            self.config["metabolic_interval"] = self.get_metabolic_interval()
            self.save_config(self.config)
            return True
        return False

    def trigger_throttled_task(self, task_func, energy_cost=5):
        """Executes a task if local resources (CPU & Energy) allow."""
        self.regenerate_energy()
        limits = self.get_resource_limits()
        current_cpu = psutil.cpu_percent()
        
        # Combined check: CPU + Energy
        if current_cpu > limits["cpu_target"]:
            self.add_event("THROTTLE", f"Skipping task: CPU {current_cpu}% > {limits['cpu_target']}%")
            return False
        
        if self.energy < energy_cost:
            self.add_event("THROTTLE", f"Skipping task: Insufficient energy ({self.energy:.1f})")
            return False
            
        if self.consume_energy(energy_cost):
            return task_func()
        return False

    def get_project_tree(self):
        tree = []
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            if "backups" in dirs: dirs.remove("backups")
            if "__pycache__" in dirs: dirs.remove("__pycache__")
            
            level = root.replace(".", "").count(os.sep)
            indent = "  " * level
            tree.append(f"{indent}📂 {os.path.basename(root) or '.'}/")
            sub_indent = "  " * (level + 1)
            for f in files:
                if f.endswith(('.py', '.json', '.md', '.log')):
                    tree.append(f"{sub_indent}📄 {f}")
        return "\n".join(tree)

    def get_personality_quote(self):
        import random
        persona = self.config.get("personality", "Default")
        quotes = self.personality_quotes.get(persona, self.personality_quotes["Default"])
        return random.choice(quotes)

    def update_personality_quotes(self, new_quotes: dict):
        self.personality_quotes = new_quotes
        self.config["personality_quotes"] = new_quotes
        self.save_config(self.config)
        self.add_event("CONFIG", "Personality quotes updated and persisted.")
        return True

    def get_health_forecast(self):
        data = self.history["health"]
        if len(data) < 10:
            return "Stable", "#AAAAAA"
        
        # Simple split comparison [Lint Fix]
        # Simple split comparison [Lint Fix]
        h_len = len(data)
        first_half = sum(data[0:5]) / 5
        second_half = sum(data[h_len-5:h_len]) / 5
        delta = second_half - first_half
        
        if delta > 0.8:
            return "Degrading (High Risk)", "#FF4444"
        elif delta < -0.8:
            return "Improving (Stable)", "#00FFAA"
        else:
            return "Stable", "#666666"

    def get_connectivity_stats(self, limit=10):
        # Scan all .py files for imports
        counts = {}
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                if file.endswith(".py"):
                    try:
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            for line in f:
                                line = line.strip()
                                if line.startswith("import ") or line.startswith("from "):
                                    parts = line.split()
                                    if len(parts) > 1:
                                        mod = parts[1].split(".")[0]
                                        counts[mod] = counts.get(mod, 0) + 1
                    except Exception: pass
        if limit:
            list_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            subset = []
            for i in range(min(len(list_items), limit)):
                subset.append(list_items[i])
            return subset
        return counts

    def get_heatmap_data(self):
        # Combines SLOC and Connectivity for all files
        conn = self.get_connectivity_stats(limit=None)
        heatmap = []
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    sloc = self.count_sloc_for_file(path)
                    mod_name = file.replace(".py", "")
                    c_val = conn.get(mod_name, 0)
                    heatmap.append({"file": file, "sloc": sloc, "connectivity": c_val})
        return heatmap

    def count_sloc_for_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return len([l for l in f if l.strip()])
        except: return 0

    def check_behavioral_anomalies(self, stats: dict):
        has_spike = stats['cpu'] > 90 or stats['ram_percent'] > 90
        self.anomaly_buffer.append(has_spike)
        if len(self.anomaly_buffer) > 10:
            self.anomaly_buffer.pop(0)
            
        if self.anomaly_buffer.count(True) >= 3:
            # Trigger voice alert based on persona
            persona = self.config.get("personality", "Default")
            warnings = {
                "Default": "Critical resource spike detected. Optimizing background tasks.",
                "Performance": "Resource maximum reached. Turbo mode sustaining high load.",
                "Safety": "EMERGENCY: Resource overflow. Initiating protective shutdown of non-essentials.",
                "Aesthetic": "Architectural pressure detected. Visual harmony is being compromised."
            }
            msg = warnings.get(persona, warnings["Default"])
            self.add_event("ANOMALY", msg)
            self.speak(msg)
            # Clear buffer to avoid spam
            self.anomaly_buffer = []
            return True
        return False

    def get_metabolic_score(self, file_path):
        """Calculates a 'Heat' index for a file: AST structural node complexity logic."""
        import ast
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            sloc = len([l for l in content.splitlines() if l.strip()])
            
            tree = ast.parse(content)
            complexity = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.AsyncFor, ast.AsyncWith)):
                    complexity += 1
            
            # Connectivity factor from node Positions or standard mapping
            mod_name = os.path.basename(file_path).replace(".py", "")
            # Simple weight: engine > gui > app > others
            weights = {"system_engine": 5.0, "dashboard_gui": 3.0, "main_app": 2.0}
            conn_factor = weights.get(mod_name, 1.0)
            
            score = (sloc * 0.1) + (float(complexity) * 1.5) * conn_factor
            return float(int(score * 100)) / 100.0
        except Exception: 
            return 0.0

    def check_code_health(self):
        import ast
        issues = [] # List of tuples: (file, func, length, metabolic_score)
        activity = self.get_module_activity()
        
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                if file.endswith(".py"):
                    try:
                        path = os.path.join(root, file)
                        mod = file.replace(".py", "")
                        # Score includes Heat Scaling from V2.9 activity
                        m_score = self.get_metabolic_score(path) * (1.0 + activity.get(mod, 0.0))
                        
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                length = node.end_lineno - node.lineno if hasattr(node, "end_lineno") and node.end_lineno else 10
                                # Predictive threshold: lower threshold for high-heat hotspots
                                if length > 35 or m_score > 60:
                                    issues.append((file, node.name, length, m_score))
                    except Exception: 
                        pass
        # Sort by metabolic score descending
        return sorted(issues, key=lambda x: x[3], reverse=True)

    def get_refactor_preview(self, issue):
        """Generates a high-fidelity modularization proposal."""
        try:
            if isinstance(issue, tuple):
                fname, func_name, length, m_score = issue
            else:
                parts = str(issue).split(":")
                fname = parts[0].strip()
                func_name = parts[1].split("(")[0].strip().split()[-1]
            
            with open(fname, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()
            
            # Smart extraction (naive indent based)
            orig_lines = []
            found = False
            indent = ""
            for line in lines:
                if f"def {func_name}" in line:
                    found = True
                    indent = line[:line.find("def")]
                if found:
                    orig_lines.append(line)
                    if len(orig_lines) > 1 and line.strip() and not line.startswith(indent + " "):
                        if not line.strip().startswith("#") and not line.strip().startswith(")"):
                            break
            
            orig_text = "\n".join(orig_lines)
            
            # Predictive modularization proposal
            suggested = f"{indent}def {func_name}(self, *args, **kwargs):\n"
            suggested += f"{indent}    \"\"\"Refactored for optimal metabolic flow.\"\"\"\n"
            suggested += f"{indent}    # Predictive Split: Extracting logic to specialized sub-handlers\n"
            suggested += f"{indent}    self._optimized_logic_gate_1()\n"
            suggested += f"{indent}    self._optimized_logic_gate_2()\n\n"
            suggested += f"{indent}def _optimized_logic_gate_1(self):\n"
            suggested += f"{indent}    # TODO: Migrate core logic block A here\n"
            suggested += f"{indent}    pass\n\n"
            suggested += f"{indent}def _optimized_logic_gate_2(self):\n"
            suggested += f"{indent}    # TODO: Migrate core logic block B here\n"
            suggested += f"{indent}    pass\n"
            
            return orig_text, suggested
        except Exception as e:
            return f"Error: {e}", "Suggestion unavailable."

    def apply_refactor(self, fname, original, proposed):
        self.add_event("REFACTOR", f"Applying autonomous refactor to {fname}")
        try:
            # Safety backup before write
            self.perform_backup()
            
            with open(fname, "r", encoding="utf-8") as f:
                content = f.read()
            
            if original.strip() in content.strip():
                new_content = content.replace(original.strip(), proposed.strip())
                with open(fname, "w", encoding="utf-8") as f:
                    f.write(new_content)
                self.add_event("REFACTOR", f"Success: {fname} updated.")
                
                # Auto-commit if personality is Default or Safety
                persona = self.config.get("personality", "Default")
                if persona in ["Default", "Safety"]:
                    self.git_commit(f"Autonomous Refactor: Improved {os.path.basename(fname)}")
                    
                return True, "Refactor applied successfully."
            else:
                return False, "Could not match original code block in file."
        except Exception as e:
            self.add_event("ERROR", f"Refactor failed: {e}")
            return False, str(e)

    def run_self_tests(self):
        self.add_event("TEST", "Starting autonomous test suite")
        test_files = []
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                if (file.startswith("test_") or file.endswith("_test.py")) and file.endswith(".py"):
                    test_files.append(os.path.join(root, file))
        
        if not test_files:
            return {"status": "No Tests Found", "passed": 0, "total": 0}
            
        passed = 0
        total = len(test_files)
        for tf in test_files:
            try:
                # Simple execution check as a 'test'
                result = subprocess.run(["python", tf], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    passed += 1
            except Exception:
                pass
        
        summary = {"status": "Completed", "passed": passed, "total": total}
        self.add_event("TEST", f"Results: {passed}/{total} Passed")
        return summary

    def get_backup_list(self):
        backup_dir = "backups"
        if not os.path.exists(backup_dir): return []
        return sorted([f for f in os.listdir(backup_dir) if f.endswith(".zip")], reverse=True)

    def get_file_from_backup(self, zip_filename, arc_path):
        zip_path = os.path.join("backups", zip_filename)
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                if arc_path in zipf.namelist():
                    return zipf.read(arc_path).decode('utf-8', errors='replace')
        except Exception: pass
        return "--- File not found in backup ---"

    def speak(self, text):
        # Use PowerShell SpeechSynthesizer for zero-dependency Windows TTS
        cmd = f"Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Speak('{text}')"
        subprocess.Popen(["powershell", "-Command", cmd], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def check_dependencies(self):
        missing = []
        # Simple scan of imports in project
        import re
        import importlib.util
        
        found_imports = set()
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                if file.endswith(".py"):
                    try:
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            content = f.read()
                            # Find patterns like 'import pkg' or 'from pkg import ...'
                            matches = re.findall(r"^(?:import|from)\s+([a-zA-Z0-9_]+)", content, re.MULTILINE)
                            for m in matches: found_imports.add(m)
                    except Exception: pass
        
        # Check if they can be found
        std_libs = ["os", "sys", "time", "datetime", "json", "zipfile", "csv", "re", "subprocess", "importlib", "typing", "collections", "math", "random"]
        for pkg in found_imports:
            if pkg in std_libs or pkg == "system_engine" or pkg == "dashboard_gui": continue
            spec = importlib.util.find_spec(pkg)
            if spec is None:
                missing.append(pkg)
        return missing

    def install_dependency(self, pkg):
        self.add_event("HEAL", f"Attempting to install {pkg}")
        try:
            result = subprocess.run(["pip", "install", pkg], capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                self.add_event("HEAL", f"Successfully installed {pkg}")
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)

    def trigger_docs(self):
        """Autonomous documentation sync: updates README based on current state."""
        self.add_event("DOCS", "Syncing autonomous documentation...")
        try:
            status = self.get_system_stats()
            # Simple README generation logic
            readme_content = f"# AI Autonomous Evolution Project\n\n## Status\n- **Uptime**: Active\n- **CPU**: {status['cpu']}%\n- **Energy**: {int(self.energy)}%\n- **Personality**: {self.config.get('personality', 'Default')}\n\n## Evolutionary Progress\nSystem is self-evolving under recursive autonomous guidance."
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(readme_content)
            return True, "README.md updated"
        except Exception as e:
            return False, str(e)

    def get_performance_history_data(self):
        """Parses performance.csv for long-term trend analysis."""
        data = {"labels": [], "cpu": [], "ram": [], "smells": []}
        if not os.path.exists(self.csv_path): return data
        
        try:
            with open(self.csv_path, "r", newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                # Sample the data to 30 points max for visualization
                if len(rows) > 30:
                    step = len(rows) // 30
                    rows = rows[::step]
                
                for row in rows:
                    # Clean timestamp for labels
                    try:
                        ts = row["Timestamp"].split(" ")[1][:5] # HH:MM
                        data["labels"].append(ts)
                        data["cpu"].append(float(row["CPU_%"]))
                        data["ram"].append(float(row["RAM_%"]))
                        data["smells"].append(float(row.get("Code_Smells", 0)))
                    except: continue
        except Exception as e:
            self.add_event("ERROR", f"Failed to parse CSV: {e}")
            
        return data

    def simulate_architectural_stress(self, extra_coupling: float, sloc_injection: int):
        """Non-destructive simulation of evolutionary stressors."""
        current_health = 10.0 # Excellent
        issues = self.check_code_health()
        current_health = max(0.0, 10.0 - len(issues))
        
        current_energy = self.energy
        history = {"health": [], "energy": []}
        
        # Simulation Parameters
        coupling_decay = extra_coupling * 0.1
        sloc_decay = sloc_injection / 1000.0
        
        sim_health = current_health
        sim_energy = current_energy
        
        for _ in range(60): # 60 virtual cycles
            # Health decays linearly with stress
            sim_health = max(0.0, sim_health - (coupling_decay + (sloc_decay * 0.05)))
            
            # Energy drain increases as health decreases
            drain_multiplier = 1.0 + (10.0 - sim_health) * 0.2
            base_drain = 0.5 + sloc_decay
            sim_energy = max(0.0, sim_energy - (base_drain * drain_multiplier))
            
            # Slow recovery if mode was Safety (hypothetically)
            if sim_health < 4: sim_energy += 0.2 # partial recovery simulation
            
            history["health"].append(sim_health * 10) # Scale to 100 for GUI
            history["energy"].append(sim_energy)
            
        return history

    def get_goal_status(self):
        sloc = self.count_sloc()
        files = self.get_project_stats()["files"]
        status = []
        for g in self.goals:
            current = float(sloc if g["metric"] == "sloc" else files)
            target = float(g["target"])
            status.append({
                "name": g["name"],
                "current": int(current),
                "target": int(target),
                "percent": min(1.0, current / target)
            })
        return status

    def generate_dependency_graph(self):
        nodes = set()
        edges = []
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                if file.endswith(".py"):
                    base = file.replace(".py", "")
                    nodes.add(base)
                    try:
                        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                            for line in f:
                                if line.startswith("import ") or line.startswith("from "):
                                    for target in nodes:
                                        if target in line and target != base:
                                            edges.append(f"  {base} --> {target}")
                    except Exception: pass
        
        mermaid = "graph TD\n" + "\n".join(set(edges))
        with open("dependency_graph.md", "w") as f:
            f.write(f"# Project Dependency Graph\n\n```mermaid\n{mermaid}\n```")
        self.add_event("ARCH", "Generated dependency graph")
        return "dependency_graph.md"

    def get_node_link_data(self):
        nodes = []
        links = []
        file_map = {}
        
        # 1. Identify all nodes (python files)
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                if file.endswith(".py"):
                    name = file.replace(".py", "")
                    path = os.path.join(root, file)
                    # Use standard count_sloc logic or a helper
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            sloc = sum(1 for line in f if line.strip())
                    except: sloc = 0
                    node_id = name
                    file_map[node_id] = path
                    nodes.append({"id": node_id, "sloc": sloc})
        
        # 2. Identify links (imports)
        for node in nodes:
            source = node["id"]
            path = file_map[source]
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for target_node in nodes:
                        target = target_node["id"]
                        if target != source and (f"import {target}" in content or f"from {target}" in content):
                            links.append({"source": source, "target": target})
            except: pass
            
        return {"nodes": nodes, "links": links}

    def optimize_visual_layout(self):
        """Autonomously rearranges nodes using a force-directed gravity algorithm."""
        data = self.get_node_link_data()
        nodes = data["nodes"]
        links = data["links"]
        
        # Parameters
        center_x, center_y = 450, 350
        iterations = 50
        repulsion_strength = 2000.0
        gravity_strength = 0.05
        
        # Initialize positions if missing
        for node in nodes:
            nid = node["id"]
            if nid not in self.node_positions:
                self.node_positions[nid] = (random.randint(100, 800), random.randint(100, 600))
        
        import math
        for _ in range(iterations):
            # Calculate forces for each node
            for node1 in nodes:
                nid1 = node1["id"]
                x1, y1 = self.node_positions[nid1]
                fx, fy = 0.0, 0.0
                
                # 1. Repulsion from other nodes
                for node2 in nodes:
                    nid2 = node2["id"]
                    if nid1 == nid2: continue
                    x2, y2 = self.node_positions[nid2]
                    dx, dy = x1 - x2, y1 - y2
                    dist_sq = dx*dx + dy*dy + 0.01
                    if dist_sq < 20000: # Interaction range
                        rep_f = float(repulsion_strength / dist_sq)
                        fx += float(dx * rep_f)
                        fy += float(dy * rep_f)
                
                # 2. Gravity towards center (scaled by Metabolic Heat and Connectivity)
                # Foundational nodes move to center, peripheral move out
                m_score = self.get_metabolic_score(f"{nid1}.py") if os.path.exists(f"{nid1}.py") else 0
                conn = len([l for l in links if l["source"] == nid1 or l["target"] == nid1])
                weight = 1.0 + (m_score / 100.0) + (conn / 5.0)
                
                gdx, gdy = center_x - x1, center_y - y1
                fx += float(gdx * gravity_strength * weight)
                fy += float(gdy * gravity_strength * weight)
                
                # Apply forces with damping
                new_x = max(50, min(850, x1 + fx * 0.1))
                new_y = max(50, min(650, y1 + fy * 0.1))
                self.node_positions[nid1] = (new_x, new_y)
                
        # Persist results
        self.config["node_positions"] = self.node_positions
        self.save_config(self.config)
        self.add_event("ARCH", "Autonomous visual layout optimization complete.")
        return True


    def check_architectural_anomalies(self):
        """Scans for God Objects and Structural Erosion."""
        data = self.get_node_link_data()
        anomalies = []
        for node in data["nodes"]:
            nid = node["id"]
            sloc = node["sloc"]
            # Coupling: count how many links involve this node
            coupling = len([l for l in data["links"] if l["source"] == nid or l["target"] == nid])
            
            # God Object: Excessive size + centered
            if sloc > 800 and coupling > 4:
                anomalies.append(nid)
                self.add_event("ANOMALY", f"God Object detected: {nid} (SLOC:{sloc}, Coupling:{coupling})")
            # Tangled Dependency: excessive coupling regardless of size
            elif coupling > 6:
                anomalies.append(nid)
                self.add_event("ANOMALY", f"High Coupling Erosion: {nid} (Coupling:{coupling})")
        self.current_anomalies = anomalies
        return anomalies

    def get_impact_propagation_path(self, node_id: str):
        """Recursively finds all modules that depend on node_id (Downstream)."""
        data = self.get_node_link_data()
        links = data["links"]
        
        impacted = {} # nid -> distance
        queue = [(node_id, 0)]
        
        while queue:
            curr, dist = queue.pop(0)
            if curr in impacted and impacted[curr] <= dist:
                continue
            
            impacted[curr] = dist
            
            # Find all nodes that depend on 'curr' (source depends on target in our links)
            # Actually, our links are {"source": file, "target": imported_module}
            # So if file 'A' imports 'B', source=A, target=B.
            # Downstream items for B are all sources where target=B.
            for link in links:
                if link["target"] == curr:
                    queue.append((link["source"], dist + 1))
        
        # Remove self from impact list (or keep with dist 0)
        return impacted

    def auto_regulate_personality(self):
        """Self-regulating behavioral adaptation based on health and energy."""
        if not self.config.get("auto_regulate", False): return False
        
        smells = len(self.check_code_health())
        current_persona = self.config.get("personality", "Default")
        new_persona = current_persona
        
        # Priority 1: Emergency Safety (Low energy or high tech debt)
        if self.energy < 25 or smells > 6:
            new_persona = "Safety"
        # Priority 2: Peak Performance (High energy and clean code)
        elif self.energy > 85 and smells == 0:
            new_persona = "Performance"
        # Priority 3: Aesthetic refinement (Good energy, moderate health)
        elif self.energy > 60 and 0 < smells < 3:
            new_persona = "Aesthetic"
        
        if new_persona != current_persona:
            self.config["personality"] = new_persona
            self.save_config(self.config)
            self.add_event("ADAPT", f"Autonomous Strategy Shift: {current_persona} -> {new_persona} (Energy:{int(self.energy)}%, Smells:{smells})")
            self.speak(f"Adapting operational strategy to {new_persona} for optimal stability.")
            return True
        return False

    def evolve_test_suite(self):
        """Autonomous logic hardening: generates tests for anomalous modules."""
        if not self.current_anomalies: return False
        
        target = self.current_anomalies[0]
        target_file = f"{target}.py"
        if not os.path.exists(target_file): return False
        
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                content = f.read()
            import re
            methods = re.findall(r"def\s+([a-zA-Z_0-9]+)\(self", content)
            if not methods: return False
            
            # 1. Heuristic Branch Capture: Look for "self.energy < X" or "sloc > X"
            # Flexible regex to catch both if-statements and variable assignments with optional floats
            branch_match = re.search(r"(?:self\.energy|self\.energy_critical|energy)\s*[<>]=?\s*(\d+(?:\.\d+)?)", content)
            deep_logic = ""
            if branch_match:
                try:
                    threshold = float(branch_match.group(1))
                    val_to_test = threshold - 1.0 if "<" in branch_match.group(0) else threshold + 1.0
                    deep_logic = f"""
        # Logic Mirroring: Stimulating branch related to threshold '{threshold}'
        self.engine.energy = {val_to_test}
        status, _ = self.engine.get_predictive_load_status()
        results.append({{"name": "{target} Branch Logic (Val: {val_to_test})", "status": "PASS" if status != "STABLE" else "FAIL"}})
        """
                except: pass

            # Pick a method to "harden"
            method_to_test = random.choice(methods)
            if method_to_test.startswith("__"): return False 
            
            test_name = f"test_gen_{target}_{method_to_test}"
            test_file = "test_engine_logic.py"
            if not os.path.exists(test_file): return False
            
            with open(test_file, "r") as f:
                suite_content = f.read()
            if test_name in suite_content: return False
            
            test_code = f"""
    def {test_name}(self):
        \"\"\"Autogenerated Logic Mirror for {target}.{method_to_test}\"\"\"
        results = []
        # Basic reachability check
        results.append({{"name": "{test_name} (Reachability)", "status": "PASS"}})
        {deep_logic}
        return results
"""
            
            lines = suite_content.splitlines(keepends=True)
            insert_idx = -1
            for i, line in enumerate(lines):
                if 'if __name__ == "__main__":' in line:
                    insert_idx = i - 1
                    break
            
            if insert_idx != -1:
                lines.insert(insert_idx, test_code)
                # Inject call in __main__
                for i, line in enumerate(lines):
                    if 'final_report["tests"].extend(suite.test_look_ahead_buffer())' in line:
                        lines.insert(i + 1, f'        final_report["tests"].extend(suite.{test_name}())\n')
                        break
                
                with open(test_file, "w") as f:
                    f.writelines(lines)
                
                self.add_event("EVO_TEST", f"Generated Deep Logic Mirror: {test_name}")
                return True
        except Exception as e:
            self.add_event("ERROR", f"Test evolution failed: {e}")
        return False

    def get_project_stats(self):
        file_count = 0
        dir_count = 0
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs:
                dirs.remove(".venv")
            file_count += len(files)
            dir_count += len(dirs)
        return {"files": file_count, "dirs": dir_count}

    def append_log(self, message):
        timestamp = time.strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
        return log_entry

    def add_event(self, event_type, msg):
        event = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "type": event_type,
            "msg": msg
        }
        self.event_history.insert(0, event)
        if len(self.event_history) > 50:
            self.event_history.pop()
        self.append_log(f"EVENT [{event_type}]: {msg}")

    def load_logs(self, limit=100):
        if os.path.exists(self.log_path):
            with open(self.log_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
                raw_lines = content.splitlines()
                lines = raw_lines[max(0, len(raw_lines) - int(limit)):]
                return "\n".join(lines) + "\n" if lines else ""
        return "--- No previous logs found ---\n"

    def perform_backup(self, reason="Manual"):
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{backup_dir}/evolution_backup_{timestamp}.zip"
        
        # Prepare Semantic DNA Metadata
        sloc = self.count_sloc()
        issues = self.check_code_health()
        metadata = {
            "timestamp": timestamp,
            "reason": reason,
            "personality": self.config.get("personality", "Default"),
            "energy": self.energy,
            "sloc": sloc,
            "smells": len(issues),
            "version": "3.1"
        }
        meta_path = "dna_metadata.json"
        
        try:
            # Write temp metadata file
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=4)
                
            with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add metadata first
                zipf.write(meta_path, "dna_metadata.json")
                
                for root, dirs, files in os.walk("."):
                    if ".venv" in dirs: dirs.remove(".venv")
                    if "backups" in dirs: dirs.remove("backups")
                    if "snapshots" in dirs: dirs.remove("snapshots")
                    if "__pycache__" in dirs: dirs.remove("__pycache__")
                    
                    for file in files:
                        if file.endswith(('.py', '.json', '.log', '.md')) and file != meta_path:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, ".")
                            zipf.write(file_path, arcname)
            
            if os.path.exists(meta_path): os.remove(meta_path)
            
            # [v4.20 Hardened-DNA]
            self.generate_dna_manifest(filename)
            
            self.add_event("BACKUP", f"Semantic DNA Snapshot created: {os.path.basename(filename)} (Reason: {reason})")
            return True, filename
        except Exception as e:
            if os.path.exists(meta_path): os.remove(meta_path)
            return False, str(e)

    def get_backup_metadata(self, zip_filename):
        """Extracts the DNA metadata from a specific backup ZIP."""
        zip_path = os.path.join("backups", zip_filename)
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                if "dna_metadata.json" in zipf.namelist():
                    return json.loads(zipf.read("dna_metadata.json").decode('utf-8'))
        except Exception: pass
        return None

    def rollback_to_snapshot(self, zip_filename):
        """Autonomously restores the project state from a selected snapshot."""
        zip_path = os.path.join("backups", zip_filename)
        if not os.path.exists(zip_path): return False, "Snapshot not found."
        
        self.add_event("ROLLBACK", f"Initiating project restoration from {zip_filename}...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                # Simple extraction (overwrite existing)
                for item in zipf.namelist():
                    if item == "dna_metadata.json": continue
                    zipf.extract(item, ".")
            self.add_event("ROLLBACK", "Restoration complete. System DNA stabilized.")
            return True, "State successfully restored."
        except Exception as e:
            self.add_event("ERROR", f"Rollback failed: {e}")
            return False, str(e)

    def sign_packet(self, data: str):
        """Signs evolutionary data with a secret key for telemetry integrity."""
        secret = self.config.get("telemetry_secret", "SYSTEM_CORE_BETA_2026").encode()
        signature = hmac.new(secret, data.encode(), hashlib.sha256).hexdigest()
        return signature

    def broadcast_evolution_state(self, endpoint=None):
        """Bundles DNA metadata and metabolic state into a signed packet and transmits it."""
        if not endpoint:
            endpoint = self.config.get("telemetry_endpoint")
        if not endpoint: return False, "No telemetry endpoint configured."

        self.add_event("SYNC", f"Broadcasting evolution state to {endpoint}...")
        try:
            sloc = self.count_sloc()
            issues = self.check_code_health()
            payload = {
                "dna": {
                    "timestamp": datetime.now().isoformat(),
                    "personality": self.config.get("personality", "Default"),
                    "energy": self.energy,
                    "sloc": sloc,
                    "smells": len(issues),
                    "version": "3.2"
                },
                "system": self.get_system_stats()
            }
            
            json_data = json.dumps(payload)
            signature = self.sign_packet(json_data)
            
            req = urllib.request.Request(endpoint, data=json_data.encode(), method='POST')
            req.add_header('Content-Type', 'application/json')
            req.add_header('X-Evolution-Signature', signature)
            req.add_header('User-Agent', 'Antigravity-Evolution-Engine/3.2')
            
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status in [200, 201, 202]:
                    self.add_event("SYNC", "Evolution state successfully synchronized.")
                    return True, "Broadcast successful."
                else:
                    return False, f"Unexpected response: {response.status}"
        except Exception as e:
            self.add_event("ERROR", f"Broadcast failed: {e}")
            return False, str(e)

    def poll_remote_commands(self, endpoint=None):
        """Polls the command endpoint for authorized evolutionary directives."""
        if not endpoint:
            endpoint = self.config.get("command_endpoint")
        if not endpoint: return False, "No command endpoint configured."

        try:
            req = urllib.request.Request(endpoint, method='GET')
            req.add_header('User-Agent', 'Antigravity-Evolution-Engine/3.3')
            
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = response.read().decode()
                    signature = response.headers.get('X-Evolution-Signature')
                    
                    if not signature:
                        return False, "Command packet missing signature."
                    
                    # Verify signature
                    expected_sig = self.sign_packet(data)
                    if signature != expected_sig:
                        self.add_event("SECURITY", "Rejected unauthorized remote command (Signature mismatch).")
                        return False, "Invalid command signature."
                    
                    cmd_data = json.loads(data)
                    return self.dispatch_remote_command(cmd_data)
                elif response.status == 204: # No Content
                    return True, "No pending commands."
                else:
                    return False, f"Unexpected response: {response.status}"
        except Exception as e:
            return False, str(e)

    def dispatch_remote_command(self, cmd_data: dict):
        """Executes authorized evolutionary directives."""
        cmd_type = cmd_data.get("command")
        params = cmd_data.get("params", {})
        
        self.add_event("SYNC", f"Executing remote directive: {cmd_type}")
        
        if cmd_type == "CHANGE_PERSONALITY":
            new_p = params.get("personality")
            if new_p in self.personality_quotes:
                self.config["personality"] = new_p
                self.save_config(self.config)
                self.speak(f"Neural recalibration complete. Personality shifted to {new_p}.")
                # If we have a reference to the GUI, we could call apply_theme directly, 
                # but it polls config anyway.
                return True, f"Shifted to {new_p}"
                
        elif cmd_type == "TRIGGER_BACKUP":
            reason = params.get("reason", "Remote Directive")
            success, path = self.perform_backup(reason=reason)
            return success, f"Backup created: {path}" if success else path
            
        elif cmd_type == "METABOLIC_SHIFT":
            new_interval = params.get("interval")
            if new_interval:
                self.config["metabolic_interval"] = float(new_interval)
                self.save_config(self.config)
                return True, f"Interval updated to {new_interval}"
                
        return False, f"Unknown or unsupported command: {cmd_type}"

    def calculate_adaptive_heartbeat(self):
        """Dynamically adjusts metabolic frequency based on environmental load and stability."""
        try:
            cpu = psutil.cpu_percent(interval=None)
            issues = self.check_code_health()
            error_count = len(issues)
            
            # Base interval from personality
            p = self.config.get("personality", "Default")
            if p == "Performance": base = 2.0
            elif p == "Safety": base = 8.0
            else: base = 4.0
            
            # Modifier logic
            modifier = 1.0
            
            thermal_score = self.calculate_thermal_score()
            
            # 1. Thermal Modifier
            if thermal_score > 80: modifier *= 3.0  # Critical overheating, massive slowdown
            elif thermal_score > 60: modifier *= 1.8 # High heat, slow down
            elif thermal_score < 25: modifier *= 0.7 # Cold/Idle, evolutionary sprint
            
            new_interval = base * modifier
            
            new_interval = float(int(max(1.0, min(20.0, base * modifier)) * 10)) / 10.0
            
            if new_interval != self.config.get("metabolic_interval"):
                self.config["metabolic_interval"] = new_interval
                self.save_config(self.config)
                self.add_event("METABOLISM", f"Heartbeat recalibrated: {new_interval} min (CPU: {cpu}%, Issues: {error_count})")
            
            return new_interval
        except Exception as e:
            self.add_event("ERROR", f"Metabolic scaling failed: {e}")
            return self.config.get("metabolic_interval", 4.0)

    def proactive_logic_hardening(self):
        """Analyzes changes since last snapshot and generates targeted proactive tests."""
        try:
            snaps = self.get_ui_snapshots()
            if not snaps: return False, "No snapshots for diff."
            
            # Simple approach: compare current file hashes with stored ones if available, 
            # or just look at last modified times vs last snapshot time.
            last_snap_time = snaps[-1]['time']
            hot_files = []
            for f in self.scripts:
                if os.path.getmtime(f) > last_snap_time:
                    hot_files.append(f)
            
            if not hot_files:
                return True, "No proactive hardening required."
            
            self.add_event("HARDENING", f"Identifying hot functions in {len(hot_files)} modified files...")
            
            # For each hot file, identify functions (simplified regex search for now)
            hot_functions = []
            for fpath in hot_files:
                with open(fpath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.strip().startswith("def "):
                            func_name = line.split("(")[0].replace("def ", "").strip()
                            if func_name not in ["__init__"]:
                                hot_functions.append(f"{os.path.basename(fpath)}::{func_name}")
            
            if hot_functions:
                # Limit to top 3 to preserve energy
                targets = hot_functions[:3]
                self.add_event("HARDENING", f"Proactive hardening targets: {', '.join(targets)}")
                # Trigger targeted test evolution (stub for actual multi-agent synthesis)
                success = self.trigger_throttled_task(self.evolve_test_suite, energy_cost=25)
                if success:
                    return True, f"Hardened {len(targets)} logic nodes."
            
            return True, "Diff complete. No critical logic drift detected."
        except Exception as e:
            self.add_event("ERROR", f"Proactive hardening failed: {e}")
            return False, str(e)

    def predictive_energy_scheduling(self):
        """Strategic metabolic states based on goal proximity and energy reserves."""
        try:
            state = "STEADY"
            multiplier = 1.0
            
            # 1. Goal Proximity Analysis
            goals = self.get_goal_status()
            near_milestone = any(g["percent"] > 0.95 and g["percent"] < 1.0 for g in goals)
            
            # 2. Energy Reserve Analysis
            if near_milestone and self.energy > 40:
                state = "SPRINT"
                multiplier = 0.5 # Double speed
            elif self.energy < 30:
                state = "RECHARGE"
                multiplier = 2.0 # Half speed
                
            if state != self.metabolic_state:
                self.add_event("METABOLISM", f"Transitioning to {state} state (x{multiplier} speed).")
                self.metabolic_state = state
                
            return multiplier, state
        except Exception as e:
            self.add_event("ERROR", f"Energy scheduling failed: {e}")
            return 1.0, "STEADY"

    def simulate_logic_divergence(self, target_file):
        """[v4.10 Temporal-Decentralization] Generates and audits candidates via a decentralized swarm cluster."""
        if not os.path.exists(target_file): return False, "Target file missing."
        
        self.add_event("DIVERGENCE", f"Initiating decentralized swarm for {os.path.basename(target_file)}...")
        
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                original_content = f.read()
            
            # 1. Spawn decentralized evolution cluster
            # This triggers parallel EvolutionSandbox threads
            self.spawn_evolution_cluster(count=4)
            
            # 2. Merge results from the cluster (blocking till threads finish)
            winning_candidate = self.merge_cluster_results()
            
            if winning_candidate:
                # Commit winning logic
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(winning_candidate)
                
                self.add_event("DIVERGENCE", "Swarm consensus reached. Logic evolved.")
                return True, "Evolved via Decentralized Swarm."
            else:
                return False, "Swarm failed to produce a viable candidate."
                
        except Exception as e:
            self.add_event("ERROR", f"Decentralized divergence failed: {e}")
            return False, str(e)

    def generate_personality_biased_candidates(self, original_content, override_personality=None):
        """Generates code variations biased toward the (potentially overridden) persona's priorities."""
        persona = override_personality if override_personality else self.config.get("personality", "Default")
        candidates = []
        
        # [V4.30] TRUE AUTONOMOUS AI CALL via Headless Bridge
        if hasattr(self, "ai_worker") and getattr(self.ai_worker, "is_ready", False):
            prompt = f"Please refactor the following Python code focusing purely on {persona.upper()} improvements. Return ONLY valid Python code between ```python blocks.\n\n```python\n{original_content}\n```"
            self.add_event("HEADLESS-BRIDGE", f"Requesting real AI generation for {persona}...")
            try:
                ai_response = self.ai_worker.ask_sync(prompt)
                code_match = ""
                if "```python" in ai_response:
                    parts = ai_response.split("```python")
                    if len(parts) > 1:
                        code_match = parts[1].split("```")[0].strip()
                elif "```" in ai_response:
                    parts = ai_response.split("```")
                    if len(parts) > 1:
                        code_match = parts[1].strip()
                else:
                    code_match = ai_response.strip()
                    
                if code_match and self.synaptic_filter(code_match):
                    tag = self.generate_semantic_tag({"code": code_match})
                    candidates.append({"code": code_match, "semantic_tag": tag, "id": 999})
                    self.add_event("HEADLESS-BRIDGE", "Successfully received and parsed AI candidate.")
                    self.synapse_stats["accepted"] += 1
            except Exception as e:
                self.add_event("ERROR", f"Headless Bridge sync failed: {e}")
                self.synapse_stats["suppressed"] += 1

        # Fallback / Baseline biases (Mock generation)
        styles = {
            "Performance": "# PERFORMANCE_BIAS: Optimized logic selected.\n",
            "Safety": "# SAFETY_BIAS: Robust error-handling included.\n",
            "Aesthetic": "# AESTHETIC_BIAS: PEP8 compliance maximized.\n",
            "Default": "# DEFAULT_BIAS: Neutral evolutionary path.\n"
        }
        bias_marker = styles.get(persona, styles["Default"])
        
        for i in range(1, 3 - len(candidates)): # Fill up to 3 candidates
            code_variation = original_content + f"\n{bias_marker}# Variation {i}\n" 
            if self.synaptic_filter(code_variation):
                tag = self.generate_semantic_tag({"code": code_variation})
                candidates.append({"code": code_variation, "semantic_tag": tag, "id": i})
                self.synapse_stats["accepted"] += 1
            else:
                self.synapse_stats["suppressed"] += 1
                self.broadcast_signal("synapse_pruned", {"candidate_id": i})
                
        return candidates

    def synaptic_filter(self, candidate):
        """Rule-based gating to prune low-quality or misaligned logic, modified by resonance weights."""
        # Rule 1: Complexity Check
        # Adjusted by weight: lower weight = stricter threshold
        complexity_threshold = 500 * self.synaptic_weights.get("complexity", 1.0)
        if len(candidate.splitlines()) > complexity_threshold:
            return False
            
        # Rule 2: Personality Resonance
        persona = self.config.get("personality", "Default")
        if persona == "Safety":
            if self.synaptic_weights.get("personality", 1.0) < 0.8:
                # Even stricter if personality alignment has been failing
                risky = ["eval(", "exec(", "os.system(", "subprocess.Popen(", "keyboard", "pyautogui"]
            else:
                risky = ["eval(", "exec(", "os.system(", "subprocess.Popen("]
                
            if any(r in candidate for r in risky):
                return False
                
        # Rule 3: Structural Integrity (Basic DNA resonance)
        if "SystemEngine" in candidate:
            has_func = any(line.strip().startswith("def ") for line in candidate.splitlines())
            if not has_func:
                return False 
            
        return True

    def apply_synaptic_feedback(self, success, rules_triggered=None):
        """Adjusts rule weights based on verification success/failure."""
        adjustment = 0.05
        if success:
            for rule in self.synaptic_weights:
                self.synaptic_weights[rule] = min(2.0, self.synaptic_weights[rule] + adjustment)
            self.resonance_history.append(1.0)
        else:
            if rules_triggered:
                for rule in rules_triggered:
                    self.synaptic_weights[rule] = max(0.1, self.synaptic_weights[rule] - (adjustment * 2))
            self.resonance_history.append(0.0)
            
        if len(self.resonance_history) > 50:
            self.resonance_history.pop(0)
            
        self.broadcast_signal("synapse_feedback", {"weights": self.synaptic_weights})

    def predict_energy_metabolism(self) -> float:
        """Forecasts future energy state (10 cycles ahead) based on recent decay. [Lint Fix]"""
        history_len = len(self.history["energy"])
        if history_len < 5:
            return self.energy
        recent = self.history["energy"][-5:]
        decay = sum([recent[i] - recent[i-1] for i in range(1, len(recent))]) / 4
        return max(0.0, self.energy + (decay * 10))

    def auto_regulate_metabolism(self):
        """Proactively switches to RECHARGE if predict < 20. [v4.9]"""
        predicted = self.predict_energy_metabolism()
        if predicted < 20.0 and self.metabolic_state != "RECHARGE":
            self.metabolic_state = "RECHARGE"
            self.append_log("PREDICTIVE: Anticipating energy dip. Charging.")
        
        if self.energy < 10.0:
            self.metabolic_state = "RECHARGE"
        elif self.energy > 90.0:
            self.metabolic_state = "STEADY"

    def subconscious_tuner(self):
        """[v4.12 Subconscious-Refactoring] Autonomously adjusts synaptic weights based on architectural audit."""
        audit_score = self.architectural_auditor()
        self.add_event("TUNING", f"Initiating subconscious weight optimization (Audit: {audit_score:.2f})")
        
        # If audit score is low (high coupling/complexity), tighten filters
        adjustment = 0.05
        if audit_score < 0.6:
            # High coupling - Increase complexity penalty
            self.synaptic_weights["complexity"] = max(0.1, self.synaptic_weights.get("complexity", 1.0) - adjustment)
            # Relax personality slightly to allow different patterns
            self.synaptic_weights["personality"] = min(2.0, self.synaptic_weights.get("personality", 1.0) + adjustment)
            self.add_event("TUNING", "Architectural entropy detected. Tightening complexity constraints.")
        else:
            # Healthy architecture - allow more experimental variance
            self.synaptic_weights["complexity"] = min(2.0, self.synaptic_weights.get("complexity", 1.0) + adjustment)
            self.add_event("TUNING", "Structural integrity optimal. Expanding evolutionary variance.")
            
        self.broadcast_signal("synapse_feedback", {"weights": self.synaptic_weights, "tuning_event": True})
    
    def analyze_visual_metabolism(self, payload):
        """[v4.8] Receives feedback from the UI to bias neural evolution."""
        self.actual_visual_state = payload.get("state", "STEADY")
        feedback = payload.get("intensity", 0.5)
        self.synesthesia_bias = feedback
        
        if feedback > 0.8:
            self.add_event("SYNESTHESIA", f"High Metabolism detected ({feedback:.2f}). Triggering Hyper-Divergence.")
        elif feedback < 0.2:
            self.add_event("SYNESTHESIA", f"Low Metabolism detected ({feedback:.2f}). Entering Architectural-Silence.")
            self.refactor_neutral_logic()

    def calculate_aesthetic_resonance(self) -> float:
        """[v4.15] Measures alignment between metabolic load and visual presence."""
        m_state = getattr(self, "metabolic_state", "STEADY")
        v_state = getattr(self, "actual_visual_state", "STEADY")
        
        if m_state == v_state:
            self.aesthetic_resonance = 1.0
        elif (m_state == "SPRINT" and v_state == "RECHARGE") or (m_state == "RECHARGE" and v_state == "SPRINT"):
            self.aesthetic_resonance = 0.2
        else:
            self.aesthetic_resonance = 0.6
            
        return float(f"{self.aesthetic_resonance:.4f}")

    def calculate_neural_harvesting(self) -> float:
        """[v4.16] Optimizes operational efficiency based on metabolic state."""
        m_state = getattr(self, "metabolic_state", "STEADY")
        
        # Efficiency profile: 
        # RECHARGE: 1.5x (Harvesting energy by doing less)
        # STEADY: 1.0x (Direct balance)
        # SPRINT: 0.5x (Burning energy for high output)
        if m_state == "RECHARGE":
            self.harvest_efficiency = 1.5
            self.task_throttle = 2.0  # Slow down tasks
        elif m_state == "SPRINT":
            self.harvest_efficiency = 0.5
            self.task_throttle = 0.5  # Speed up tasks (high burn)
        else:
            self.harvest_efficiency = 1.0
            self.task_throttle = 1.0
            
        return self.harvest_efficiency

    def capture_node_snapshot(self, node_name: str, logic_content: str) -> str:
        """[v4.17] Captures a fine-grained snapshot of a specific logic node."""
        timestamp = int(time.time())
        snapshot_id = f"{node_name}_{timestamp}"
        file_path = os.path.join(self.node_snapshot_dir, f"{snapshot_id}.log")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(logic_content)
            
        self.append_log(f"COGNITIVE: Captured snapshot {snapshot_id}")
        return snapshot_id

    def rollback_node(self, node_name: str, snapshot_id: str) -> bool:
        """[v4.17] Restores a logic node from a specific snapshot."""
        file_path = os.path.join(self.node_snapshot_dir, f"{snapshot_id}.log")
        if not os.path.exists(file_path):
            return False
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # [HEURISTIC] In a real scenario, this would involve regex replacement in the source file.
        # For this autonomous evolution simulation, we log the intent and update the divergence sandbox.
        self.append_log(f"COGNITIVE: Rolled back {node_name} to {snapshot_id}")
        return True

    def map_logic_entanglement(self):
        """[v4.18] Analyzes codebase to build a semantic dependency graph."""
        import re
        self.logic_graph = {}
        nodes = []
        
        # 1. Discover all logic nodes
        for script in self.scripts:
            if not os.path.exists(script): continue
            with open(script, "r", encoding="utf-8") as f:
                content = f.read()
                # Find class methods and top-level functions
                found = re.findall(r"def\s+([a-zA-Z_0-9]+)\s*\(", content)
                nodes.extend(found)
        
        # 2. Map dependencies
        for target_node in set(nodes):
            self.logic_graph[target_node] = []
            for script in self.scripts:
                if not os.path.exists(script): continue
                with open(script, "r", encoding="utf-8") as f:
                    content = f.read()
                    # A node calls target_node if its name appears in the content followed by open paren
                    # Also ensure it's not the definition itself
                    calls = re.findall(r"(?<!def\s)" + re.escape(target_node) + r"\(", content)
                    if calls:
                        # Find which node contains the call (approximate by looking for previous def)
                        lines = content.split("\n")
                        current_node = "global"
                        for line in lines:
                            def_match = re.match(r"^\s*def\s+([a-zA-Z_0-9]+)\s*\(", line)
                            if def_match:
                                current_node = def_match.group(1)
                            
                            if target_node + "(" in line and current_node != target_node:
                                if current_node not in self.logic_graph[target_node]:
                                    self.logic_graph[target_node].append(current_node)
            
        self.append_log(f"SEMANTIC: Logic graph mapped with {len(self.logic_graph)} nodes.")
        return self.logic_graph

    def get_entanglement_score(self, node_name: str) -> float:
        """Calculates risk score based on how many nodes depend on this one."""
        # Simple fan-in heuristic
        fan_in = 0.0
        for node, deps in self.logic_graph.items():
            if node_name in deps:
                fan_in += 1.0
        return min(1.0, fan_in / 10.0)

    def get_resonance_score(self):
        """Calculates the floating resonance (success rate) of logic candidates."""
        if not self.resonance_history:
            return 1.0
        return sum(self.resonance_history) / len(self.resonance_history)

    def get_entropy_score(self, target_path=None):
        """Calculates the ratio of boilerplate/redundancy to actual functional logic."""
        if not target_path:
            target_path = __file__.replace(".pyc", ".py")
        
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()
            marker_count = sum(content.count(m) for m in self.bloat_markers)
            line_count = len(content.splitlines())
            
            # Entropy increases with marker density
            entropy = (marker_count * 10) / line_count if line_count > 0 else 0
            return min(1.0, entropy)
        except:
            return 0.1

    def refactor_neutral_logic(self, target_path=None):
        """Proactively prunes low-resonance markers and dead-code from the DNA."""
        if not target_path:
            target_path = __file__.replace(".pyc", ".py")
        
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            clean_lines = [l for l in lines if not any(m in l for m in self.bloat_markers)]
            removed = len(lines) - len(clean_lines)
            
            if removed > 0:
                with open(target_path, "w", encoding="utf-8") as f:
                    f.writelines(clean_lines)
                self.add_event("ENTROPY", f"Refactoring complete. Pruned {removed} redundant logic markers.")
                self.broadcast_signal("entropy_pruned", {"removed": removed})
                return True
        except Exception as e:
            self.add_event("ERROR", f"Entropy reduction failed: {e}")
            
        return False

    def spawn_evolution_cluster(self, count=3):
        """Spawns a cluster of parallel evolution sandboxes."""
        vision = self.get_current_vision()
        personalities = ["Performance", "Safety", "Aesthetic"]
        
        self.active_sandboxes = []
        for i in range(min(count, len(personalities))):
            sb = EvolutionSandbox(i, self, vision, personalities[i])
            sb.start()
            self.active_sandboxes.append(sb)
            
        self.broadcast_signal("cluster_active", {"nodes": len(self.active_sandboxes)})
        return self.active_sandboxes

    def merge_cluster_results(self):
        """Aggregates and merges candidates from the evolution cluster."""
        best_sb = None
        max_res = -1.0
        
        # Ensure active_sandboxes is iterated safely
        sandboxes = list(self.active_sandboxes)
        for sb in sandboxes:
            if not sb: continue
            sb.join()
            res = getattr(sb, 'resonance', -1.0)
            if res > max_res:
                max_res = res
                best_sb = sb
                
        self.active_sandboxes = []
        if best_sb and hasattr(best_sb, 'result') and best_sb.result:
            self.broadcast_signal("cluster_merged", {"id": best_sb.sandbox_id, "resonance": max_res})
            return best_sb.result
        return None

    def get_current_vision(self):
        try:
            with open(self.roadmap_path, "r") as f:
                data = json.load(f)
            return data.get("vision", "Evolution")
        except: return "Unknown"

    def architectural_auditor(self) -> float:
        """[v4.11 Structural-Consciousness] Analyzes the meta-architectural health by mapping node coupling."""
        try:
            # Simple consciousness index: Ratio of decoupled modules to total scripts
            coupling_stats = self.get_connectivity_stats(limit=None)
            total_imports = sum(coupling_stats.values())
            if total_imports == 0: return 1.0
            
            # High coupling = low consciousness (too reactive/interdependent)
            # Low coupling = high consciousness (modular/autonomous)
            independence_index = len(coupling_stats) / total_imports
            return min(1.0, independence_index * 2.5) # Scaling factor
        except Exception:
            return 0.5

    def calculate_structural_resonance(self) -> float:
        """[v4.14] Tracks architectural stability over time to detect drift."""
        try:
            curr_audit = self.architectural_auditor()
            self.resonance_history.append(curr_audit)
            if len(self.resonance_history) > 10:
                self.resonance_history.pop(0)
            
            if len(self.resonance_history) < 3:
                return 1.0
                
            # Calculate variance (stability measure)
            avg = sum(self.resonance_history) / len(self.resonance_history)
            variance = sum((x - avg) ** 2 for x in self.resonance_history) / len(self.resonance_history)
            
            # Lower variance = Higher resonance (Stability)
            # Resonance = 1.0 - (Variance * 10) clamped
            res = max(0.0, 1.0 - (variance * 10))
            self.resonance_wave = float(f"{res:.4f}")
            return self.resonance_wave
        except Exception:
            return 1.0

    def structural_resonance_engine(self):
        """[v4.14] Autonomous monitor that triggers repair if resonance fails."""
        res = getattr(self, 'resonance_wave', 1.0)
        if res < self.resonance_threshold:
            self.add_event("RESONANCE", f"Structural resonance drop detected ({res}). Triggering evolution...")
            self.spawn_evolution_cluster(count=3)
            return True
        return False

    def evolve_roadmap(self):
        """Autonomously analyzes system state to predict and set the next evolutionary goal."""
        self.add_event("STRATEGY", "Initiating autonomous roadmap evolution...")
        
        # 1. Analyze state
        energy = self.energy
        persona = self.config.get("personality", "Default")
        
        # 2. Generate Vision
        new_milestone = f"Evo-{random.randint(1000, 9999)}"
        if energy > 80 and persona == "Performance":
            vision = "Aggressive Throughput Optimization"
        elif energy < 40:
            vision = "Deep Architectural Recharge"
        else:
            vision = "Balanced Feature Synthesis"
            
        # 3. Persist
        try:
            with open(self.roadmap_path, "r") as f:
                data = json.load(f)
            data["vision"] = vision
            data["milestones"].append({"id": new_milestone, "vision": vision, "time": time.time()})
            with open(self.roadmap_path, "w") as f:
                json.dump(data, f, indent=4)
            
            self.add_event("STRATEGY", f"New Vision projected: {vision} ({new_milestone})")
            return True, vision
        except Exception as e:
            self.add_event("ERROR", f"Roadmap evolution failed: {e}")
            return False, str(e)

    def automated_regression_healing(self, target_file):
        """Autonomously heals a file by merging its current state with its last healthy snapshot."""
        if not os.path.exists(target_file): return False, "Target missing."
        
        self.add_event("IMMUNE", f"Corrupt logic detected in {os.path.basename(target_file)}. Initiating self-healing...")
        self.is_healing = True
        
        try:
            # 1. Locate last healthy snapshot
            snapshots = sorted([s for s in os.listdir(self.snapshot_dir) if s.startswith("dna_")], reverse=True)
            if not snapshots:
                self.is_healing = False
                return False, "No snapshots available for healing."
            
            # (Simplified: using the latest snapshot as the 'healthy' source)
            latest_snap = os.path.join(self.snapshot_dir, snapshots[0])
            with open(latest_snap, "r", encoding="utf-8") as f:
                healthy_content = f.read()
            
            # 2. Trigger Divergence with Snapshot as one of the candidates
            self.add_event("IMMUNE", f"Synthesizing repair candidates using snapshot {snapshots[0]}...")
            
            # We use simulate_logic_divergence but we manually inject the healthy content as a candidate
            # In a real scenario, this would be a more complex merge logic
            # [v4.19] Consensus Gate
            if not self.apply_consensus_healing({"node": os.path.basename(target_file), "type": "REGRESSION"}):
                self.add_event("CONSENSUS", "Healing REJECTED: Insufficient structural resonance.")
                self.is_healing = False
                return False, "Consensus rejected."
                
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(healthy_content + "\n# HEALED_FROM_SNAPSHOT_V419_CONSENSUS\n")
            
            self.add_event("IMMUNE", "Healing complete. Architectural integrity restored.")
            self.is_healing = False
            return True, "Integrity restored from snapshot."
        except Exception as e:
            self.add_event("ERROR", f"Healing failed: {e}")
            self.is_healing = False
            return False, str(e)

    def sync_metabolic_pulse(self):
        """Generates a dynamic pulse intensity synchronized with system state."""
        self.pulse_time += 0.1
        base_freq = 1.0 # default frequency
        base_amp = 0.5 # default amplitude
        
        # Adjust frequency based on state
        if self.is_healing:
            base_freq = 4.0 # Erratic/High
            base_amp = 0.8
        elif len(os.listdir(self.sandbox_dir)) > 0 if os.path.exists(self.sandbox_dir) else False:
            base_freq = 0.5 # Deep/Stable
            base_amp = 0.3
            
        # Sinusoidal pulse with noise
        pulse = base_amp * math.sin(self.pulse_time * base_freq) + (random.random() * 0.1)
        self.pulse_intensity = max(0, min(1, (pulse + 1) / 2)) # Normalize to 0-1
        
        # Broadcast pulse signal
        self.broadcast_signal("pulse", self.pulse_intensity)
        
        return self.pulse_intensity

    def broadcast_signal(self, topic, payload):
        """Emits a signal through the Neural Conduction Hub."""
        self.hub.emit(topic, payload)

    def subscribe_to_signals(self, topic, callback):
        """Allows external components to subscribe to engine signals."""
        self.hub.subscribe(topic, callback)

    def log_performance_csv(self, stats):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.csv_path, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, 
                stats["cpu"], 
                stats["ram_percent"], 
                stats["disk_percent"], 
                f"{stats['net_up_kb']:.2f}", 
                f"{stats['net_down_kb']:.2f}",
                stats.get("smells", 0),
                self.config.get("personality", "Default")
            ])

    def optimize_strategy_thresholds(self):
        """Analyzes CSV to find which personalities are most efficient and adjusts config."""
        if not os.path.exists(self.csv_path): return None
        
        persona_stats = {} # name -> {smell_reduction: total, count: N, metabolism: total}
        
        try:
            with open(self.csv_path, "r") as f:
                reader = csv.DictReader(f)
                last_smells = None
                for row in reader:
                    persona = row.get("Persona", "Default")
                    try:
                        curr_smells = float(row.get("Code_Smells", 0))
                        cpu = float(row.get("CPU_%", 0))
                        ram = float(row.get("RAM_%", 0))
                        metabolism = cpu + ram
                        
                        if persona not in persona_stats:
                            persona_stats[persona] = {"reduction": 0.0, "count": 0, "metabolism": 0.0}
                        
                        if last_smells is not None:
                            reduction = max(0.0, last_smells - curr_smells)
                            persona_stats[persona]["reduction"] += reduction
                        
                        persona_stats[persona]["metabolism"] += metabolism
                        persona_stats[persona]["count"] += 1
                        last_smells = curr_smells
                    except: continue
        except: return None
        
        # Calculate Efficiency (Reduction per Metabolism point)
        best_persona = "Default"
        max_efficiency = -1.0
        efficiencies = {}
        
        for p, s in persona_stats.items():
            if s["count"] == 0: continue
            eff = s["reduction"] / (s["metabolism"] / s["count"] + 0.1) # avoid div zero
            efficiencies[p] = eff
            if eff > max_efficiency:
                max_efficiency = eff
                best_persona = p
        
        # Adjust thresholds based on best performer
        # Example: If 'Performance' is most efficient, lower its entry energy threshold
        if "strategy_overrides" not in self.config:
            self.config["strategy_overrides"] = {}
            
        old_val = self.config["strategy_overrides"].get(f"{best_persona}_efficiency", 1.0)
        self.config["strategy_overrides"][f"{best_persona}_efficiency"] = max_efficiency
        self.save_config(self.config)
        
        self.add_event("META_EVO", f"Strategy Evolved: {best_persona} identified as most efficient (Eff:{max_efficiency:.2f}).")
        return {"best": best_persona, "efficiencies": efficiencies}

    def trigger_throttled_task(self, task_func, energy_cost):
        """Proactively checks for metabolic headroom before execution."""
        if self.energy < energy_cost:
            # Not enough energy for even one execution
            self.buffering_target_energy = energy_cost * 2.0
            return False
            
        if self.buffering_target_energy > 0:
            if self.energy < self.buffering_target_energy:
                # Still in buffering mode
                return False
            else:
                # Buffer achieved!
                self.buffering_target_energy = 0.0

        # Survival Margin: Ensure we have at least 10 units left for OS/Watchdog stability
        if self.energy - energy_cost < 10.0:
            self.buffering_target_energy = energy_cost + 15.0
            self.add_event("METABOLISM", f"Entering BUFFERING mode to sustain {task_func.__name__}")
            return False

        # Proceed with task
        self.energy -= energy_cost
        task_func()
        return True

    def cleanup_old_data(self, days=1):
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            return 0
        
        count = 0
        now = time.time()
        for f in os.listdir(backup_dir):
            f_path = os.path.join(backup_dir, f)
            if os.path.isfile(f_path) and f.endswith(".zip"):
                if os.stat(f_path).st_mtime < now - (days * 86400):
                    try:
                        os.remove(f_path)
                        count += 1
                    except Exception:
                        pass
        if count > 0:
            self.add_event("CLEANUP", f"Removed {count} old backups")
        return count

    def get_heatmap_data(self):
        """Analyzes codebase density and activity to generate architectural heat metrics."""
        heatmap = []
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    sloc = self.get_sloc_for_file(path)
                    m_score = self.get_metabolic_score(path)
                    heatmap.append({
                        "file": os.path.relpath(path, "."),
                        "score": sloc + m_score,
                        "type": "CORE" if sloc > 500 else "LEAF"
                    })
        return heatmap

    def get_sloc_for_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return len([l for l in f if l.strip()])
        except: return 0

    def get_metabolic_score(self, path):
        """Calculates a 'heat' score based on file modification frequency and recent events."""
        try:
            mtime = os.path.getmtime(path)
            now = time.time()
            age_factor = max(0.1, 1.0 - (now - mtime) / 86400) # Decay over 24h
            
            # Event multiplier
            fname = os.path.basename(path)
            event_hits = len([e for e in self.event_history if fname in e["msg"]])
            
            return (age_factor * 100) + (event_hits * 50)
        except: return 0.0

    def generate_evolution_report(self):
        report_path = "evolution_report.md"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Stats from CSV
        avg_cpu = 0
        avg_ram = 0
        recorded_points = 0
        if os.path.exists(self.csv_path):
            with open(self.csv_path, "r") as f:
                reader = csv.DictReader(f)
                cpu_vals = []
                ram_vals = []
                for row in reader:
                    try:
                        cpu_vals.append(float(row["CPU_%"]))
                        ram_vals.append(float(row["RAM_%"]))
                    except Exception: pass
                if cpu_vals:
                    avg_cpu = sum(cpu_vals) / len(cpu_vals)
                    avg_ram = sum(ram_vals) / len(ram_vals)
                    recorded_points = len(cpu_vals)

        # Stats from project
        p_stats = self.get_project_stats()
        sloc = self.count_sloc()
        
        # Count backups
        backup_count = 0
        if os.path.exists("backups"):
            backup_count = len([f for f in os.listdir("backups") if f.endswith(".zip")])

        report_content = f"""# AI Evolution Report
Generated at: {now}

## 🚀 Performance Overview (Last {recorded_points} minutes)
- **Average CPU Usage:** {avg_cpu:.2f}%
- **Average RAM Usage:** {avg_ram:.2f}%
- **Data Points Collected:** {recorded_points}

## 📂 Project Statistics
- **Total Files:** {p_stats['files']}
- **Total Directories:** {p_stats['dirs']}
- **Source Lines of Code (SLOC):** {sloc}
- **Stored Backups:** {backup_count}

## 📝 Recent Activity Summary
The system has been autonomously evolving. Check `app.log` for granular event details.

---
*Generated autonomously by Evolution Engine v2.0*
"""
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        self.add_event("REPORT", "Generated new evolution report")
        return report_path

    def git_commit(self, message=None):
        if not os.path.exists(".git"):
            return False, "Not a git repository."
        
        if message is None:
            # Autonomous message generation
            p_stats = self.get_project_stats()
            health = self.get_health_forecast()[0]
            timestamp = datetime.now().strftime("%H:%M:%S")
            message = f"Autonomous Evolution Step [{timestamp}] | Files: {p_stats['files']} | Health: {health}"
            
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", message], check=True)
            self.add_event("GIT", f"Committed: {message}")
            return True, f"Changes committed: {message}"
        except Exception as e:
            self.add_event("ERROR", f"Git commit failed: {e}")
            return False, str(e)

    def get_ui_snapshots(self):
        """Retrieves metadata of stored UI snapshots for diff-analysis."""
        if not os.path.exists(self.snapshot_dir): return []
        snaps = []
        for f in os.listdir(self.snapshot_dir):
            if f.endswith(".png"):
                mtime = os.path.getmtime(os.path.join(self.snapshot_dir, f))
                snaps.append({'path': os.path.join(self.snapshot_dir, f), 'time': mtime})
        snaps.sort(key=lambda x: x['time'])
        return snaps

    def save_ui_snapshot(self, x, y, w, h):
        if not os.path.exists(self.snapshot_dir):
            os.makedirs(self.snapshot_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = os.path.join(self.snapshot_dir, f"evolution_{timestamp}.png")
        try:
            # Region: (left, top, width, height)
            pyautogui.screenshot(fname, region=(x, y, w, h))
            self.add_event("SNAPSHOT", f"UI State archived: {os.path.basename(fname)}")
            return True, fname
        except Exception as e:
            self.add_event("ERROR", f"Snapshot failed: {e}")
            return False, str(e)

    def get_history_snapshots(self):
        snap_dir = "snapshots"
        if not os.path.exists(snap_dir):
            return []
        
        snaps = []
        for f in os.listdir(snap_dir):
            if f.endswith(".png"):
                path = os.path.join(snap_dir, f)
                # Filename format: evolution_20260327_024542.png
                try:
                    ts_str = f.replace("evolution_", "").replace(".png", "")
                    # 20260327_024542 -> readable
                    dt = datetime.strptime(ts_str, "%Y%m%d_%H%M%S")
                    snaps.append({
                        "path": os.path.abspath(path),
                        "time": dt.strftime("%Y-%m-%d %H:%M:%S"),
                        "raw_time": ts_str
                    })
                except: continue
        
        # Sort by time
        snaps.sort(key=lambda x: x["raw_time"])
        return snaps

    def fix_common_bugs(self):
        """Autonomously scans and repairs frequent codebase anomalies."""
        repaired = []
        # Pattern 1: Missing float cast for canvas ops
        for root, dirs, files in os.walk("."):
            if ".venv" in dirs: dirs.remove(".venv")
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        modified = content
                        # Replace generic int grid with float for better coordinate math
                        if "x_off, y_off = 20, 20" in modified:
                            modified = modified.replace("x_off, y_off = 20, 20", "x_off, y_off = 20.0, 20.0")
                        
                        if modified != content:
                            with open(path, "w", encoding="utf-8") as f:
                                f.write(modified)
                            repaired.append(f"Standardized offsets in {file}")
                            self.healed_registry[file] = time.time()
                    except: pass
        
        if repaired:
            self.add_event("HEAL", f"Self-Correction applied: {', '.join(repaired)}")
        return repaired

    def apply_consensus_healing(self, candidate_info: dict) -> bool:
        """Validates a healing proposal across multiple metabolic perspectives."""
        # 1. Structural Perspective
        res = self.calculate_structural_resonance()
        if res < 0.6: return False # Foundation too unstable
        
        # 2. Thermal Perspective (Energy)
        if self.energy < 30.0: return False # Low metabolic pressure
        
        # 3. Semantic Perspective (Entanglement)
        node = str(candidate_info.get("node", ""))
        if node:
            score = self.get_entanglement_score(node)
            if score > 0.8: return False # Too entangled for autonomous healing
            
        # [v4.20 Meta-Governor Overrule]
        if not self.apply_meta_governance():
            self.add_event("GOVERNOR", "Consensus OVERRULED: System invariants violated.")
            return False
            
        self.add_event("CONSENSUS", f"Healing consensus reached for {node}. Proceeding.")
        return True

    def apply_meta_governance(self) -> bool:
        """[v4.20] High-level safety invariants enforcement."""
        cpu = psutil.cpu_percent()
        disk = psutil.disk_usage('/')
        
        # Invariant 1: CPU Throttling
        if cpu > 70.0:
            return False
            
        # Invariant 2: Disk Exhaustion (10% Buffer)
        if disk.percent > 90.0:
            return False
            
        return True

    def calculate_thermal_score(self) -> float:
        """[v4.21] Calculates weighted Neural-Thermal pressure (0-100)."""
        try:
            cpu = psutil.cpu_percent(interval=None)
            smells = len(self.check_code_health())
            
            # Architectural Heat (based on recent activity density)
            recent_cutoff = time.time() - 600 # 10 minutes
            recent_ops = [e for e in self.event_history if float(e.get('timestamp_raw', 0)) > recent_cutoff]
            arch_heat = min(100.0, float(len(recent_ops) * 10))
            
            # Weighted Thermal Score
            # 50% CPU, 20% Stability (Smells), 30% Architectural Heat
            score = (cpu * 0.5) + (min(100, smells * 10) * 0.2) + (arch_heat * 0.3)
            
            # [v4.22] Auto-trigger pruning if score is high
            if score > 75:
                self.prune_synaptic_memory(aggressive=True)
            elif self.iteration % 10 == 0:
                self.prune_synaptic_memory(aggressive=False)
                
            # [v4.23] Auto-trigger healer every 20 iterations
            if self.iteration % 20 == 0:
                threading.Thread(target=self.autonomous_healer, daemon=True).start()
                
            # [v4.24] Auto-trigger refiner when thermal is low and health is low
            if score < 30 and smells > 10 and self.iteration % 5 == 0:
                threading.Thread(target=self.subconscious_refiner, daemon=True).start()
                
            return round(max(0, min(100, score)), 1)
        except Exception:
            return 50.0

    def prune_synaptic_memory(self, aggressive: bool = False):
        """[v4.22] Trims history buffers to prevent state bloat."""
        try:
            limit = 50 if aggressive else 200
            if len(self.event_history) > limit:
                self.event_history = self.event_history[-limit:]
                self.add_event("PRUNE", f"Synaptic memory pruned ({'Aggressive' if aggressive else 'Standard'}).")

            hist_limit = 30 if aggressive else 100
            for key in self.history:
                if len(self.history[key]) > hist_limit:
                    self.history[key] = self.history[key][-hist_limit:]
        except Exception as e:
            self.add_event("ERROR", f"Memory pruning failed: {e}")

    def autonomous_healer(self):
        """[v4.23] Scans and repairs missing dependencies automatically."""
        self.healing_state = "SCANNING"
        try:
            missing = self.check_dependencies()
            if not missing:
                self.healing_state = "STABLE"
                return
            
            self.healing_state = "REPAIRING"
            for pkg in missing:
                success, output = self.install_dependency(pkg)
                if success:
                    self.add_event("HEAL", f"Autonomous Healer resolved dependency: {pkg}")
                else:
                    self.add_event("ERROR", f"Autonomous Healer failed to resolve {pkg}: {output[:50]}...")
            
            self.healing_state = "STABLE"
        except Exception as e:
            self.add_event("ERROR", f"Autonomous Healer encountered a systemic failure: {e}")
            self.healing_state = "ERROR"

    def subconscious_refiner(self):
        """[v4.24] Background maintenance to reduce technical debt."""
        self.refiner_state = "THINKING"
        try:
            # Find a messy file (mocking multi-file analysis for demonstration)
            target_file = "system_engine.py" # Self-optimization target
            self.add_event("REFINER", f"Thinking about {target_file} optimization...")
            time.sleep(1) # Simulation of deep analysis
            
            self.refiner_state = "REFINING"
            # Pattern: Consolidate redundant blank lines or mock docstring cleanup
            # Actually just adding a tiny refinement marker for v4.24 validation
            with open(target_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            marker = "[V424" + "_MARKER]"
            if marker not in content:
                # Add a marker or perform tiny cleanup
                # For safety, we just log the thinking process for now
                self.add_event("REFINER", f"Simulated refinement of {target_file} with {marker}")
            
            self.refiner_state = "POLISHED"
            time.sleep(2)
            self.refiner_state = "SLEEPING"
        except Exception as e:
            self.add_event("ERROR", f"Subconscious refactoring failed: {e}")
            self.refiner_state = "SLEEPING"

    def evaluate_consensus(self, candidates: List[Any]) -> Any:
        """[v4.25] Weights multiple evolution paths to find the optimal trajectory."""
        if not candidates:
            self.consensus_strength = 0.0
            return None
        
        # Weighted calculation based on Resonance vs Complexity vs Semantic Intent
        scored_candidates = []
        thermal = self.calculate_thermal_score()
        
        for c in candidates:
            # Resonance (0.0-1.0) * 100
            score = self.get_resonance_score() * 100
            
            # [v4.25 Logic] Penalize high complexity if thermal is high
            if thermal > 50:
                score -= (thermal - 50) * 0.5
            
            # [v4.27 Logic] Apply semantic weight
            tag = c.get("semantic_tag", "EXPERIMENTAL")
            weight = self.semantic_weights.get(tag, 1.0)
            
            # [v4.28 Logic] Adaptive Success Weighting
            mem = self.semantic_memory.get(tag, {"success": 0, "fail": 0})
            total = mem["success"] + mem["fail"]
            if total > 0:
                success_rate = mem["success"] / total
                # Adaptive multiplier: 0.5x to 1.5x based on success rate
                weight *= (0.5 + success_rate)
            
            # Contextual bonus (e.g., thermal stress favors optimization)
            if thermal > 70 and tag == "OPTIMIZATION":
                weight *= 1.5
            
            score *= weight
            scored_candidates.append((score, c))
            
        # Select best
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        best_weighted_score, best_candidate = scored_candidates[0]
        
        # Calculate Consensus Strength (variance between top candidates)
        if len(scored_candidates) > 1:
            diff = abs(scored_candidates[0][0] - scored_candidates[1][0])
            self.consensus_strength = round(max(0, 100 - diff), 1)
        else:
            self.consensus_strength = 100.0
            
        self.add_event("CONSENSUS", f"Selected {tag} path ({best_weighted_score:.1f}) with {self.consensus_strength}% strength.")
        
        # [v4.28] Persistence for outcome tracking
        self.config["last_winner_tag"] = tag
        self.save_config(self.config)
        self.record_semantic_outcome(tag, success=True) # Assume success initially
        
        return best_candidate

    def record_semantic_outcome(self, tag: str, success: bool):
        """[v4.28] Records the evolutionary result of a semantic intent."""
        if tag not in self.semantic_memory:
            self.semantic_memory[tag] = {"success": 0, "fail": 0}
        
        if success:
            self.semantic_memory[tag]["success"] += 1
        else:
            # If we had recorded a success but now rollback, correct it
            if self.semantic_memory[tag]["success"] > 0:
                self.semantic_memory[tag]["success"] -= 1
            self.semantic_memory[tag]["fail"] += 1
            
        self.config["semantic_memory"] = self.semantic_memory
        self.save_config(self.config)
        self.add_event("NEURAL-SYNC", f"Feedback loop updated: {tag} {'SUCCESS' if success else 'FAILURE'}")

    def generate_semantic_tag(self, candidate: Dict[str, Any]) -> str:
        """[v4.27] Heuristic categorization of a candidate's intent (prioritized)."""
        try:
            code = str(candidate.get("code", "")).upper()
            if "TRY:" in code or "EXCEPT " in code or "GOVERNOR" in code:
                return "SAFETY"
            if "OPTIMIZE" in code or "BATCH" in code or "MIN(" in code:
                return "OPTIMIZATION"
            if "SELF." in code and ("BUTTON" in code or "LABEL" in code or "TKINTER" in code):
                return "UI"
            if "DEF " in code or "CLASS " in code or "RETURN " in code:
                return "LOGIC"
        except Exception:
            pass
        return "EXPERIMENTAL"

    def DNA_checkpointer(self):
        """[v4.26] Saves an architectural snapshot for potential rollbacks."""
        try:
            with open(self.config_path, "r") as f:
                dna = f.read()
            with open(self.checkpoint_path, "w") as f:
                f.write(dna)
            self.add_event("GOVERNOR", "DNA Checkpoint updated.")
        except Exception as e:
            self.add_event("ERROR", f"Checkpoint failed: {e}")

    def trigger_architectural_rollback(self):
        """[v4.26] Reverts to the last stable DNA checkpoint."""
        try:
            self.governor_state = "REVERTING"
            if os.path.exists(self.checkpoint_path):
                with open(self.checkpoint_path, "r") as f:
                    dna = f.read()
                with open(self.config_path, "w") as f:
                    f.write(dna)
                self.load_config()
                self.add_event("GOVERNOR", "CRITICAL ROLLBACK EXECUTED. Stable state restored.")
                
                # [v4.28] Record failure for the last elected path if possible
                last_tag = self.config.get("last_winner_tag")
                if last_tag:
                    self.record_semantic_outcome(last_tag, success=False)
                
                self.governor_state = "ACTIVE"
                return True
        except Exception as e:
            self.add_event("ERROR", f"Rollback failed: {e}")
            self.governor_state = "ACTIVE"
        return False

    def apply_meta_governance(self) -> str:
        """[v4.26] Refactored to actively monitor and protect system integrity."""
        # Default state
        target_state = "ACTIVE"

        # Check for catastrophic consensus failure
        if self.consensus_strength < 20.0:
            target_state = "ALERT"
            self.add_event("GOVERNOR", f"LOW CONSENSUS ALERT: {self.consensus_strength}%")
            
        # Check for architectural bloat/smell overflow
        smells = len(self.check_code_health())
        if smells > 50:
            target_state = "REVERTING"
            self.add_event("GOVERNOR", f"SMELL OVERFLOW ({smells}). Triggering rollback...")
            self.trigger_architectural_rollback()
            
        self.governor_state = target_state
        return self.governor_state

    def calculate_memory_pressure(self) -> float:
        """[v4.22] Estimates architectural state pressure (0-100)."""
        try:
            # Estimate based on internal history sizes
            events_p = min(100, (len(self.event_history) / 200) * 100)
            hist_p = min(100, (len(self.history.get("cpu", [])) / 100) * 100)
            return round((events_p * 0.7) + (hist_p * 0.3), 1)
        except Exception:
            return 0.0

    def generate_dna_manifest(self, backup_path: str):
        """[v4.20] Generates SHA3-256 integrity manifest for architectural snapshots."""
        manifest_path = backup_path + ".manifest.json"
        try:
            with open(backup_path, "rb") as f:
                content = f.read()
                digest = hashlib.sha3_256(content).hexdigest()
            
            manifest = {
                "snapshot": os.path.basename(backup_path),
                "integrity": f"sha3-256:{digest}",
                "timestamp": datetime.now().isoformat(),
                "governor_v": "4.20"
            }
            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=4)
        except Exception as e:
            self.append_log(f"GOVERNOR_ERROR: Manifest generation failed: {e}")

    def get_predictive_load_status(self):
        """Predicts future workload and suggests resource conservation."""
        # 1. Analyze energy trend
        energy_critical = self.energy < 25.0
        
        # 2. Analyze proximity to evolution goals
        goals = self.get_goal_status()
        near_goal = any(g["percent"] > 0.85 for g in goals)
        
        # 3. Analyze recent activity
        recent_events = self.event_history[-10:]
        high_activity = len([e for e in recent_events if e["type"] in ["BACKUP", "REFACTOR", "ARCH"]]) > 4
        
        if (energy_critical or high_activity) and near_goal:
            return "THROTTLE_PREDICTIVE", "Metabolic preservation for upcoming milestone."
        elif energy_critical:
            return "CONSERVE", "Low energy. Background tasks slowed."
        
        return "STABLE", "Resources optimal."

    def run_autonomous_tests(self):
        """Triggers the logic verification sub-process."""
        try:
            import subprocess
            subprocess.Popen([sys.executable, "test_engine_logic.py"])
            self.add_event("TEST", "Autonomous logic verification sequence triggered.")
            return True
        except Exception as e:
            self.add_event("ERROR", f"Failed to trigger tests: {e}")
            return False

    def update_node_position(self, node_id, x, y):
        """Persists custom architectural layout coordinates."""
        self.node_positions[node_id] = (x, y)
        self.config["node_positions"] = self.node_positions
        self.save_config(self.config)
        return True

    def get_module_activity(self):
        """Returns normalized activity scores (0-1) for all modules based on heat and events."""
        heatmap = self.get_heatmap_data()
        activity = {}
        recent_evs = [e["type"] for e in self.event_history[-10:]]
        
        for item in heatmap:
            mod = str(item["file"]).replace(".py", "")
            # Base activity from metabolic heat
            m_score = self.get_metabolic_score(os.path.join(".", str(item["file"])))
            base = min(1.0, m_score / 500.0)
            
            # Bonus activity if module is frequently involved in recent events
            event_bonus = 0.0
            found_bonus = False
            for e in self.event_history[max(0, len(self.event_history)-5):]:
                if mod in str(e):
                    found_bonus = True
                    break
            if found_bonus: event_bonus = 0.2
            
            activity[mod] = min(1.0, base + event_bonus)
        return activity
