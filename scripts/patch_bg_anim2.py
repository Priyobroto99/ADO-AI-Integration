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
        @keyframes float4 {
            0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.15; }
            50% { transform: translate(40px, 40px) scale(1.3); opacity: 0.4; }
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
        @keyframes panGrid {
            0% { background-position: 0 0; }
            100% { background-position: 40px 40px; }
        }
        .bg-animated-gradient {
            background: linear-gradient(-45deg, #f8fafc, #eff6ff, #e0e7ff, #f8fafc);
            background-size: 400% 400%;
            animation: gradientMove 15s ease infinite;
        }
        .bg-animated-grid {
            background-size: 40px 40px;
            background-image: 
                linear-gradient(to right, rgba(99, 102, 241, 0.05) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(99, 102, 241, 0.05) 1px, transparent 1px);
            animation: panGrid 20s linear infinite;
        }
    </style>
'''
# We will use regex to replace all existing animation css blocks to clean it up and add the new one.
# Find the start of @keyframes float1 up to </style>
content = re.sub(r'@keyframes float1.*?</style>', new_css.strip(), content, flags=re.DOTALL)


# 2. Replace loggedOutState HTML
old_logged_out = re.compile(r'<div id="loggedOutState".*?</div>\s*</div>\s*</div>', re.DOTALL)

new_logged_out = '''<div id="loggedOutState" class="hidden relative flex-col items-center justify-center min-h-[82vh] w-full gap-8 rounded-2xl bg-animated-gradient overflow-hidden border border-gray-200 shadow-sm mt-2">
            
            <!-- Panning Grid Background -->
            <div class="absolute inset-0 bg-animated-grid mix-blend-multiply opacity-60"></div>
            
            <!-- Floating Data Orbs (Expanded) -->
            <div class="absolute top-10 left-10 w-32 h-32 bg-blue-300 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float1 8s ease-in-out infinite;"></div>
            <div class="absolute top-20 right-20 w-48 h-48 bg-indigo-200 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float2 10s ease-in-out infinite;"></div>
            <div class="absolute bottom-10 left-32 w-36 h-36 bg-purple-200 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float3 12s ease-in-out infinite;"></div>
            <div class="absolute bottom-20 right-32 w-40 h-40 bg-blue-200 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float4 14s ease-in-out infinite;"></div>
            <div class="absolute top-1/2 left-4 w-24 h-24 bg-purple-300 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float2 9s ease-in-out infinite;"></div>
            <div class="absolute bottom-1/4 right-10 w-28 h-28 bg-indigo-300 rounded-full mix-blend-multiply filter blur-2xl" style="animation: float1 11s ease-in-out infinite;"></div>
            
            <!-- Floating Data Strings/Nodes -->
            <div class="absolute top-1/4 left-1/4 text-xs text-blue-600/30 font-mono tracking-widest font-bold" style="animation: float1 15s infinite;">0100110</div>
            <div class="absolute bottom-1/3 right-1/4 text-xs text-indigo-600/30 font-mono tracking-widest font-bold" style="animation: float2 18s infinite;">DATA.SYNC()</div>
            <div class="absolute top-1/2 right-[15%] text-xs text-purple-600/30 font-mono tracking-widest font-bold" style="animation: float3 12s infinite;">{ metrics: live }</div>
            <div class="absolute bottom-[20%] left-[15%] text-xs text-blue-600/30 font-mono tracking-widest font-bold" style="animation: float4 14s infinite;">SYSTEM.ONLINE</div>
            <div class="absolute top-[15%] right-[30%] text-xs text-indigo-600/30 font-mono tracking-widest font-bold" style="animation: float1 16s infinite;">await fetchMetrics()</div>

            <!-- Pulse Rings Behind Icon -->
            <div class="absolute top-1/2 left-1/2 w-80 h-80 border border-blue-400/40 rounded-full" style="animation: ripple 3s linear infinite; transform-origin: top left;"></div>
            <div class="absolute top-1/2 left-1/2 w-80 h-80 border border-indigo-300/40 rounded-full" style="animation: ripple 3s linear infinite 1.5s; transform-origin: top left;"></div>
            <div class="absolute top-1/2 left-1/2 w-[28rem] h-[28rem] border border-purple-200/30 rounded-full" style="animation: ripple 4s linear infinite 0.75s; transform-origin: top left;"></div>

            <!-- Foreground Animated Icon -->
            <div class="relative w-72 h-72 border-b-4 border-l-4 border-gray-300/80 z-10 backdrop-blur-md bg-white/40 p-5 rounded-xl shadow-lg">
                <!-- Animated Bars -->
                <div class="absolute bottom-0 left-6 w-12 bg-blue-400 rounded-t-md drop-shadow-md" style="animation: growBar 2s ease-in-out infinite 0s;"></div>
                <div class="absolute bottom-0 left-24 w-12 bg-indigo-400 rounded-t-md drop-shadow-md" style="animation: growBar 2s ease-in-out infinite 0.4s;"></div>
                <div class="absolute bottom-0 left-44 w-12 bg-purple-500 rounded-t-md drop-shadow-md" style="animation: growBar 2s ease-in-out infinite 0.8s;"></div>
                <div class="absolute bottom-0 left-64 w-12 bg-blue-600 rounded-t-md drop-shadow-md" style="animation: growBar 2s ease-in-out infinite 1.2s;"></div>
                
                <!-- Animated Trend Line -->
                <svg class="absolute inset-0 w-full h-full text-green-500 z-20 drop-shadow-lg" fill="none" stroke="currentColor" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <path stroke-width="4" stroke-linecap="round" stroke-linejoin="round" d="M8,80 L32,45 L58,55 L95,15" stroke-dasharray="200" style="animation: dashLine 4s ease-in-out infinite;"></path>
                    <circle cx="95" cy="15" r="5" fill="currentColor" class="animate-pulse shadow-green-500"></circle>
                </svg>
            </div>
            
            <!-- Text Content -->
            <div class="text-center z-10 bg-white/60 px-10 py-5 rounded-2xl backdrop-blur-md shadow-lg border border-white/80 mt-4">
                <h2 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-indigo-700 tracking-tight drop-shadow-sm">CAT Delivery Excellence</h2>
                <p class="text-gray-700 mt-3 text-base max-w-md mx-auto font-medium">Please login to access real-time team metrics, performance analytics, and advanced tracker configurations.</p>
            </div>
        </div>'''
        
content = old_logged_out.sub(new_logged_out, content, count=1)

with open('frontend/cat_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
