from system_engine import SystemEngine
from dashboard_gui import EvolutionDashboard
import customtkinter as ctk

def main():
    # Initialize Core Engine
    engine = SystemEngine()
    
    # Initialize GUI with Engine
    app = EvolutionDashboard(engine)
    
    # Run
    app.mainloop()

if __name__ == "__main__":
    main()


