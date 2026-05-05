"""System Analysis and Monitoring Module"""

import subprocess
import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import platform

logger = logging.getLogger(__name__)

class SystemAnalyzer:
    """System monitoring and security analysis"""
    
    def __init__(self):
        """Initialize system analyzer"""
        self.os_type = platform.system()
        self.is_linux = self.os_type in ['Linux']
    
    def analyze_system_security(self) -> Dict[str, Any]:
        """Comprehensive system security analysis"""
        if not self.is_linux:
            return {'error': 'This feature requires Linux'}
        
        return {
            'timestamp': datetime.now().isoformat(),
            'os_info': self._get_os_info(),
            'security_status': self._check_security_status(),
            'network_analysis': self._analyze_network(),
            'process_analysis': self._analyze_processes(),
            'file_permissions': self._analyze_file_permissions(),
            'system_vulnerabilities': self._check_vulnerabilities(),
        }
    
    def _get_os_info(self) -> Dict[str, str]:
        """Get OS information"""
        try:
            info = {
                'os_type': self.os_type,
                'hostname': self._run_command('hostname'),
                'kernel_version': self._run_command('uname -r'),
                'uptime': self._run_command('uptime -p'),
            }
            return {k: v.strip() if v else 'N/A' for k, v in info.items()}
        except Exception as e:
            logger.error(f"Error getting OS info: {str(e)}")
            return {}
    
    def _check_security_status(self) -> Dict[str, Any]:
        """Check system security status"""
        try:
            return {
                'firewall': self._check_firewall(),
                'selinux': self._check_selinux(),
                'sudo_access': self._check_sudo_access(),
                'ssh_enabled': self._check_ssh(),
                'updates_available': self._check_updates(),
            }
        except Exception as e:
            logger.error(f"Error checking security: {str(e)}")
            return {}
    
    def _analyze_network(self) -> Dict[str, Any]:
        """Analyze network configuration"""
        try:
            return {
                'open_ports': self._get_open_ports(),
                'listening_services': self._get_listening_services(),
                'network_interfaces': self._get_network_interfaces(),
                'dns_config': self._get_dns_config(),
            }
        except Exception as e:
            logger.error(f"Error analyzing network: {str(e)}")
            return {}
    
    def _analyze_processes(self) -> Dict[str, Any]:
        """Analyze running processes"""
        try:
            suspicious_processes = self._find_suspicious_processes()
            return {
                'total_processes': self._get_process_count(),
                'suspicious_processes': suspicious_processes,
                'high_memory_usage': self._get_high_memory_processes(),
                'high_cpu_usage': self._get_high_cpu_processes(),
            }
        except Exception as e:
            logger.error(f"Error analyzing processes: {str(e)}")
            return {}
    
    def _analyze_file_permissions(self) -> Dict[str, List[str]]:
        """Analyze file permissions for security issues"""
        try:
            return {
                'world_writable': self._find_world_writable_files(),
                'suid_files': self._find_suid_files(),
                'sgid_files': self._find_sgid_files(),
            }
        except Exception as e:
            logger.error(f"Error analyzing permissions: {str(e)}")
            return {}
    
    def _check_vulnerabilities(self) -> List[Dict[str, str]]:
        """Check for known vulnerabilities"""
        vulnerabilities = []
        
        # Check for common CVE patterns
        kernel_version = self._run_command('uname -r')
        if kernel_version:
            # Simplified check - in production would use CVE database
            if '4.4' in kernel_version:
                vulnerabilities.append({
                    'type': 'kernel_cve',
                    'version': kernel_version,
                    'recommendation': 'Update kernel to latest version'
                })
        
        return vulnerabilities
    
    # Helper methods
    def _run_command(self, command: str) -> Optional[str]:
        """Run shell command safely"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Error running command {command}: {str(e)}")
            return None
    
    def _check_firewall(self) -> Dict[str, str]:
        """Check firewall status"""
        status = self._run_command('sudo systemctl is-active firewalld')
        return {
            'service': 'firewalld',
            'status': 'active' if status == 'active' else 'inactive'
        }
    
    def _check_selinux(self) -> Dict[str, str]:
        """Check SELinux status"""
        status = self._run_command('getenforce')
        return {
            'service': 'selinux',
            'status': status or 'not available'
        }
    
    def _check_sudo_access(self) -> str:
        """Check sudo access"""
        try:
            result = subprocess.run(['sudo', '-v'], capture_output=True, timeout=2)
            return 'enabled' if result.returncode == 0 else 'disabled'
        except:
            return 'unknown'
    
    def _check_ssh(self) -> Dict[str, str]:
        """Check SSH status"""
        status = self._run_command('sudo systemctl is-active ssh')
        return {
            'service': 'ssh',
            'status': 'active' if status == 'active' else 'inactive',
            'port': '22 (default)'
        }
    
    def _check_updates(self) -> str:
        """Check for available updates"""
        updates = self._run_command('apt list --upgradable 2>/dev/null | wc -l')
        if updates:
            return f"{updates} packages available"
        return "Unable to check"
    
    def _get_open_ports(self) -> List[str]:
        """Get list of open ports"""
        output = self._run_command('sudo netstat -tuln 2>/dev/null | grep LISTEN')
        if output:
            return output.split('\n')[:10]  # Limit to 10
        return []
    
    def _get_listening_services(self) -> List[str]:
        """Get listening services"""
        output = self._run_command('sudo ss -tlnp 2>/dev/null')
        if output:
            return output.split('\n')[:10]  # Limit to 10
        return []
    
    def _get_network_interfaces(self) -> List[str]:
        """Get network interfaces"""
        output = self._run_command('ip link show')
        if output:
            return output.split('\n')[:10]  # Limit to 10
        return []
    
    def _get_dns_config(self) -> List[str]:
        """Get DNS configuration"""
        output = self._run_command('cat /etc/resolv.conf | grep nameserver')
        if output:
            return output.split('\n')
        return []
    
    def _get_process_count(self) -> int:
        """Get total process count"""
        output = self._run_command('ps aux | wc -l')
        return int(output) if output else 0
    
    def _find_suspicious_processes(self) -> List[str]:
        """Find potentially suspicious processes"""
        suspicious_keywords = ['nc', 'netcat', 'ncat', 'telnet', '/dev/tcp']
        suspicious = []
        
        output = self._run_command('ps aux')
        if output:
            for line in output.split('\n'):
                if any(keyword in line.lower() for keyword in suspicious_keywords):
                    suspicious.append(line.strip())
        
        return suspicious[:10]
    
    def _get_high_memory_processes(self) -> List[Dict[str, str]]:
        """Get processes using high memory"""
        output = self._run_command('ps aux --sort=-%mem | head -5')
        if output:
            return [{'process': line.strip()} for line in output.split('\n')[1:6]]
        return []
    
    def _get_high_cpu_processes(self) -> List[Dict[str, str]]:
        """Get processes using high CPU"""
        output = self._run_command('ps aux --sort=-%cpu | head -5')
        if output:
            return [{'process': line.strip()} for line in output.split('\n')[1:6]]
        return []
    
    def _find_world_writable_files(self) -> List[str]:
        """Find world-writable files (security risk)"""
        output = self._run_command('find / -perm -002 -type f 2>/dev/null')
        if output:
            return output.split('\n')[:10]  # Limit to 10
        return []
    
    def _find_suid_files(self) -> List[str]:
        """Find SUID files"""
        output = self._run_command('find / -perm -4000 -type f 2>/dev/null')
        if output:
            return output.split('\n')[:10]  # Limit to 10
        return []
    
    def _find_sgid_files(self) -> List[str]:
        """Find SGID files"""
        output = self._run_command('find / -perm -2000 -type f 2>/dev/null')
        if output:
            return output.split('\n')[:10]  # Limit to 10
        return []
