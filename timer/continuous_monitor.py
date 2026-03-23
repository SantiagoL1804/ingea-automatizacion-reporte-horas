#!/usr/bin/env python3
import time
import sys
import signal
from branch_monitor import monitor_branch_changes

# Global flag for graceful shutdown
running = True

def signal_handler(signum, frame):
    global running
    print(f"\n🛑 Received signal {signum}. Shutting down gracefully...")
    running = False

def continuous_monitor(interval_seconds=30):
    """Continuously monitor branch changes at specified intervals"""
    global running
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal
    
    print(f"🚀 Starting continuous branch monitoring (checking every {interval_seconds}s)")
    print("Press Ctrl+C to stop")
    print("-" * 60)
    
    try:
        while running:
            print(f"⏰ {time.strftime('%Y-%m-%d %H:%M:%S')} - Checking for branch changes...")
            
            try:
                monitor_branch_changes()
            except Exception as e:
                print(f"❌ Error during monitoring: {e}")
            
            print(f"💤 Waiting {interval_seconds}s until next check...")
            
            # Sleep in small intervals to allow for graceful shutdown
            for _ in range(interval_seconds):
                if not running:
                    break
                time.sleep(1)
            
            print()  # Empty line for readability
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    
    print("👋 Branch monitoring stopped")

if __name__ == "__main__":
    # Default interval is 30 seconds, but can be customized
    interval = 30
    
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
            if interval < 10:
                print("⚠️  Warning: Minimum interval is 10 seconds")
                interval = 10
        except ValueError:
            print("❌ Invalid interval. Using default of 30 seconds.")
    
    continuous_monitor(interval)