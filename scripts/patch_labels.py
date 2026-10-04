import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

mapping_code = '''
        const friendlyNames = {
            'spAssigned': 'Story Points Assigned',
            'spCompleted': 'Story Points Completed',
            'usAssigned': 'User Stories Assigned',
            'usCompleted': 'User Stories Completed',
            'usPushed': 'User Stories Pushed',
            'defectLeakage': 'Defect Leakage (%)',
            'prodIncidents': 'Production Incidents',
            'openRisks': 'Open Risks',
            'escalations': 'Escalations',
            'autoCoverage': 'Automation Coverage (%)',
            'autoStability': 'Automation Stability (%)',
            'autoToolsReq': 'Automation Tools Gap',
            'buildToolsReq': 'Build Tools Gap',
            'sowMilestones': 'SOW Milestones',
            'regRunTime': 'Regression Run Time',
            'regExecTimeNoAuto': 'Regression Exec Time (No Auto)',
            'autoBugs': 'Automation Bugs',
            'kt': 'Knowledge Transfer',
            'assets': 'Assets Created',
            'usAssignedPts': 'US Assigned Details',
            'defectPts': 'Defect Details',
            'incidentPts': 'Incident Details',
            'riskPts': 'Risk Details',
            'sowPts': 'SOW Details',
            'escalationPts': 'Escalation Details',
            'autoToolPts': 'Auto Tool Details',
            'buildToolPts': 'Build Tool Details',
            'cloudProf': 'Cloud Proficiency',
            'cicdSetup': 'CI/CD Setup',
            'ktPrep': 'KT Preparation',
            'autoBugsPts': 'Auto Bugs Details',
            'cicdMat': 'CI/CD Maturity',
            'assetPts': 'Asset Details',
            'deloitteTime': 'Deloitte Time',
            'tenroxTime': 'Tenrox Time',
            'catManager': 'CAT Manager',
            'engagementCode': 'Engagement Code',
            'lobLead': 'LOB Lead',
            'processComp': 'Process Compliance (%)'
        };

        function getFriendlyName(key) {
            let label = key;
            if (key.endsWith('_expected')) {
                const base = key.replace('_expected', '');
                label = (friendlyNames[base] || base) + ' (Expected)';
            } else if (key.endsWith('_variance')) {
                const base = key.replace('_variance', '');
                label = (friendlyNames[base] || base) + ' (Variance)';
            } else {
                label = friendlyNames[key] || key;
            }
            if (label === key) {
                label = label.replace(/([A-Z])/g, ' ').replace(/^./, function(str){ return str.toUpperCase(); });
            }
            return label;
        }

        function renderUpdateForm() {'''

content = content.replace('function renderUpdateForm() {', mapping_code)

old_label = '''<label class="block text-xs text-tremor-content font-medium mb-1">' + k + '</label>'''
new_label = '''<label class="block text-xs text-tremor-content font-medium mb-1">' + getFriendlyName(k) + '</label>'''

content = content.replace(old_label, new_label)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
