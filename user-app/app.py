from flask import Flask, render_template, redirect, request, session
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# ============================================
# MOCK DATA - Replace with database calls later
# ============================================

USER_DATA = {
    "username": os.getenv("USERNAME", "demo_user"),
    "email": os.getenv("EMAIL", "user@example.com"),
    "container_id": os.getenv("CONTAINER_ID", "abc123def456"),
    "port": os.getenv("PORT", "8080"),
    "status": "running",
    "uptime_days": 7,
    "created_date": "2024-01-10",
    "last_started": "Today at 09:00",
}

ACTIVITY_LOG = [
    {"time": "Today 14:32", "action": "Service restarted"},
    {"time": "Yesterday 09:15", "action": "Container created successfully"},
    {"time": "Yesterday 09:10", "action": "User account registered"},
]

METRICS = {
    "cpu_avg": 49,
    "cpu_max": 61,
    "memory_avg": 39,
    "memory_max": 51,
    "uptime_avg": 99.0,
    "uptime_max": 100,
}

HEALTH_STATUS = {
    "service": {"label": "Service Status", "status": "healthy", "text": "✓ Healthy"},
    "cpu": {"label": "CPU Load", "status": "warning", "text": "⚠ Normal"},
    "memory": {"label": "Memory Usage", "status": "healthy", "text": "✓ Good"},
    "connectivity": {"label": "Connectivity", "status": "healthy", "text": "✓ Connected"},
}

# ============================================
# ROUTES
# ============================================

@app.route("/")
def dashboard():
    """Main dashboard page with comprehensive user data"""
    
    context = {
        # User information
        "username": USER_DATA["username"],
        "email": USER_DATA["email"],
        "container_id": USER_DATA["container_id"],
        "port": USER_DATA["port"],
        
        # Status information
        "container_status": USER_DATA["status"].capitalize(),
        "uptime_days": USER_DATA["uptime_days"],
        "created_date": USER_DATA["created_date"],
        "last_started": USER_DATA["last_started"],
        "last_update": "Now",
        
        # Metrics
        "cpu_avg": METRICS["cpu_avg"],
        "cpu_max": METRICS["cpu_max"],
        "memory_avg": METRICS["memory_avg"],
        "memory_max": METRICS["memory_max"],
        "uptime_avg": METRICS["uptime_avg"],
        "uptime_max": METRICS["uptime_max"],
        
        # Activity log
        "activity_log": ACTIVITY_LOG,
        
        # Health status
        "health_status": HEALTH_STATUS,
    }
    
    return render_template("index.html", **context)

@app.route("/logs")
def logs():
    """View service logs (redirect placeholder)"""
    return render_template("logs.html", logs=ACTIVITY_LOG)

@app.route("/settings")
def settings():
    """User settings page"""
    return render_template("settings.html", username=USER_DATA["username"], email=USER_DATA["email"])

@app.route("/activity")
def activity():
    """Full activity history"""
    return render_template("activity.html", activity_log=ACTIVITY_LOG)

@app.route("/help")
def help():
    """Help and support page"""
    return render_template("help.html")

@app.route("/logout")
def logout():
    """Logout user and redirect to auth service"""
    session.clear()
    return redirect("http://localhost:5000/user/login")

@app.route("/api/status")
def api_status():
    """API endpoint for service status"""
    return {
        "status": USER_DATA["status"],
        "uptime_days": USER_DATA["uptime_days"],
        "port": USER_DATA["port"],
        "timestamp": datetime.now().isoformat(),
    }

@app.route("/api/restart", methods=["POST"])
def api_restart():
    """API endpoint to restart service"""
    return {
        "success": True,
        "message": "Service restart initiated",
        "timestamp": datetime.now().isoformat(),
    }

@app.route("/api/metrics")
def api_metrics():
    """API endpoint for metrics data"""
    return {
        "cpu": {
            "average": METRICS["cpu_avg"],
            "max": METRICS["cpu_max"],
        },
        "memory": {
            "average": METRICS["memory_avg"],
            "max": METRICS["memory_max"],
        },
        "uptime": {
            "average": METRICS["uptime_avg"],
            "max": METRICS["uptime_max"],
        },
    }

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return render_template("500.html"), 500

# ============================================
# CONTEXT PROCESSORS
# ============================================

@app.context_processor
def inject_now():
    """Inject current time into all templates"""
    return {"now": datetime.now()}

@app.context_processor
def inject_user():
    """Inject user data into all templates"""
    return {
        "current_user": USER_DATA["username"],
        "user_email": USER_DATA["email"],
    }

# ============================================
# STARTUP
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 User Dashboard Service Starting")
    print("=" * 50)
    print(f"Username: {USER_DATA['username']}")
    print(f"Email: {USER_DATA['email']}")
    print(f"Service Port: {USER_DATA['port']}")
    print("=" * 50)
    
    # Development mode - change to False for production
    debug_mode = os.getenv("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=80, debug=debug_mode)
