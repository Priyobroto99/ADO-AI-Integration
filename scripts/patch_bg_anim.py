import re

with open('frontend/cat_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
new_css = '''
        @keyframes float1 {
            0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
            50% { transform: translate(-20px, -40px) scale(1.1); opacity: 0.6; }
        }
        @keyframes float2 {
            0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.2; }
            50% { transform: translate(30px, -30px) scale(0.9); opacity: 0.5; }
        }
        @keyframes float3 {
            0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.2; }
            50% { transform: translate(-30px, 30px) scale(1.2); opacity: 0.4; }
        }
        @keyframes ripple {
            0% { transform: scale(0.8) translate(-50%, -50%); opacity: 1; }
            100% { transform: scale(2.5) translate(-20%, -20%); opacity: 0; }
        }
        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .bg-animated-gradient {
            background: linear-gradient(-45deg, #f8fafc, #eff6ff, #e0e7ff, #f8fafc);
            background-size: 400% 400%;
            animation: gradientMove 15s ease infinite;
        }
    </style>
'''
content = content.replace('</style>', new_css)

# 2. Replace loggedOutState HTML
old_logged_out = '''<div id="loggedOutState" class="hidden flex-col items-center justify-center h-[60vh] gap-8">
            <div class="relative w-64 h-64 border-b-2 border-l-2 border-gray-200">
                <!-- Animated Bars -->
                <div class="absolute bottom-0 left-6 w-10 bg-blue-300 rounded-t-sm" style="animation: growBar 2s ease-in-out infinite 0s;"></div>
                <div class="absolute bottom-0 left-20 w-10 bg-blue-400 rounded-t-sm" style="animation: growBar 2s ease-in-out infinite 0.4s;"></div>
                <div class="absolute bottom-0 left-36 w-10 bg-indigo-500 rounded-t-sm" style="animation: growBar 2s ease-in-out infinite 0.8s;"></div>
                <div class="absolute bottom-0 left-52 w-10 bg-blue-600 rounded-t-sm" style="animation: growBar 2s ease-in-out infinite 1.2s;"></div>
                
                <!-- Animated Trend Line -->
                <svg class="absolute inset-0 w-full h-full text-green-500 z-10 drop-shadow-md" fill="none" stroke="currentColor" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <path stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M10,80 L35,45 L60,55 L95,15" stroke-dasharray="200" style="animation: dashLine 4s ease-in-out infinite;"></path>
                    <circle cx="95" cy="15" r="3" fill="currentColor" class="animate-pulse"></circle>
                </svg>
            </div>
            <div class="text-center">
                <h2 class="text-3xl font-bold text-gray-800 tracking-tight">CAT Delivery Excellence</h2>
                <p class="text-gray-500 mt-2 text-sm max-w-sm mx-auto">Please login to access real-time team metrics, performance analytics, and advanced tracker configurations.</p>
            </div>
        </div>'''

new_logged_out = '''<div id="loggedOutState" class="hidden relative flex-col items-center justify-center min-h-[65vh] w-full gap-8 rounded-xl bg-animated-gradient overflow-hidden border border-gray-100 shadow-sm mt-4">
            
            <!-- Background Floating Elements -->
            <div class="absolute top-10 left-10 w-32 h-32 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl" style="animation: float1 8s ease-in-out infinite;"></div>
            <div class="absolute top-20 right-20 w-40 h-40 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl" style="animation: float2 10s ease-in-out infinite;"></div>
            <div class="absolute bottom-10 left-32 w-36 h-36 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl" style="animation: float3 12s ease-in-out infinite;"></div>
            
            <!-- Pulse Rings Behind Icon -->
            <div class="absolute top-1/2 left-1/2 w-64 h-64 border border-blue-300 rounded-full" style="animation: ripple 3s linear infinite; transform-origin: top left;"></div>
            <div class="absolute top-1/2 left-1/2 w-64 h-64 border border-indigo-200 rounded-full" style="animation: ripple 3s linear infinite 1.5s; transform-origin: top left;"></div>

            <!-- Foreground Animated Icon -->
            <div class="relative w-64 h-64 border-b-2 border-l-2 border-gray-300 z-10 backdrop-blur-sm bg-white/20 p-4 rounded-lg shadow-sm">
                <!-- Animated Bars -->
                <div class="absolute bottom-0 left-6 w-10 bg-blue-400 rounded-t-sm drop-shadow-sm" style="animation: growBar 2s ease-in-out infinite 0s;"></div>
                <div class="absolute bottom-0 left-20 w-10 bg-indigo-400 rounded-t-sm drop-shadow-sm" style="animation: growBar 2s ease-in-out infinite 0.4s;"></div>
                <div class="absolute bottom-0 left-36 w-10 bg-purple-500 rounded-t-sm drop-shadow-sm" style="animation: growBar 2s ease-in-out infinite 0.8s;"></div>
                <div class="absolute bottom-0 left-52 w-10 bg-blue-600 rounded-t-sm drop-shadow-sm" style="animation: growBar 2s ease-in-out infinite 1.2s;"></div>
                
                <!-- Animated Trend Line -->
                <svg class="absolute inset-0 w-full h-full text-green-500 z-10 drop-shadow-md" fill="none" stroke="currentColor" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <path stroke-width="4" stroke-linecap="round" stroke-linejoin="round" d="M10,80 L35,45 L60,55 L95,15" stroke-dasharray="200" style="animation: dashLine 4s ease-in-out infinite;"></path>
                    <circle cx="95" cy="15" r="4" fill="currentColor" class="animate-pulse"></circle>
                </svg>
            </div>
            
            <!-- Text Content -->
            <div class="text-center z-10 bg-white/40 px-8 py-4 rounded-xl backdrop-blur-sm shadow-sm border border-white/50">
                <h2 class="text-3xl font-bold text-gray-800 tracking-tight drop-shadow-sm">CAT Delivery Excellence</h2>
                <p class="text-gray-600 mt-2 text-sm max-w-sm mx-auto font-medium">Please login to access real-time team metrics, performance analytics, and advanced tracker configurations.</p>
            </div>
        </div>'''
        
content = content.replace(old_logged_out, new_logged_out)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
