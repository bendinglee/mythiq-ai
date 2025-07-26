"""
Mythiq AI - Advanced Diagnostics and Performance Monitoring
Real-time monitoring, health checks, performance analytics, and alerting
"""

import time
import psutil
import threading
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import deque, defaultdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Individual performance metric data point."""
    timestamp: str
    metric_name: str
    value: float
    unit: str
    tags: Dict[str, str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {}

@dataclass
class HealthCheck:
    """Health check result."""
    service_name: str
    status: str  # healthy, degraded, unhealthy
    response_time: float
    error_message: Optional[str] = None
    last_check: str = None
    consecutive_failures: int = 0
    
    def __post_init__(self):
        if self.last_check is None:
            self.last_check = datetime.now().isoformat()

@dataclass
class Alert:
    """System alert."""
    alert_id: str
    severity: str  # info, warning, error, critical
    message: str
    service: str
    metric_name: str
    threshold_value: float
    actual_value: float
    timestamp: str = None
    resolved: bool = False
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class DiagnosticsManager:
    """Advanced diagnostics and monitoring system."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize diagnostics manager."""
        self.config = config or {}
        
        # Performance metrics storage (in-memory with size limits)
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.health_checks: Dict[str, HealthCheck] = {}
        self.alerts: List[Alert] = []
        self.alert_handlers: List[Callable] = []
        
        # Monitoring configuration
        self.monitoring_interval = self.config.get("monitoring_interval", 30)  # seconds
        self.alert_thresholds = self.config.get("alert_thresholds", {
            "response_time": 5.0,  # seconds
            "memory_usage": 80.0,  # percentage
            "cpu_usage": 80.0,     # percentage
            "error_rate": 10.0,    # percentage
            "disk_usage": 90.0     # percentage
        })
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_thread = None
        self.start_time = time.time()
        
        # Performance counters
        self.request_counts = defaultdict(int)
        self.error_counts = defaultdict(int)
        self.response_times = defaultdict(list)
        
        logger.info("DiagnosticsManager initialized")
    
    def start_monitoring(self):
        """Start background monitoring."""
        if self.monitoring_active:
            logger.warning("Monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        logger.info("Background monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Background monitoring stopped")
    
    def _monitoring_loop(self):
        """Background monitoring loop."""
        while self.monitoring_active:
            try:
                self._collect_system_metrics()
                self._check_alert_conditions()
                time.sleep(self.monitoring_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_system_metrics(self):
        """Collect system performance metrics."""
        timestamp = datetime.now().isoformat()
        
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        self.record_metric("cpu_usage", cpu_percent, "percent", timestamp)
        
        # Memory metrics
        memory = psutil.virtual_memory()
        self.record_metric("memory_usage", memory.percent, "percent", timestamp)
        self.record_metric("memory_available", memory.available / (1024**3), "GB", timestamp)
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        self.record_metric("disk_usage", disk_percent, "percent", timestamp)
        
        # Network metrics (if available)
        try:
            network = psutil.net_io_counters()
            self.record_metric("network_bytes_sent", network.bytes_sent, "bytes", timestamp)
            self.record_metric("network_bytes_recv", network.bytes_recv, "bytes", timestamp)
        except:
            pass  # Network stats might not be available in all environments
        
        # Application metrics
        uptime = time.time() - self.start_time
        self.record_metric("uptime", uptime, "seconds", timestamp)
        
        # Request rate metrics
        total_requests = sum(self.request_counts.values())
        total_errors = sum(self.error_counts.values())
        error_rate = (total_errors / max(1, total_requests)) * 100
        
        self.record_metric("total_requests", total_requests, "count", timestamp)
        self.record_metric("error_rate", error_rate, "percent", timestamp)
    
    def record_metric(self, metric_name: str, value: float, unit: str, 
                     timestamp: str = None, tags: Dict[str, str] = None):
        """Record a performance metric."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        metric = PerformanceMetric(
            timestamp=timestamp,
            metric_name=metric_name,
            value=value,
            unit=unit,
            tags=tags or {}
        )
        
        self.metrics[metric_name].append(metric)
        logger.debug(f"Recorded metric {metric_name}: {value} {unit}")
    
    def record_request(self, endpoint: str, response_time: float, success: bool = True):
        """Record API request metrics."""
        self.request_counts[endpoint] += 1
        self.response_times[endpoint].append(response_time)
        
        if not success:
            self.error_counts[endpoint] += 1
        
        # Record as metrics
        timestamp = datetime.now().isoformat()
        self.record_metric(f"response_time_{endpoint}", response_time, "seconds", timestamp)
        
        # Check response time threshold
        if response_time > self.alert_thresholds.get("response_time", 5.0):
            self._create_alert(
                severity="warning",
                message=f"Slow response time for {endpoint}",
                service="api",
                metric_name="response_time",
                threshold_value=self.alert_thresholds["response_time"],
                actual_value=response_time
            )
    
    def add_health_check(self, service_name: str, check_function: Callable) -> bool:
        """Add a health check for a service."""
        try:
            start_time = time.time()
            result = check_function()
            response_time = time.time() - start_time
            
            if result:
                status = "healthy"
                error_message = None
                consecutive_failures = 0
            else:
                status = "unhealthy"
                error_message = "Health check failed"
                consecutive_failures = self.health_checks.get(service_name, HealthCheck(
                    service_name, "unknown", 0
                )).consecutive_failures + 1
            
            self.health_checks[service_name] = HealthCheck(
                service_name=service_name,
                status=status,
                response_time=response_time,
                error_message=error_message,
                consecutive_failures=consecutive_failures
            )
            
            logger.debug(f"Health check for {service_name}: {status}")
            return True
            
        except Exception as e:
            self.health_checks[service_name] = HealthCheck(
                service_name=service_name,
                status="unhealthy",
                response_time=0,
                error_message=str(e),
                consecutive_failures=self.health_checks.get(service_name, HealthCheck(
                    service_name, "unknown", 0
                )).consecutive_failures + 1
            )
            logger.error(f"Health check failed for {service_name}: {e}")
            return False
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall system health status."""
        overall_status = "healthy"
        unhealthy_services = []
        degraded_services = []
        
        for service_name, health_check in self.health_checks.items():
            if health_check.status == "unhealthy":
                overall_status = "unhealthy"
                unhealthy_services.append(service_name)
            elif health_check.status == "degraded":
                if overall_status == "healthy":
                    overall_status = "degraded"
                degraded_services.append(service_name)
        
        return {
            "overall_status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "uptime": time.time() - self.start_time,
            "services": {name: asdict(check) for name, check in self.health_checks.items()},
            "unhealthy_services": unhealthy_services,
            "degraded_services": degraded_services,
            "total_services": len(self.health_checks)
        }
    
    def get_performance_summary(self, hours: int = 1) -> Dict[str, Any]:
        """Get performance summary for the last N hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        summary = {}
        
        for metric_name, metric_deque in self.metrics.items():
            recent_metrics = [
                m for m in metric_deque 
                if datetime.fromisoformat(m.timestamp) > cutoff_time
            ]
            
            if recent_metrics:
                values = [m.value for m in recent_metrics]
                summary[metric_name] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "latest": values[-1],
                    "unit": recent_metrics[-1].unit
                }
        
        return {
            "time_range_hours": hours,
            "metrics": summary,
            "generated_at": datetime.now().isoformat()
        }
    
    def _check_alert_conditions(self):
        """Check for alert conditions."""
        # Check latest metrics against thresholds
        for metric_name, threshold in self.alert_thresholds.items():
            if metric_name in self.metrics and self.metrics[metric_name]:
                latest_metric = self.metrics[metric_name][-1]
                
                if latest_metric.value > threshold:
                    self._create_alert(
                        severity="warning" if latest_metric.value < threshold * 1.2 else "error",
                        message=f"{metric_name} exceeded threshold",
                        service="system",
                        metric_name=metric_name,
                        threshold_value=threshold,
                        actual_value=latest_metric.value
                    )
        
        # Check for consecutive health check failures
        for service_name, health_check in self.health_checks.items():
            if health_check.consecutive_failures >= 3:
                self._create_alert(
                    severity="error",
                    message=f"Service {service_name} has failed {health_check.consecutive_failures} consecutive health checks",
                    service=service_name,
                    metric_name="health_check",
                    threshold_value=3,
                    actual_value=health_check.consecutive_failures
                )
    
    def _create_alert(self, severity: str, message: str, service: str, 
                     metric_name: str, threshold_value: float, actual_value: float):
        """Create and process an alert."""
        alert_id = f"{service}_{metric_name}_{int(time.time())}"
        
        # Check if similar alert already exists and is unresolved
        existing_alert = None
        for alert in self.alerts:
            if (alert.service == service and 
                alert.metric_name == metric_name and 
                not alert.resolved):
                existing_alert = alert
                break
        
        if existing_alert:
            # Update existing alert
            existing_alert.actual_value = actual_value
            existing_alert.timestamp = datetime.now().isoformat()
            logger.debug(f"Updated existing alert {existing_alert.alert_id}")
        else:
            # Create new alert
            alert = Alert(
                alert_id=alert_id,
                severity=severity,
                message=message,
                service=service,
                metric_name=metric_name,
                threshold_value=threshold_value,
                actual_value=actual_value
            )
            
            self.alerts.append(alert)
            logger.warning(f"Created alert {alert_id}: {message}")
            
            # Trigger alert handlers
            for handler in self.alert_handlers:
                try:
                    handler(alert)
                except Exception as e:
                    logger.error(f"Error in alert handler: {e}")
    
    def add_alert_handler(self, handler: Callable[[Alert], None]):
        """Add an alert handler function."""
        self.alert_handlers.append(handler)
        logger.info("Added alert handler")
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                logger.info(f"Resolved alert {alert_id}")
                return True
        return False
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all unresolved alerts."""
        return [alert for alert in self.alerts if not alert.resolved]
    
    def get_alert_history(self, hours: int = 24) -> List[Alert]:
        """Get alert history for the last N hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [
            alert for alert in self.alerts
            if datetime.fromisoformat(alert.timestamp) > cutoff_time
        ]
    
    def get_diagnostics_report(self) -> Dict[str, Any]:
        """Generate comprehensive diagnostics report."""
        return {
            "system_health": self.get_health_status(),
            "performance_summary": self.get_performance_summary(hours=1),
            "active_alerts": [asdict(alert) for alert in self.get_active_alerts()],
            "recent_alerts": [asdict(alert) for alert in self.get_alert_history(hours=24)],
            "monitoring_config": {
                "monitoring_interval": self.monitoring_interval,
                "alert_thresholds": self.alert_thresholds,
                "monitoring_active": self.monitoring_active
            },
            "request_statistics": {
                "total_requests": sum(self.request_counts.values()),
                "total_errors": sum(self.error_counts.values()),
                "endpoints": dict(self.request_counts),
                "error_counts": dict(self.error_counts)
            },
            "generated_at": datetime.now().isoformat()
        }
    
    def cleanup_old_data(self, days: int = 7):
        """Clean up old metrics and alerts."""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        # Clean old alerts
        self.alerts = [
            alert for alert in self.alerts
            if datetime.fromisoformat(alert.timestamp) > cutoff_time
        ]
        
        # Metrics are automatically cleaned by deque maxlen
        logger.info(f"Cleaned up diagnostics data older than {days} days")
    
    def export_metrics(self, metric_names: List[str] = None, 
                      hours: int = 24) -> Dict[str, List[Dict]]:
        """Export metrics data for analysis."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        exported_metrics = {}
        
        metrics_to_export = metric_names or list(self.metrics.keys())
        
        for metric_name in metrics_to_export:
            if metric_name in self.metrics:
                recent_metrics = [
                    asdict(m) for m in self.metrics[metric_name]
                    if datetime.fromisoformat(m.timestamp) > cutoff_time
                ]
                exported_metrics[metric_name] = recent_metrics
        
        return exported_metrics

