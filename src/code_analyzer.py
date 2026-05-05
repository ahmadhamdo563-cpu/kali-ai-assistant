"""Code Analysis and Review Module"""

import os
import ast
import json
from typing import Dict, List, Any, Tuple
from pathlib import Path
import logging
import re
from collections import defaultdict

logger = logging.getLogger(__name__)

class CodeAnalyzer:
    """Advanced code analysis and review system"""
    
    SUPPORTED_LANGUAGES = {
        'python': ['.py'],
        'javascript': ['.js', '.jsx', '.ts', '.tsx'],
        'go': ['.go'],
        'rust': ['.rs'],
        'cpp': ['.cpp', '.cc', '.cxx', '.h', '.hpp'],
        'java': ['.java'],
        'c': ['.c', '.h'],
        'bash': ['.sh'],
    }
    
    SECURITY_PATTERNS = {
        'sql_injection': r"(execute|query|sql).*['\"].*\$|\?.*['\"]|f['\"].*\$",
        'xss_vulnerability': r"(innerHTML|dangerouslySetInnerHTML|eval)\s*[=:]",
        'hardcoded_password': r"(password|passwd|pwd|secret|key)\s*[=:]\s*['\"][^'\"]*['\"]",
        'unencrypted_connection': r"http://|telnet|ftp://",
        'unsafe_deserialization': r"(pickle|deserialize|loads)\s*\(",
        'command_injection': r"(system|exec|shell|subprocess)\s*\(",
        'weak_cryptography': r"(md5|sha1|des)\(|CryptContext\(schemes=\['plaintext'\]",
        'path_traversal': r"\.\.[\\/]",
    }
    
    CODE_QUALITY_RULES = {
        'max_function_length': 50,
        'max_cyclomatic_complexity': 10,
        'max_line_length': 100,
        'min_function_docstring': True,
        'naming_convention': 'snake_case',
    }
    
    def __init__(self):
        """Initialize code analyzer"""
        self.findings = defaultdict(list)
        self.metrics = {}
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single code file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {'error': f'File not found: {file_path}'}
            
            language = self._detect_language(file_path)
            
            if not language:
                return {'error': f'Unsupported file type: {file_path.suffix}'}
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Perform analyses
            security_issues = self._analyze_security(content, language)
            quality_issues = self._analyze_code_quality(content, language, file_path)
            metrics = self._calculate_metrics(content, language)
            suggestions = self._generate_suggestions(content, language, security_issues, quality_issues)
            
            return {
                'file': str(file_path),
                'language': language,
                'security_issues': security_issues,
                'quality_issues': quality_issues,
                'metrics': metrics,
                'suggestions': suggestions,
                'overall_risk': self._calculate_risk_score(security_issues),
                'code_quality_score': self._calculate_quality_score(quality_issues),
            }
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return {'error': str(e)}
    
    def analyze_directory(self, dir_path: str) -> Dict[str, Any]:
        """Analyze all code files in a directory"""
        try:
            dir_path = Path(dir_path)
            results = {
                'directory': str(dir_path),
                'files_analyzed': [],
                'total_security_issues': 0,
                'total_quality_issues': 0,
                'critical_vulnerabilities': [],
            }
            
            # Find all code files
            for language, extensions in self.SUPPORTED_LANGUAGES.items():
                for ext in extensions:
                    for file_path in dir_path.rglob(f'*{ext}'):
                        if '.git' not in str(file_path):  # Skip git directories
                            file_analysis = self.analyze_file(str(file_path))
                            
                            if 'error' not in file_analysis:
                                results['files_analyzed'].append(file_analysis)
                                results['total_security_issues'] += len(file_analysis.get('security_issues', []))
                                results['total_quality_issues'] += len(file_analysis.get('quality_issues', []))
                                
                                # Track critical issues
                                for issue in file_analysis.get('security_issues', []):
                                    if issue.get('severity') == 'CRITICAL':
                                        results['critical_vulnerabilities'].append({
                                            'file': file_analysis['file'],
                                            'issue': issue
                                        })
            
            return results
        except Exception as e:
            logger.error(f"Error analyzing directory {dir_path}: {str(e)}")
            return {'error': str(e)}
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        for language, extensions in self.SUPPORTED_LANGUAGES.items():
            if file_path.suffix in extensions:
                return language
        return None
    
    def _analyze_security(self, content: str, language: str) -> List[Dict[str, Any]]:
        """Analyze code for security vulnerabilities"""
        issues = []
        lines = content.split('\n')
        
        for pattern_name, pattern in self.SECURITY_PATTERNS.items():
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    severity = 'CRITICAL' if pattern_name in ['sql_injection', 'command_injection'] else 'HIGH'
                    issues.append({
                        'type': pattern_name,
                        'line': line_num,
                        'code': line.strip(),
                        'severity': severity,
                        'message': self._get_security_message(pattern_name)
                    })
        
        return issues
    
    def _analyze_code_quality(self, content: str, language: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze code quality issues"""
        issues = []
        lines = content.split('\n')
        
        # Check line length
        for line_num, line in enumerate(lines, 1):
            if len(line) > self.CODE_QUALITY_RULES['max_line_length']:
                issues.append({
                    'type': 'line_too_long',
                    'line': line_num,
                    'length': len(line),
                    'message': f'Line exceeds {self.CODE_QUALITY_RULES["max_line_length"]} characters'
                })
        
        # Language-specific analysis
        if language == 'python':
            issues.extend(self._analyze_python(content))
        elif language in ['javascript', 'typescript']:
            issues.extend(self._analyze_javascript(content))
        
        return issues
    
    def _analyze_python(self, content: str) -> List[Dict[str, Any]]:
        """Analyze Python code"""
        issues = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Check function length
                if isinstance(node, ast.FunctionDef):
                    func_lines = node.end_lineno - node.lineno
                    if func_lines > self.CODE_QUALITY_RULES['max_function_length']:
                        issues.append({
                            'type': 'function_too_long',
                            'function': node.name,
                            'lines': func_lines,
                            'message': f'Function "{node.name}" is too long ({func_lines} lines)'
                        })
                    
                    # Check for docstring
                    if not ast.get_docstring(node) and node.name != '__init__':
                        issues.append({
                            'type': 'missing_docstring',
                            'function': node.name,
                            'message': f'Function "{node.name}" missing docstring'
                        })
        except SyntaxError as e:
            issues.append({
                'type': 'syntax_error',
                'line': e.lineno,
                'message': str(e)
            })
        
        return issues
    
    def _analyze_javascript(self, content: str) -> List[Dict[str, Any]]:
        """Analyze JavaScript/TypeScript code"""
        issues = []
        
        # Check for console.log (should be removed in production)
        if 'console.log' in content:
            issues.append({
                'type': 'debug_code',
                'message': 'Found console.log statements - should be removed in production'
            })
        
        # Check for var usage (should use let/const)
        if re.search(r'\bvar\s+\w+', content):
            issues.append({
                'type': 'deprecated_var',
                'message': 'Using "var" - prefer "let" or "const"'
            })
        
        return issues
    
    def _calculate_metrics(self, content: str, language: str) -> Dict[str, Any]:
        """Calculate code metrics"""
        lines = content.split('\n')
        
        return {
            'total_lines': len(lines),
            'blank_lines': len([l for l in lines if not l.strip()]),
            'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
            'code_lines': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
        }
    
    def _generate_suggestions(self, content: str, language: str, 
                            security_issues: List, quality_issues: List) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if security_issues:
            suggestions.append(f"Fix {len(security_issues)} security vulnerabilities before production")
        
        if quality_issues:
            suggestions.append(f"Refactor {len(quality_issues)} code quality issues for better maintainability")
        
        if len(content) > 10000:
            suggestions.append("Consider breaking this file into smaller modules")
        
        if language == 'python':
            if 'import *' in content:
                suggestions.append("Avoid wildcard imports (import *)")
        
        return suggestions
    
    def _calculate_risk_score(self, security_issues: List) -> str:
        """Calculate overall risk score"""
        if not security_issues:
            return "LOW"
        
        critical_count = len([i for i in security_issues if i.get('severity') == 'CRITICAL'])
        
        if critical_count > 0:
            return "CRITICAL"
        elif len(security_issues) > 5:
            return "HIGH"
        elif len(security_issues) > 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_quality_score(self, quality_issues: List) -> int:
        """Calculate code quality score (0-100)"""
        if not quality_issues:
            return 100
        
        # Deduct points for each issue
        score = 100 - (len(quality_issues) * 2)
        return max(0, score)
    
    def _get_security_message(self, pattern_name: str) -> str:
        """Get user-friendly security message"""
        messages = {
            'sql_injection': 'Potential SQL Injection vulnerability - use parameterized queries',
            'xss_vulnerability': 'Potential XSS vulnerability - sanitize user input',
            'hardcoded_password': 'Hardcoded credentials found - use environment variables',
            'unencrypted_connection': 'Unencrypted connection detected - use HTTPS/TLS',
            'unsafe_deserialization': 'Unsafe deserialization - can lead to RCE',
            'command_injection': 'Potential command injection - avoid system/exec with user input',
            'weak_cryptography': 'Weak cryptographic algorithm - use modern algorithms',
            'path_traversal': 'Potential path traversal vulnerability',
        }
        return messages.get(pattern_name, 'Potential security issue')
