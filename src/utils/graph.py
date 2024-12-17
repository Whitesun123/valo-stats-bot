import matplotlib.pyplot as plt
import io

def generate_triangle_coordinates(rows=5, triangle_height=35, start_x=150, start_y=20):
    triangles = []
    upside_down_triangles = []
    current_y = start_y
    
    for row in range(rows):
        num_triangles = row + 1
        row_width = num_triangles * triangle_height
        row_start_x = start_x - (row_width / 2)
        
        for i in range(num_triangles):
            x = row_start_x + (i * triangle_height)
            triangles.append({
                'points': f"{x} {current_y} {x + triangle_height} {current_y + triangle_height} {x - triangle_height} {current_y + triangle_height}",
                'position': len(triangles)
            })
            
            if row < rows - 1 and i < num_triangles - 1:
                upside_down_triangles.append({
                    'points': f"{x} {current_y + triangle_height} {x + (2 * triangle_height)} {current_y + triangle_height} {x + triangle_height} {current_y + (2 * triangle_height)}"
                })
        
        current_y += triangle_height
    
    return triangles, upside_down_triangles

def create_performance_graph(matches_data, player_name):
    plt.style.use('dark_background')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#2C2F33')  
    ax.set_facecolor('#2C2F33')
    
    kills = []
    deaths = []
    assists = []
    labels = []
    
    for match in reversed(matches_data[:5]):  
        kills.append(match['kills'])
        deaths.append(match['deaths'])
        assists.append(match['assists'])
        labels.append(match['map'][:7])  
    
    ax.plot(range(len(kills)), kills, marker='o', label='Kills', color='#00ff00', linewidth=2)
    ax.plot(range(len(deaths)), deaths, marker='o', label='Deaths', color='#ff4444', linewidth=2)
    ax.plot(range(len(assists)), assists, marker='o', label='Assists', color='#00ffff', linewidth=2)
    
    ax.set_title(f'Last 5 Matches Performance - {player_name}', color='white', pad=20)
    ax.set_xlabel('Maps', color='white')
    ax.set_ylabel('Count', color='white')
    ax.legend(facecolor='#2C2F33', edgecolor='#99AAB5')
    ax.grid(True, linestyle='--', alpha=0.3, color='#99AAB5')
    
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#99AAB5')
    
    plt.xticks(range(len(labels)), labels, rotation=45)
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#2C2F33')
    buf.seek(0)
    plt.close()
    
    return buf